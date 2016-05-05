from random import randint
"""
# Dealer Class
"""
# TODO: Allow dealer to play by different house rules
class Dealer(object):

	name_list = ['Paul','George','John','Ringo']

	def __init__(self, h):
		name = Dealer.name_list[randint(0,len(Dealer.name_list) - 1)]
		self._name = name
		self._hand = []
		self._cash = 0
		self._score = 0
		self._house = h
		self._blackjack = False

	@property
	def blackjack(self):
		return self._blackjack

	@blackjack.setter
	def blackjack(self, b):
		self._blackjack = b

	@property
	def house(self):
		return self._house

	@house.setter
	def house(self, h):
		self._house = h

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, n):
		self._name = n

	@property
	def cash(self):
		return self._cash

	@cash.setter
	def cash(self, c):
		self._cash = c

	@property
	def hand(self):
		return self._hand

	@hand.setter
	def hand(self, h):
		self._hand = h

	@property
	def score(self):
		return self._score

	@score.setter
	def score(self, s):
		self._score = s

	def greeting(self):
		""" Print Dealer greeting to console."""
		star ='*'
		print(star*50)
		print("Hello I'm your dealer {name} \nLet's Play Blackjack!"\
												.format(name = self.name))
		print(star*50)

	def receive_card(self, card):
		""" Add a card to current hand."""
		self.hand.append(card)

	def reset(self):
		""" Reset round based variables, called after each round."""
		self.hand = []
		self._score = 0
		self._blackjack = False

	def check_bust(self):
		""" Check if current score is greater than 21."""
		self.score = 0
		ace = False
		for card in self.hand:
			if card.value == 11:
				ace = True
			self.score = self.score + card.value
			if self.score > 21:
				if ace == True:
					self.score = self.score - 10
					ace = False
				else:
					return True
		return False

	def get_score(self):
		""" Calculate score of current hand."""
		self.score = 0
		ace = False
		for card in self.hand:
			if card.value == 11:
				ace = True
			self.score = self.score + card.value
			if self.score > 21:
				if ace == True:
					self.score = self.score - 10
					ace = False
		return self.score

	def show_info(self):
		""" Output hand info to the console."""
		tick = '-'
		print(tick*20)
		print("Name: {n} (Dealer)".format(n = self.name))
		print("Hand: {h}".format(h = [card.display for card in self.hand]))
		print("Count: {c}".format(c = self.get_score()))
		print(tick*20)

	def quick_show(self):
		""" Output hand info to the console in a shorthand way."""
		print("{n}: {h}: {c}".format(
								n = self.name,
								h = [card.display for card in self.hand],
								c = self.get_score()
								)
							)

	def show_card(self):
		""" Output dealer's 'up' card to the console."""
		print"Dealer: {h}, hidden card".format(h = self.hand[0].display)

	def highest(self, players):
		# This is not used! Not how blackjack is played
		""" Check if dealer has higher score than all players."""
		for player in players:
			if player.get_score() > self.get_score():
				return False
		return True

	def check_hit(self):
		""" Check if score is less than 17."""
		self.get_score()
		if self.score < 17:
			return True
		else:
			return False
