"""
# Bot Player Class
"""
from random import randint

from base_player_class import Player
class BotPlayer(Player):

	strategies = {1: 'Stand on 12 or Greater', 2: 'Stand on 17 or greater'}
	DEFAULT = 1

	def __init__(self, c, t):
		self._name = BasePlayer.name_list[randint(0,len(BotPlayer.name_list) - 1)]
		self._strategy = BotPlayer.strategies[BotPlayer.DEFAULT]

	def hit(self):
		""" Check whether to hit or stay."""
		self.get_score()
		if self.score < 17:
			return True
		else:
			return False
