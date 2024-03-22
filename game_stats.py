class GameStats:
	"""跟踪游戏的统计信息"""

	def __init__(self,ai_game):
		"""初始化统计信息"""
		self.settings=ai_game.settings	
		self.reset_stats()
		#任何情况下最高得分都是0分
		self.high_score=0
		self.high_score2=0

		#让游戏一开始处于非活动状态
		self.game_active = False
		self.multi_player = False


	def reset_stats(self):
		"""初始化游戏运行期间可能发生的变化统计"""
		self.ships_left=self.settings.ship_limit
		self.ships_left2=self.settings.ship_limit2
		self.ships_active=True
		self.ships_active2=True
		self.score=0
		#设置玩家的等级
		self.level=1
		self.level2=1