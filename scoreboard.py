import pygame.font
from ship import Ship
from ship2 import Ship2
from pygame.sprite import Group


class Scoreboard:
	"""显示得分信息的类"""

	def __init__(self,ai_game):
		"""初始化显示得分涉及的属性"""
		self.ai_game=ai_game
		self.screen=ai_game.screen
		self.screen_rect=self.screen.get_rect()
		self.settings=ai_game.settings
		self.stats=ai_game.stats

		#显示得分信息时使用的字体设置
		self.text_color=(255,255,255)
		self.font=pygame.font.SysFont(None,48)
		#准备初始得分和最高得分的图像
		self.prep_score()
		self.prep_high_score()
		self.prep_high_score2()

		#显示当前等级的图像
		self.prep_level()

		#显示剩余的飞船数量：
		self.prep_ships()
		self.prep_ships2()


	def prep_ships(self):
		"""显示还会剩下多少只飞船"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship=Ship(self.ai_game)
			ship.draw_shipleft('images/left.png')
			ship.rect.x = ship_number * 50
			ship.rect.y=10
			self.ships.add(ship)

	def prep_ships2(self):
		"""显示2p还会剩下多少只飞船"""
		self.shs = Group()
		for shs_number in range(self.stats.ships_left2):
			ship2=Ship2(self.ai_game)
			ship2.draw_shipleft('images/left2.png')
			ship2.rect.x = shs_number * 50
			ship2.rect.y=50
			self.shs.add(ship2)

	'''最高得分图像'''
	def prep_high_score(self):
		'''将最高得分渲染成图像'''
		high_score = round(self.stats.high_score,-1)
		high_score_str = "Highest:"+"{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)
		#在屏幕顶部中央显示最高得分
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top=self.score_rect.top
	def prep_high_score2(self):
		'''将最高得分渲染成图像'''
		high_score2 = round(self.stats.high_score2,-1)
		high_score_str2 = "Highest:"+"{:,}".format(high_score2)
		self.high_score_image2 = self.font.render(high_score_str2,True,self.text_color,self.settings.bg_color)
		#在屏幕顶部中央显示最高得分
		self.high_score_rect2 = self.high_score_image2.get_rect()
		self.high_score_rect2.centerx = self.screen_rect.centerx
		self.high_score_rect2.top=self.score_rect.top


	def prep_score(self):
		score_str=str(self.stats.score)
		"""将得分转换为渲染的图像"""
		rounded_score=round(self.stats.score,-1)
		score_str = "{:,}".format(rounded_score)
		self.score_image=self.font.render(score_str,True,self.text_color,self.settings.bg_color)

		#在屏幕右上角显示得分
		self.score_rect=self.score_image.get_rect()
		self.score_rect.right=self.screen_rect.right-20
		self.score_rect.top=20




	def show_score(self):
		"""在屏幕上显示得分"""
		self.screen.blit(self.score_image,self.score_rect)
		'''在屏幕顶部中央显示最高得分'''
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		#在屏幕左上角绘制飞船：
		self.ships.draw(self.screen)
	def show_score2(self):
		"""在屏幕上显示2P游戏得分"""
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image2,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		#在屏幕左上角绘制第一艘飞船：
		self.ships.draw(self.screen)
		self.shs.draw(self.screen)

	def check_high_score(self):
		'''检查是否诞生了最高得分'''
		if self.stats.score>self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()
	def check_high_score2(self):
		'''检查是否诞生了最高得分'''
		if self.stats.score>self.stats.high_score2:
			self.stats.high_score2 = self.stats.score
			self.prep_high_score2()

	def prep_level(self):
		"""将等级转换为渲染的图像"""
		level_str=str(self.stats.level)
		self.level_image=self.font.render(level_str,True,self.text_color,self.settings.bg_color)

		#在得分下方显示等级
		self.level_rect=self.level_image.get_rect()
		self.level_rect.right=self.score_rect.right
		self.level_rect.top=self.score_rect.bottom +2