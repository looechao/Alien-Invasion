import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""管理飞船的类"""
	def __init__(self, ai_game):
			##初始化飞船并设置其初始位置
		self.screen=ai_game.screen
		self.screen_rect=ai_game.screen.get_rect()
		self.settings = ai_game.settings
		#加载飞船图像并获得其外接矩形
		self.image=pygame.image.load('images/ship.png')
		self.rect = self.image.get_rect()	
		 	#对于每搜新飞船，都将其放在屏幕底部的中央
		self.rect.midbottom=self.screen_rect.midbottom

		#在飞船的属性x中存储小数值
		self.x=float(self.rect.x)

		#移动标志
		self.moving_right=False
		self.moving_left=False

		#设置是否可见
		self.visible = True

		super().__init__()


	def update(self):
		#根据移动标志调整飞船的位置
		#更新飞船而不只是rect对象的值
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.rect.x+=self.settings.ship_speed
		if self.moving_left and self.rect.left>0:
			self.rect.x-=self.settings.ship_speed
	def center_ship(self):
		"""让飞船在屏幕中央"""
		self.rect.midbottom=self.screen_rect.midbottom
		self.x=float(self.rect.x)

	def draw_shipleft(self,image_path):
		'''画剩余飞船数量的图像'''
		self.image = pygame.image.load(image_path)

			

	def blitme(self):
			#在指定位置绘制飞船
			self.screen.blit(self.image,self.rect)

	def set_invisible(self):
		"""隐藏飞船"""
		self.visible=False
		self.rect.y = -self.rect.height
