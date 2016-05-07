"""
Bot Player Class
"""
#TODO create a place bet function
from random import randint

from player_class import Player

class BotPlayer(Player):

	#strategies = {1: 'Stand on 12 or Greater', 2: 'Stand on 17 or greater'}

	strategies = [1, 2, 3]
	strategy_names =[
						"Stand on all 12 or greater",
						"Stand on all 17 or greater",
						"Hit on soft 17"
					]

	def __init__(self, n, c, t, s=None):
		Player.__init__(self, n, c, t)
		if s is not None:
			self._strategy = s
		else:
			self._strategy = BotPlayer \
								.strategies \
								[randint(0, len(BotPlayer.strategies)-1)]
		self._strategy_name = BotPlayer.strategy_names[self.strategy-1]

	@property
	def strategy(self):
		return self._strategy

	@strategy.setter
	def strategy(self):
		self._strategy = s

	@property
	def strategy_name(self):
		return self._strategy_name

	def next_move(self):
		""" Return a string of what the bots next move is."""
		if self.hand:
			if self.hit():
				return "Hit"
			else:
				return "Stand"
		else:
			return "Bet"

	def show_info(self):
		""" Print useful player information to the console."""
		tick = '-'
		print(tick*20)
		print("Name: {n}".format(n = self.name))
		print("Cash: {c}".format(c = self.cash - self.bet))
		print("Bet:  {b}".format(b = self.bet))
		print("Hand: {h}".format(h = [card.display for card in self.hand]))
		print("Count: {c}".format(c = self.get_score()))
		print("Strategy: {s}".format(s = self.strategy_name))
		print("Next Move: {m}".format(m = self.next_move()))
		print(tick*20)

	def stand_on_all_12(self):
		""" Bot will hit only if hand is less than 12."""
		if self.score < 12:
			return True
		else:
			return False

	def stand_on_all_17(self):
		""" Bot will hit only if hand is less than 17."""
		if self.score < 17:
			return True
		else:
			return False

	def hit_on_soft_17(self):
		""" Bot will hit if score is less than 17 or 17 with an ace."""
		if self.score < 17:
			return True
		elif self.score == 17:
			for card in self.hand:
				if card.value == 11:
					return True
		else:
			return False

	def hit(self):
		""" Check whether to hit or stay."""
		self.get_score()
		if self.strategy == 1:
			return self.stand_on_all_12()
		elif self.strategy == 2:
			return self.stand_on_all_17()
		elif self.strategy == 3:
			return self.hit_on_soft_17()
		else:
			return False # place holder for now
