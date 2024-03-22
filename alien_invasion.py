import sys
import time
import pygame
import numpy as np
import random
import time
from settings import Settings
from ship import Ship
from ship2 import Ship2
from bullet import Bullet
from alienbullet import Alienbullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from time import sleep
from bonus import Bonus
from weaponbonus import Weaponbonus

class AlienInvasion:
	#管理游戏资源和行为的类
	def __init__(self):
	#初始化游戏并创建游戏资源
		pygame.init()
		self.settings=Settings()
		self.bonus_counter= 0
		self.bonus_limit=300
		self.bonuses = pygame.sprite.Group()

		self.weaponbonus_counter= 0
		self.weaponbonus_limit=300
		self.weaponbonuses = pygame.sprite.Group()
		self.last_width_change = 0

		self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")
		self.ship=Ship(self)
		self.ship2=Ship2(self)
		self.bullets=pygame.sprite.Group()

		self.aliens=pygame.sprite.Group()
		#创建存储游戏统计信息的实例
		self.stats=GameStats(self)
		# 创建记分牌
		self.sb=Scoreboard(self)
		self.sb2=Scoreboard(self)


		self._create_fleet()
		#创建play按钮和其它按钮
		self.play_button=Button(self,"Single Player mode",0)
		self.play_button2=Button(self,"Multi Player Mode",1)
		self.help_button=Button(self,"Help",2)

		

	def run_game(self):
	##开始游戏的主循环
		while True:
			if not self.stats.game_active:
				self._update_screen()  
				self._check_events()
				self.stats.reset_stats()
			if self.stats.game_active and not self.stats.multi_player:
				self._update_screen()  
				self._check_events()
				self.ship.update()
				self.bullets.update()
				self._update_bullets()
				self._update_aliens()
				self._update_bonus()
				self._create_bonus()
				self._update_weaponbonus()
				self._create_weaponbonus()
			if self.stats.game_active and self.stats.multi_player:
				self._update_screen()  
				self._check_events()
				self.ship.update()
				self.ship2.update()
				self.bullets.update()
				self.ship2.bullets.update()
				self._update_bullets()
				self._update_aliens()
				self._update_weaponbonus()
				self._create_weaponbonus()


			#监视键盘和鼠标事件
	def _check_events(self):
		    #响应鼠标和键盘按键
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						self._check_keydown_events(event)
					elif event.type==pygame.KEYUP:
						self._check_keyup_events(event)
					elif event.type==pygame.MOUSEBUTTONDOWN:
						mouse_pos=pygame.mouse.get_pos()
						self._check_play_button(mouse_pos)
						self._check_play_button2(mouse_pos)
						self._check_help_button(mouse_pos)

	
	def _check_keydown_events(self,event):
		"""响应按键"""
		screen=self.screen
		if event.key == pygame.K_RIGHT:
			#让飞船向右边移动
			self.ship.moving_right=True
		elif event.key == pygame.K_LEFT:
			#让飞船向左边移动
			self.ship.moving_left=True
		if event.key == pygame.K_d:
			#让飞船向右边移动
			self.ship2.moving_right=True
		elif event.key == pygame.K_a:
			#让飞船向左边移动
			self.ship2.moving_left=True		
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_UP and self.stats.game_active:
			self._fire_bullet()
		elif event.key == pygame.K_SPACE and self.stats.game_active:
			self.ship2.fire_bullet()	
		elif event.key == pygame.K_p:
			self._start_game()

	def _start_game(self):
		pygame.mouse.set_visible(True)
		#重置游戏统计信息：
		self.stats.reset_stats()
		self.stats.game_active=False

		#清空余下的外星人和子弹
		self.aliens.empty()
		self.bullets.empty()
		self.ship2.bullets.empty()
		self.bonuses.empty()
		self.weaponbonuses.empty()


	def _check_keyup_events(self,event):
		"""响应松开"""
		if event.key==pygame.K_RIGHT:
 			self.ship.moving_right=False
		elif event.key==pygame.K_LEFT:
			self.ship.moving_left=False	

		if event.key==pygame.K_d:
 			self.ship2.moving_right=False
		elif event.key==pygame.K_a:
			self.ship2.moving_left=False		
	def _check_play_button(self,mouse_pos):
		"""在玩家单击play按钮时开始游戏"""
		button_clicked=self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.multi_player:
			#隐藏鼠标
			pygame.mouse.set_visible(False)
			#重置游戏统计信息：
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active=True
			self.stats.multi_player=False
			self.sb.prep_score()
			self.sb.prep_ships()
			self.sb.prep_level()

			#清空余下的外星人和子弹
			self.aliens.empty()
			self.bullets.empty()
			self.ship2.set_invisible()

			#创建一群新的外星人并让飞船居中
			self._create_fleet()
			self.ship.center_ship()
	def _check_play_button2(self,mouse_pos):
		"""在玩家单击play按钮时开始游戏"""
		button_clicked=self.play_button2.rect.collidepoint(mouse_pos)
		if button_clicked:
			#隐藏鼠标
			pygame.mouse.set_visible(False)
			#重置游戏统计信息：
			self.settings.initialize_dynamic_settings()
			self.stats.multi_player=True
			self.stats.game_active=True

			#清空余下的外星人和子弹
			self.aliens.empty()
			self.bullets.empty()

			#创建一群新的外星人并让飞船居中
			self._create_fleet()
			self.ship.center_ship()
			self.ship2.center_ship()

			#设置两个玩家的出事的分和剩余飞船的数量
			self.sb2.prep_score()
			self.sb2.prep_level()
			self.sb2.prep_ships()
			self.sb2.prep_ships2()

			#将当前玩家设置为玩家1
			self.current_player = 1

	def _check_help_button(self,mouse_pos):
		"""在玩家单击play按钮时开始游戏"""
		button_clicked=self.help_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#显示帮助对话框：
			help_dialog=HelpDialog()
			help_dialog.show()

	def _fire_bullet(self):
		"""创建一颗子弹，并将其加入编组bullets中"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet=Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""更新子弹的位置并删除消失的子弹"""
		#更新子弹的位置：
		self.bullets.update()
		self.ship2.bullets.update()

		self.ship_group = pygame.sprite.Group(self.ship)
		self.ship2_group = pygame.sprite.Group(self.ship2)

		for alien in self.aliens:
			for alienbullet in alien.alienbullets.sprites():
				alienbullet.update()
		#删除消失的子弹
		for bullet in self.bullets.copy():
			if bullet.rect.bottom<=0:
				self.bullets.remove(bullet)

		for bullet in self.ship2.bullets.copy():
			if bullet.rect.bottom<=0:
				self.ship2.bullets.remove(bullet)

		for alien in self.aliens:
			for alienbullet in alien.alienbullets.sprites():
				if alienbullet.rect.bottom<=0:
					self.alien.alienbullets.remove(alienbullet)

		for alien in self.aliens:
			for alienbullet in alien.alienbullets:
				if pygame.sprite.spritecollide(alienbullet, self.ship_group, True):
				# 处理外星人子弹击中self.ship的情况
					if self.stats.ships_left>0:
						#将ship_left-1
						self.stats.ships_left-=1
						if self.stats.multi_player:
							alien.alienbullets.remove(alienbullet)
							self.sb2.prep_ships()
						if not self.stats.multi_player:
							self.sb.prep_ships()	
							#清空余下的子弹
							alien.alienbullets.remove(alienbullet)
					if self.stats.ships_left==0 and not self.stats.multi_player:
						self.stats.game_active=False
						self.ship.set_invisible()
						pygame.mouse.set_visible(True)
					if self.stats.ships_left==0 and self.stats.multi_player:
						if self.stats.ships_left2==0:
							self.ship.set_invisible()
							self.ship2.set_invisible()		
							self.stats.game_active=False
							pygame.mouse.set_visible(True)
						if self.stats.ships_left2>0:
							self.ship.set_invisible()
				elif pygame.sprite.spritecollide(alienbullet, self.ship2_group, True):
				# 处理外星人子弹击中self.ship2的情况
					if self.stats.ships_left2>0:
						alien.alienbullets.remove(alienbullet)
						#将ship_left-1
						self.stats.ships_left2-=1
						self.sb2.prep_ships2()
						alien.alienbullets.remove(alienbullet)
					if self.stats.ships_left2==0 and self.stats.ships_left>0:
						self.ship2.set_invisible()
					if self.stats.ships_left==0 and self.stats.ships_left2==0:
						self.stats.game_active=False
						pygame.mouse.set_visible(True)
				if pygame.sprite.spritecollide(alienbullet, self.bullets, True):
						alien.alienbullets.remove(alienbullet)
						self.bullets.empty()
				if pygame.sprite.spritecollide(alienbullet, self.ship2.bullets, True):
						alien.alienbullets.remove(alienbullet)
						self.ship2.bullets.empty()
		self._check_bullet_alien_collisions()


	def _check_bullet_alien_collisions(self):
		"""检查是否有子弹射中了外星人，如果是，删除子弹和外星人"""
		collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
		collisions2 = pygame.sprite.groupcollide(self.ship2.bullets,self.aliens,True,True)



		if not self.aliens and self.stats.game_active and not self.stats.multi_player:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#提高等级：
			self.stats.level +=1
			self.sb.prep_level()
		if not self.aliens and self.stats.game_active and self.stats.multi_player:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#提高等级：
			self.stats.level +=1
			self.sb2.prep_level()
		if collisions and not self.stats.multi_player:
			self.stats.score+=self.settings.alien_points
			self.sb.prep_score()
			self.sb.check_high_score()
		if collisions and self.stats.multi_player:
			self.stats.score+=self.settings.alien_points
			self.sb2.prep_score()
			self.sb2.check_high_score2()
		if collisions2:
			self.stats.score+=self.settings.alien_points
			self.sb2.prep_score()
			self.sb2.check_high_score2()



	def _update_aliens(self):
		"""检查是否有外星人位于屏幕边缘"""
		"""更新外星人群中所有外星人的位置"""
		self._check_fleet_edges()
		self.aliens.update()


		if pygame.sprite.spritecollideany(self.ship,self.aliens) and self.stats.ships_active:
			self._ship_hit()
		if pygame.sprite.spritecollideany(self.ship2,self.aliens) and self.stats.ships_active2:
			self._ship_hit2()
		#检查是否有外星人到大屏幕的底端
		self._check_aliens_bottom()

	def _create_fleet(self):
		"""创建外星人群"""
		alien=Alien(self)
		alien_width,alien_height=alien.rect.size
		available_space_x=self.settings.screen_width-(alien_width)
		number_aliens_x=available_space_x // (2*alien_width)

		#计算屏幕可以容纳多少行外星人
		ship_height=self.ship.rect.height
		available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height)
		number_rows=available_space_y // (3*alien_height)

		#创建第一行外星人
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number,row_number)

	def _create_alien(self,alien_number,row_number):

			#创建一个外星人并将其加入当前行
			alien=Alien(self)
			alien_width,alien_height=alien.rect.size
			alien.x=alien_width+2*alien_width*alien_number
			alien.rect.x=alien.x
			alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
			self.aliens.add(alien)
  			
	def _update_screen(self):
		#每次循环都重绘屏幕
		background = pygame.image.load('images/bg.png')
		self.screen.blit(background, (0, 0))
		if self.stats.game_active and self.stats.multi_player:
			self.ship2.blitme()
			self.ship.blitme()
			self.sb2.show_score2()
		if self.stats.game_active and not self.stats.multi_player:
			self.ship.blitme()
			#显示得分
			self.sb.show_score()
		

		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		for bullet in self.ship2.bullets.sprites():
			bullet.draw_bullet()

		for alien in self.aliens:
			for alienbullet in alien.alienbullets.sprites():
				alienbullet.draw_alienbullet()

		self.aliens.draw(self.screen)

		for bonus in self.bonuses.sprites():
			bonus.blitme()
		for weaponbonus in self.weaponbonuses.sprites():
			weaponbonus.blitme()

		duration = 6
		if time.time() - self.last_width_change > duration:
			self.settings.bullet_width = 30


		if not self.stats.game_active:
			background = pygame.image.load('images/background.jpg')
			self.screen.blit(background, (0, 0))
			self.play_button.draw_button()
			self.play_button2.draw_button()
			self.help_button.draw_button()
			self.ship.set_invisible()
			self.aliens.empty()
			self.bullets.empty()
			pygame.mouse.set_visible(True)
			self.ship2.set_invisible()
			self.ship.set_invisible()
			self.stats.reset_stats()
			self.stats.multi_player=False

		#让最近绘制的屏幕可见
		pygame.display.flip()



	def _check_fleet_edges(self):
		"""有外星人达到边缘时采取响应的措施"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""将正群外星人下移，并改变他们的方向"""
		for alien in self.aliens.sprites():
			alien.rect.y+=self.settings.fleet_drop_speed
			alien.fire_bullet()
		self.settings.fleet_direction*=-1

	def _ship_hit(self):
		"""响应飞船被外星人撞到"""
		if self.stats.ships_left>0:
			#将ship_left-1
			self.stats.ships_left-=1
			if self.stats.multi_player:
				self.sb2.prep_ships()
			if not self.stats.multi_player:
				self.sb.prep_ships()	
			#清空余下的外星人和子弹

			self.aliens.empty()
			self.bullets.empty()

			#创建一群新的外星人，并且将飞船放到屏幕底端的中央
			self._create_fleet()
			self.ship.center_ship()
			#暂停
			sleep(0.5)
		if self.stats.ships_left==0 and not self.stats.multi_player:
			self.stats.game_active=False
			self.ship.set_invisible()
			pygame.mouse.set_visible(True)
		if self.stats.ships_left==0 and self.stats.multi_player:
			if self.stats.ships_left2==0:
				self.ship.set_invisible()
				self.ship2.set_invisible()		
				self.stats.game_active=False
				pygame.mouse.set_visible(True)
			if self.stats.ships_left2>0:
				self.ship.set_invisible()
	def _ship_hit2(self):
		"""响应飞船被外星人撞到"""
		if self.stats.ships_left2>0:
			#将ship_left-1
			self.stats.ships_left2-=1
			self.sb2.prep_ships2()
			#清空余下的外星人和子弹

			self.aliens.empty()
			self.bullets.empty()

			#创建一群新的外星人，并且将飞船放到屏幕底端的中央
			self._create_fleet()
			self.ship2.center_ship()
			#暂停
			sleep(0.5)
		if self.stats.ships_left2==0 and self.stats.ships_left>0:
			self.ship2.set_invisible()
		if self.stats.ships_left==0 and self.stats.ships_left2==0:
			self.stats.game_active=False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		"""检查是否有外星人到达了屏幕的底端"""
		screen_rect=self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom>=screen_rect.bottom:
				#结束游戏：
				self._ship_hit()
				self._ship_hit2()
				break

	def _update_bonus(self):
		"""更新所有bonus的位置，并删除已经消失的bonus."""
		self.bonuses.update()
		# Look for powerup-ship collisions.
		if pygame.sprite.spritecollideany(self.ship, self.bonuses):
			self._bonus_hit()
		if pygame.sprite.spritecollideany(self.ship2, self.bonuses):
			self._bonus_hit2()

    
	def _bonus_hit(self):
		"""与飞船1相撞"""
		if self.stats.ships_left<6:
			self.stats.ships_left+=1
		if not self.stats.multi_player:
			self.sb.prep_ships()
		if  self.stats.multi_player:
			self.sb2.prep_ships()
		self.bonuses.empty()
	def _bonus_hit2(self):
		"""与飞船2相撞"""
		if self.stats.ships_left2<6:
			self.stats.ships_left2+=1
		if self.stats.multi_player:
			self.sb2.prep_ships2()
		# Get rid of the powerup
		self.bonuses.empty()
	def _create_bonus(self):
		"""在屏幕上侧边缘随机生成bonus奖励."""
		self.bonus_counter += 1
		if self.bonus_counter >= self.bonus_limit:
			bonus = Bonus(self)
			bonus.rect.x = random.randint(0, self.settings.screen_width)
			bonus.rect.y = 0
			self.bonuses.add(bonus)
			self.bonus_counter = 0  # Reset the counter

	def _update_weaponbonus(self):
		"""更新所有bonus的位置，并删除已经消失的bonus."""
		self.weaponbonuses.update()
		# Look for powerup-ship collisions.
		if pygame.sprite.spritecollideany(self.ship, self.weaponbonuses):
			self._weaponbonus_hit()
		if pygame.sprite.spritecollideany(self.ship2, self.weaponbonuses):
			self._weaponbonus_hit()

    
	def _weaponbonus_hit(self):
		"""吃到武器奖励后子弹强化6秒"""
		default_width=15
		if self.settings.bullet_width<60:
			self.settings.bullet_width*=2
			self.last_width_change= time.time()
			self.weaponbonuses.empty()
	def _create_weaponbonus(self):
		"""在屏幕上侧边缘随机生成bonus奖励."""
		self.weaponbonus_counter += 1
		if self.weaponbonus_counter >= self.weaponbonus_limit:
			weaponbonus = Weaponbonus(self)
			weaponbonus.rect.x = random.randint(0, self.settings.screen_width)
			weaponbonus.rect.y = 0
			self.weaponbonuses.add(weaponbonus)
			self.weaponbonus_counter = 0  # Reset the counter



