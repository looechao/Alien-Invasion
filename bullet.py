import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):	
    """管理子弹"""
    def __init__(self, ai_game):
        """创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在 (0, 0) 处创建一个圆形子弹，并将其位置设置为飞船顶部中央
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_width)
        self.rect.center = ai_game.ship.rect.midtop
        self.radius = self.settings.bullet_width // 2

        # 存储子弹的位置
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """向上移动子弹"""
        # 更新子弹位置的小数值
        self.y -= self.settings.bullet_speed
        # 更新表示子弹的 rect 和圆心的位置
        self.rect.y = self.y
        self.rect.x = self.x
        self.center = (int(self.x + self.radius), int(self.y + self.radius))

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.circle(self.screen, self.color, self.rect.center, self.radius)
