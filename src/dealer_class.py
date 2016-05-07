from random import randint

from player_class import Player
"""
Dealer Class
"""
class Dealer(Player):

	def __init__(self, n, c, t, h):
		Player.__init__(self, n, c, t)
		self._house = h

	@property
	def house(self):
		return self._house

	@house.setter
	def house(self, h):
		self._house = h

	def greeting(self):
		""" Print Dealer greeting to console."""
		star ='*'
		print(star*50)
		print("Hello I'm your dealer {name} \nLet's Play Blackjack!"\
												.format(name = self.name))
		print(star*50)

	def show_card(self):
		""" Output dealer's 'up' card to the console."""
		print"Dealer: {h}, hidden card".format(h = self.hand[0].display)

	def highest(self, players):# This is not used! Not how blackjack is played
		""" Check if dealer has higher score than all players."""
		for player in players:
			if player.get_score() > self.get_score():
				return False
		return True

	def stand_on_all_17(self):
		""" Dealer stands on any hand that is 17."""
		if self.score < 17:
			return True
		else:
			return False

	def hit_on_soft_17(self):
		""" Dealer hits on hands that are 17 if has an Ace in hand."""
		if self.score < 17:
			return True
		elif self.score == 17:
			for card in self.hand:
				if card.value == 11:
					return True
		else:
			return False

	def check_hit(self):
		""" Decide to hit or stay based on house rules. """
		self.get_score()
		if self.house == 1:
			return self.stand_on_all_17()
		elif self.house == 2:
			return self.hit_on_soft_17()
		else:
			return False # place holder for now
