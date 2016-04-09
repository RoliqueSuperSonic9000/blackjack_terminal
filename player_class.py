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
		self._cards = []
	
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
	def cards(self):
		return self._cards
	
	@cards.setter
	def cards(self, s):
		self._cards = s
	
	# receive card
	def receive_card(self, card):
		self.cards.append(card)
	
	#reset cards
	def reset_cards(self):
		self.cards = []
	
	# check if player has gone over 21
	def check_bust(self):
		sum = 0
		for card in self.cards:
			sum = sum + card
			if sum > 21:
				return True
		return False
	
	# count score of cards
	def get_score(self):
		score = 0
		for card in self.cards:
			score = score + card
		return score
			
	# output useful information to the console
	def show_info(self):
		tick = '-'
		print(tick*20)
		print("Name: {n}".format(n = self.name))
		print("Cash: {c}".format(c = self.cash))
		print("Hand: {h}".format(h = self.cards)) #TODO format hand better
		print("Count: {c}".format(c = self.get_score()))
		print(tick*20)
