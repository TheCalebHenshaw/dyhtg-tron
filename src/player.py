import pygame



class Player:
    def __init__(self,x,y,color,controls,name,image) -> None:
        self.x = x
        self.y = y
        self.image = image
        self.name = name
        self.color = color
        self.controls = controls
        self.trail = [(self.x,self.y)]
        self.alive = True
        self.direction = "RIGHT"
        self.size = 5
        self.speed = 5
        self.x_collision = 155
        self.y_collision = 5

        

    def handle_controls(self,keys):
        if keys[self.controls['up']] and self.direction !='DOWN':
            self.direction = "UP"
        if keys[self.controls['down']] and self.direction !='UP':
            self.direction = "DOWN"
        if keys[self.controls['left']] and self.direction !='RIGHT':
            self.direction = "LEFT"
        if keys[self.controls['right']] and self.direction !='LEFT':
            self.direction = "RIGHT"
    def move(self):
        if self.direction=="RIGHT":
            self.x+=self.speed
        elif self.direction=="LEFT":
            self.x-=self.speed
        elif self.direction=="UP":
            self.y-=self.speed
        elif self.direction=="DOWN":
            self.y+=self.speed
    
        self.trail.append((self.x,self.y))
        if len(self.trail) > 25:
            self.trail.remove(self.trail[0])

    def draw(self, screen):
        #draw player as rectangle for now
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

        # player trail
        for segment in self.trail:
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], self.size, self.size))


    def checkForCollision(self,arenaWidth,arenaHeight,otherTrailList):
        #checks if they have collided into the wall
        if self.x >= arenaWidth-self.x_collision or self.x < self.x_collision or self.y >= arenaHeight-self.y_collision or self.y < self.y_collision:
            self.alive = False
        # check if player self collides

        if (self.x,self.y) in self.trail[:-1]:
            self.alive = False
        
        # check if player x and y is inside otherTrailList except for [:-1]
        if (self.x,self.y) in otherTrailList[:-1]:
            self.alive = False

    def reset(self,x,y):
        self.x = x
        self.y = y
        self.trail = [(self.x,self.y)]
        self.direction = "RIGHT"