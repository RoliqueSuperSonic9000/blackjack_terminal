#TODO: Create abstracted 'player' class for both player and dealer to extend
"""
# Player Class
"""
from random import randint

class Player(object):

	# Global var list
	name_list = ['Muffin','Poop','Fartface','Daipy','Turd','Cake','Skunk']

	def __init__(self, n, c):
		if n == "":
			name = Player.name_list[randint(0,len(Player.name_list) - 1)]
			self._name = name
		else:
			self._name = n
		self._cash = c
		self._hand = []
		self._score = 0
		self._bet = 0
		self._split = False
		self.split_score = []
		self._surrender = False
		self._insurance = False
		self._insurance_bet = 0
	
	@property
	def insurance_bet(self):
		return self._insurance_bet
		
	@insurance_bet.setter
	def insurance_bet(self, i):
		self._insurance_bet = i
	
	@property
	def insurance(self):
		return self._insurance
	
	@insurance.setter
	def insurance(self, i):
		self._insurance = i
		
	@property
	def surrender(self):
		return self._surrender
		
	@surrender.setter
	def surrender(self, s):
		self._surrender = s
	
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
	
	@property
	def split(self):
		return self._split
	
	@split.setter
	def split(self, s):
		self._split = s
	
	# count score of cards
	def get_score(self):
		self.score = 0
		ace = False
		for card in self.hand:
			if card.value == 11:
				ace = True
			self.score = self.score + card.value
			if self.score > 21:
				if ace:
					self.score = self.score - 10
					ace = False
		return self.score
	
	def get_split_score(self):
		self.split_score = []
		sum = 0
		ace1 = False
		for card in self.hand[0]:
			if card.value == 11:
				ace1 = True
			sum = sum + card.value
			if sum > 21:
				if ace1:
					sum = sum - 10
					ace1 = False
		self.split_score.append(sum)
		sum = 0
		ace2 = False
		for card in self.hand[1]:
			if card.value == 11:
				ace2 = True
			sum = sum + card.value
			if sum > 21:
				if ace2:
					sum = sum - 10
					ace2 = False
		self.split_score.append(sum)
		return self.split_score
		
	# receive card
	def receive_card(self, card):
		self.hand.append(card)
	
	# receive card two
	def split_receive_cards(self, card1, card2):
		self.hand[0].append(card1)
		self.hand[1].append(card2)
	
	#reset cards
	def reset_hand(self):
		self.hand = []
	
	# untested with aces
	# check if player has gone over 21
	# this is essentially the same as get_score().... need change
	def check_bust(self):
		sum = 0
		ace = False
		for card in self.hand:
			if card.value == 11:
				ace = True
			sum = sum + card.value
			if sum > 21:
				if ace:
					sum = sum - 10
					ace = False
				else:
					return True
		return False
	
	def split_hand(self):
		self.hand = [[self.hand[0]], [self.hand[1]]]
		return self.hand

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
	
	# This needs to be fixed
	def split_show(self):
		hand1 = self.hand[0]
		hand2 = self.hand[1]
		print('-'*30)
		print("Hand 1")
		print("{n}: {h}: {c}".format(n = self.name, h = [card.display for card in hand1], c = self.get_split_score()[0]))
		print("Hand 2")
		print("{n}: {h}: {c}".format(n = self.name, h = [card.display for card in hand2], c = self.get_split_score()[1]))
		print('-'*30)