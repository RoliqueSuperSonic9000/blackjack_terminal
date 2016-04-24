#TODO: Create abstracted 'player' class for both player and dealer to extend
"""
# Player Class
"""
from random import randint
class BotPlayer(object):
	# Class Variables
	name_list = ['Whoop','Muffin','Poop','Fartface','Daipy','Turd','Cake','Skunk']
	strategies = {1: 'Stand on 12 or Greater', 2: 'Stand on 17 or greater'}
	DEFAULT = 1
	# constructor
	def __init__(self, c, t):
		name = BotPlayer.name_list[randint(0,len(BotPlayer.name_list) - 1)]
		self._name = name
		self._cash = c
		self._type = t
		self._strategy = BotPlayer.strategies[BotPlayer.DEFAULT]
		self._hand = []
		self._score = 0
		self._bet = 0
		self._split = False
		self._surrender = False
		self._insurance = False
		self._insurance_bet = 0
		self._blackjack = False
		self._hit_count = 0
		
	@property
	def hit_count(self):
		return self._hit_count
		
	@hit_count.setter
	def hit_count(self, h):
		self._hit_count = h
		
	@property
	def strategy(self):
		return self._strategy
		
	@strategy.setter
	def strategy(self, s):
		self._strategy = s
	
	@property
	def type(self):
		return self._type
		
	@type.setter
	def type(self, t):
		self._type = t
	
	@property
	def blackjack(self):
		return self._blackjack
	
	@blackjack.setter
	def blackjack(self, b):
		self._blackjack = b
		
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
	
	# receive card
	def receive_card(self, card):
		self.hand.append(card)
	
	#reset cards
	def reset(self):
		self.hand = []
		self.score = 0
		self.bet = 0
		self.split = False
		self.surrender = False
		self.insurance = False
		self.insurance_bet = 0
		self.blackjack = False
		self.hit_count = 0
			
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
	
	def lose(self):
		print("{n} loses.".format(n = self.name))
		self.cash = self.cash - self.bet
	
	def win(self):
		print("{n} wins!".format(n = self.name))
		self.cash = self.cash + self.bet
	
	def tie(self):
		print("{n} ties.".format(n = self.name))
		self.cash = self.cash

	def blackjack_win(self):
		print("Player Blackjack!")
		self.cash = self.cash + self.bet + (self.bet * 1.5)
		
	# output useful information to the console
	def show_info(self):
		tick = '-'
		print(tick*20)
		print("Name: {n}".format(n = self.name))
		print("Cash: {c}".format(c = self.cash - self.bet))
		print("Bet:  {b}".format(b = self.bet))
		print("Hand: {h}".format(h = [card.display for card in self.hand])) #TODO format hand better
		print("Count: {c}".format(c = self.get_score()))
		print(tick*20)

	# output minimized info
	def quick_show(self):
		print("{n}: {h}: {c}".format(n = self.name, h = [card.display for card in self.hand], c = self.get_score()))
		
	
	# hit or stand
	def hit(self):
		self.get_score()
		if self.score < 17:
			return True
		else:
			return False