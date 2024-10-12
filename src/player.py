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
        self.size = 5  # Trail size
        self.speed = 5  # Movement speed

    def handle_controls(self, keys):
        if keys[self.controls['up']] and self.direction != 'DOWN':
            self.direction = "UP"
        elif keys[self.controls['down']] and self.direction != 'UP':
            self.direction = "DOWN"
        elif keys[self.controls['left']] and self.direction != 'RIGHT':
            self.direction = "LEFT"
        elif keys[self.controls['right']] and self.direction != 'LEFT':
            self.direction = "RIGHT"

    def move(self):
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
        if len(self.trail) > 25:
            self.trail.pop(0)  # Remove the oldest trail point

    def draw(self, screen):
        # Draw the player's sprite at the updated rect position
        screen.blit(self.image, self.rect)

        # Draw the player's trail as rectangles
        for segment in self.trail[:-1]:  # Leave out the current position
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], self.size, self.size))

    def checkForCollision(self, arenaWidth, arenaHeight, otherTrailList):
        # Check if the player has collided with the walls
        if self.rect.x >= arenaWidth or self.rect.x < 0 or self.rect.y >= arenaHeight or self.rect.y < 0:
            self.alive = False

        # Check if the player has collided with their own trail
        if self.rect.center in self.trail[:-1]:
            self.alive = False

        # Check if the player has collided with the other player's trail
        if self.rect.center in otherTrailList[:-1]:
            self.alive = False

    def reset(self, x, y):
        # Reset player position, trail, and direction
        self.rect.center = (x, y)
        self.trail = [self.rect.center]
        self.direction = "RIGHT"
        self.alive = True
