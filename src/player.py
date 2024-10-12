import pygame


class Player:
    def __init__(self,x,y,color,controls) -> None:
        self.x = x
        self.y = y
        self.color = color
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
    
