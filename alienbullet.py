import pygame
from pygame.sprite import Sprite
 
class Alienbullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alienbullet_color
        self.rect = pygame.Rect(0, 0, self.settings.alienbullet_width, self.settings.alienbullet_height)

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.alienbullet_width,
            self.settings.alienbullet_height)
        self.rect.midbottom = ai_game.alien.rect.midbottom
        
        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y += self.settings.alienbullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_alienbullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
