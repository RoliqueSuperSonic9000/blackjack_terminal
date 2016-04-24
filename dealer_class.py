from random import randint
"""
# Dealer Class
"""
# TODO: Allow dealer to play by different house rules
class Dealer(object):

	#Class Variables
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
	
	# dealer says statement to start the game
	def greeting(self):
		star ='*'
		print(star*50)
		print("Hello I'm your dealer {name} \nLet's Play Blackjack!".format(name = self.name))
		print(star*50)
	
	# receive card
	def receive_card(self, card):
		self.hand.append(card)
	
	#reset cards
	def reset(self):
		self.hand = []
		self._score = 0
		self._blackjack = False	
		
	# check if player has gone over 21
	def check_bust(self):
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
	
	# count card current cards score
	def get_score(self):
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
	
	# output relavant information to the console
	def show_info(self):
		tick = '-'
		print(tick*20)
		print("Name: {n} (Dealer)".format(n = self.name))
		print("Hand: {h}".format(h = [card.display for card in self.hand]))
		print("Count: {c}".format(c = self.get_score()))
		print(tick*20)

	# output minimized info
	def quick_show(self):
		print("{n}: {h}: {c}".format(n = self.name, h = [card.display for card in self.hand], c = self.get_score()))
		
	# show only one card
	def show_card(self):
		print"Dealer: {h}, hidden card".format(h = self.hand[0].display)
	
	# dealer decide to hit or stand
	def highest(self, players):
		for player in players:
			if player.get_score() > self.get_score():
				return False
		return True
	
	# stands on anything 17 and over
	def check_hit(self):
		self.get_score()
		if self.score < 17:
			return True
		else:
			return False