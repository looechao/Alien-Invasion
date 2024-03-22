import pygame
from pygame.sprite import Sprite


class Weaponbonus(Sprite):
    """A class to represent a single power-up in the game."""

    def __init__(self, ai_game):
        """Initialize the power-up and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the power-up image and set its rect attribute.
        self.image = pygame.image.load('images/weaponbonus.png')
        self.rect = self.image.get_rect()

        # Start each new power-up near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the power-up's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the power-up down."""
        self.rect.y += self.settings.weaponbonus_speed

    def blitme(self):
        """Draw the power-up at its current location."""
        self.screen.blit(self.image, self.rect)