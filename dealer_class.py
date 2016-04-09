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
		self._cards = []
		self._cash = 0
		
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
	
	# dealer says statement to start the game
	def greeting(self):
		star ='*'
		print(star*50)
		print("Hello I'm your dealer {name} \nLet's Play Blackjack!".format(name = self.name))
		print(star*50)
	
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
	
	# count card current cards score
	def get_score(self):
		score = 0
		for card in self.cards:
			score = score + card
		return score
		
	# output relavant information to the console
	def show_info(self):
		tick = '-'
		print(tick*20)
		print("Name: {n} (Dealer)".format(n = self.name))
		print("Hand: {h}".format(h = self.cards))
		print("Count: {c}".format(c = self.get_score()))
		print(tick*20)
