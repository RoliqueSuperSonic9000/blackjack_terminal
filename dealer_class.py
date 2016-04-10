from random import randint
"""
# Dealer Class
"""
# TODO: decision making dealer
class Dealer(object):

	# constructor
	def __init__(self):
		# initialize	
		random_names = ['Paul','George','John','Ringo']
		name = random_names[randint(0,len(random_names) - 1)]
		self._name = name
		self._hand = []
		self._cash = 0
		self._score = 0
		
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
	
	# count card current cards score
	def get_score(self):
		self.score = 0
		for card in self.hand:
			self.score = self.score + card.value
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
		
	# dealer decide to hit or stand
	def highest(self, players):
		for player in players:
			if player.get_score() > self.get_score():
				return False
		return True
	
	# hit or stand. return True for hit, False for stand
	def hit(self):
		soft = False
		for card in self.hand:
			if card.value == 11:
				soft = True
				break
		if self.get_score() < 17 and not soft:
			return True
		else:
			return False