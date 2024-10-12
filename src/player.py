import pygame
from color import Color


class Player:
    def __init__(self,x,y,color,controls,name) -> None:
        self.x = x
        self.y = y
        self.name = name
        self.color = Color.BLUE
        self.controls = controls
        self.trail = [(self.x,self.y)]
        self.alive = True
        self.direction = "RIGHT"
        self.size = 10
        self.speed = 10

        

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
            self.y+=self.speed
        elif self.direction=="DOWN":
            self.y-=self.speed
    
        self.trail.append((self.x,self.y))

    def draw(self, screen):
        #draw player as rectangle for now
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

        # player trail
        for segment in self.trail:
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], self.size, self.size))


    def checkForCollision(self,arenaWidth,arenaHeight):
        #checks if they have collided into the wall
        if self.x >= arenaWidth or self.x < 0 or self.y >= arenaHeight or self.y < 0:
            self.alive = False
        # check if player self collides

        if (self.x,self.y) in self.trail[:-1]:
            self.alive = False
    def reset(self,x,y):
        self.x = x
        self.y = y
        self.trail = [(self.x,self.y)]
        self.direction = "RIGHT"