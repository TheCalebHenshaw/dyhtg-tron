import pygame
import os
import random


invincibility_im = os.path.join("media", "Sprites", "powerups",  "invincibility.png")
speed_im = os.path.join("media", "Sprites", "powerups",  "speed.png")
double_size_im =  os.path.join("media", "Sprites", "powerups",  "double_size.png")
half_size_im = os.path.join("media", "Sprites", "powerups",  "half_size.png")

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, effect_type):
        super().__init__()
        
        # Load different images based on the power-up type
        if effect_type == 'speed_boost':
            self.image = pygame.image.load(speed_im)
        elif effect_type == 'slow':
            self.image = pygame.image.load(half_size_im)
        elif effect_type == 'double_size':
            self.image = pygame.image.load(double_size_im)
        

        self.image = pygame.transform.scale(self.image, (30, 30))  # Adjust power-up size
        self.rect = self.image.get_rect(center = (x, y))
        self.effect_type = effect_type  # Types: 'speed_boost', 'invincibility', 'shrink', 'double_size'

    def apply_effect(self, player):
        if self.effect_type == 'speed_boost':
            player.speed_boost()
        elif self.effect_type == 'slow':
            player.slow()
        elif self.effect_type == 'double_size':
            player.double_size()

