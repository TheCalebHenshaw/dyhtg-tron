import pygame
import os

image_path = 'media/Sprites/spaceships/PNG/Spaceships/ship/'

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, controls, name, image=None) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        # Load images for the spaceship
        self.images = []
        for i in range(1, 5):
            img = pygame.image.load(os.path.join(image_path + str(i) + '.png'))
            img = pygame.transform.scale(img, (65, 42))  # Scale down to fit screen size
            self.images.append(img)
        
        # Set initial image and rect
        self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Set initial position at center

        # Player details
        self.name = name
        self.color = color
        self.controls = controls
        self.trail = [self.rect.center]  # Initialize trail with the center position
        self.alive = True
        self.direction = "RIGHT"
        self.x = x
        self.y = y
        self.size = 5
        self.speed = 5
        self.x_collision = 155
        self.y_collision = 5

        self.base_speed = 5
        self.is_invincible = False

        self.speed_timer = 0
        self.size_timer = 0

        self.default_size = 100
        self.bigger = 150
        self.smaller = 50
        self.cur_size = self.default_size

        

    def handle_controls(self,keys):
        if keys[self.controls['up']] and self.direction !='DOWN':
            self.direction = "UP"
        elif keys[self.controls['down']] and self.direction != 'UP':
            self.direction = "DOWN"
        elif keys[self.controls['left']] and self.direction != 'RIGHT':
            self.direction = "LEFT"
        elif keys[self.controls['right']] and self.direction != 'LEFT':
            self.direction = "RIGHT"

    def move(self):

        if self.speed_timer > 0:
            self.speed_timer -= 1
            if self.speed_timer == 0:
                self.speed = self.base_speed  # Reset speed when timer expires

        if self.size_timer > 0:
            self.size_timer -= 1
            if self.size_timer == 0:
                self.reset_size() 

        # Update image and move based on direction
        if self.direction == "RIGHT":
            self.image = self.images[1]
            self.rect.x += self.speed
        elif self.direction == "LEFT":
            self.image = self.images[3]
            self.rect.x -= self.speed
        elif self.direction == "UP":
            self.image = self.images[0]
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.image = self.images[2]
            self.rect.y += self.speed

        # Add the new center position to the trail
        self.trail.append(self.rect.center)
        if len(self.trail) > self.cur_size:
            self.trail.pop(0)  # Remove the oldest trail point

    def draw(self, screen):
        # Draw the player's sprite at the updated rect position
        screen.blit(self.image, self.rect)

        # Draw the player's trail as rectangles
        for segment in self.trail[:-1]:  # Leave out the current position
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], self.size, self.size))

    def speed_boost(self):
        self.speed = 7  # Increase speed temporarily
        self.speed_timer = 300  # Speed boost lasts for 300 frames (5 seconds at 60fps)

    def slow(self):
        # Reduce player size and image
        self.speed = 3
        self.speed_timer = 300 

    def double_size(self):
        # Double player size and image
        self.size = 20
        self.size_timer = 300  # Double size lasts for 5 seconds

    def reset_size(self):
        # Reset player size and image
        self.cur_size = self.default_size
        


    def checkForCollision(self,arenaWidth,arenaHeight,otherTrailList):
        #checks if they have collided into the wall
        if self.rect.x >= arenaWidth-self.x_collision or self.rect.x < self.x_collision or self.rect.y >= arenaHeight-self.y_collision or self.rect.y < self.y_collision:
            print(f"Has died",self.name)
            self.alive = False

        # Check if the player has collided with their own trail
        if self.rect.center in self.trail[:-1] and not self.is_invincible:
            print(f"Has died",self.name)
            self.alive = False

        # Check if the player has collided with the other player's trail
        if self.rect.center in otherTrailList[:-1] and not self.is_invincible:
            print(f"Has died",self.name)
            self.alive = False

    def reset(self, x, y):
        # Reset player position, trail, and direction
        self.rect.center = (x, y)
        self.trail = [self.rect.center]
        self.direction = "RIGHT"
        self.alive = True
