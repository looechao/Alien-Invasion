class Settings:
	#存储游戏中所有设置的类

	def __init__(self):

		"""初始化游戏的静态设置"""
		#屏幕设置
		self.screen_width=900
		self.screen_height=800
		self.bg_color=(0,0,0)

		#飞船设置
		self.ship_limit=3
		self.ship_limit2=3

		#bullet settings
		self.bullets_allowed = 3
		self.bullets_allowed2 = 3
		self.bullet_width=30
		self.bullet_height=1
		self.bullet_color=(138,43,226)

		#alien settings
		self.fleet_drop_speed=8
		self.alien_fire_rate=9
		self.alienbullet_width=4
		self.alienbullet_height=50
		self.alienbullet_speed=20
		self.alienbullet_color=(255,20,147)		
		#加快游戏节奏的速度
		self.speedup_scale=1.5

		#奖励设置
		self.bonus_speed=5
		self.weaponbonus_speed=10

		self.initialize_dynamic_settings()


	def initialize_dynamic_settings(self):
		#积分
		self.alien_points=800

		"""初始化随游戏进行而变化的设置"""
		self.ship_speed = 5
		self.bullet_speed=3.0
		self.alien_speed=1.5
		self.bullet_width=30

		#fleetdirection 1右 -1左
		self.fleet_direction=1

		

	def increase_speed(self):
		"""提高速度设置"""
		self.ship_speed*=1.002
		self.bullet_speed*=1.002
		self.alien_speed*=self.speedup_scale