#TODO: Create abstracted 'player' class for both player and dealer to extend
"""
# Player Class
"""
from random import randint

class Player(object):

	# constructor
	def __init__(self, n, c):
		random_name_list = ['Muffin','Poop','Fartface','Daipy','Turd','Cake','Skunk']
		if n == "":
			name = random_name_list[randint(0,len(random_name_list) - 1)]
			self._name = name
		else:
			self._name = n
		self._cash = c
		self._hand = []
		self._score = 0
		self._bet = 0
	
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

	@property
	def bet(self):
		return self._bet
		
	@bet.setter
	def bet(self, b):
		self._bet = b
		
	# count score of cards
	def get_score(self):
		self.score = 0
		for card in self.hand:
			self.score = self.score + card.value
		return self.score
	
	# receive card
	def receive_card(self, card):
		self.hand.append(card)
	
	#reset cards
	def reset_hand(self):
		self.hand = []
	
	# check if player has gone over 21
	def check_bust(self):
		sum = 0
		for card in self.hand:
			sum = sum + card.value
			if sum > 21:
				return True
		return False
	
	def lose(self):
		print("{n} loses.".format(n = self.name))
		self.cash = self.cash - self.bet
	
	def win(self):
		print("{n} wins!".format(n = self.name))
		self.cash = self.cash + self.bet
	
	def tie(self):
		print("{n} ties.".format(n = self.name))
		self.cash = self.cash

	# output useful information to the console
	def show_info(self):
		tick = '-'
		print(tick*20)
		print("Name: {n}".format(n = self.name))
		print("Cash: {c}".format(c = self.cash))
		print("Hand: {h}".format(h = [card.display for card in self.hand])) #TODO format hand better
		print("Count: {c}".format(c = self.get_score()))
		print(tick*20)

	# output minimized info
	def quick_show(self):
		print("{n}: {h}: {c}".format(n = self.name, h = [card.display for card in self.hand], c = self.get_score()))