class HelpDialog:
		'''帮助对话框'''
		def __init__(self):
			pygame.init()
			self.settings=Settings()
			self.background = pygame.image.load('images/bg.png')
			# 创建屏幕对象
			self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
			#初始化对话框界面
			self.font=pygame.font.SysFont(None,36)
			self.text1 = self.font.render("Developed by ZhaoLu(20203970) in CSUFT", True, (255, 255, 255))
			self.text2 = self.font.render("1p:Use the arrow keys", True, (255, 255, 255))
			self.text3 = self.font.render("2p:Use A D and space Key", True, (255, 255, 255))
			self.text4 = self.font.render("Shoot down all the aliens to win the game",True, (255, 255, 255))
			self.text5 = self.font.render("Press any key to continue", True, (255, 255, 255))
			self.window_color = (37, 33, 57)
			self.text_color = (255, 255, 255)
		def show(self):
			text1_rect = self.text1.get_rect()
			text2_rect = self.text2.get_rect()
			text3_rect = self.text3.get_rect()
			text4_rect = self.text3.get_rect()
			text5_rect = self.text3.get_rect()

			# 设置文本的中心位置为屏幕的中心位置
			text1_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 - 120)
			text2_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 - 60)
			text3_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 )
			text4_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 + 60)
			text5_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 + 120)
        # 计算每个文本中心位置的横向偏移量，将其与屏幕中心对齐
			text1_offset = self.text1.get_width() // 100
			text2_offset = self.text2.get_width() // 30
			text3_offset = self.text3.get_width() // 30
			text4_offset = self.text4.get_width() // 5
			text5_offset = self.text5.get_width() // 30
			text1_rect.centerx = self.settings.screen_width // 2 - text1_offset
			text2_rect.centerx = self.settings.screen_width // 2 - text2_offset
			text3_rect.centerx = self.settings.screen_width // 2 - text3_offset
			text4_rect.centerx = self.settings.screen_width // 2 - text4_offset
			text5_rect.centerx = self.settings.screen_width // 2 - text5_offset

			#显示对话框：
			self.screen.blit(self.background,(0,0))
			pygame.display.set_caption("Help")
			self.screen.blit(self.text1, text1_rect)
			self.screen.blit(self.text2, text2_rect)
			self.screen.blit(self.text3, text3_rect)
			self.screen.blit(self.text4, text4_rect)
			self.screen.blit(self.text5, text5_rect)
			pygame.display.update()
			
			# 监听用户事件
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
						pygame.display.set_caption("Alien Invasion")
						return


if __name__=='__main__':
	#创建游戏实例并运行游戏
	ai = AlienInvasion()
	ai.run_game()