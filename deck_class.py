
from card_class import Card
from random import randint
"""
Deck Class
"""
class Deck(object):
	
	def __init__(self, u_id):
		self._unique_id = u_id
		self._cards = []
		for suit in Card.suits:
			for rank in Card.ranks:
				card = Card(suit, rank)
				self._cards.append(card)
		
	@property
	def unique_id(self):
		return self._unique_id
		
	@unique_id.setter
	def unique_id(self, u):
		self._unique_id = u
	
	@property
	def cards(self):
		return self._cards
		
	@cards.setter
	def cards(self, c):
		self._cards = c
	
	# fisher yates shuffle
	def shuffle(self):
		n = len(self.cards)
		for i in range(n - 1, 0, -1):
			j = randint(0, i)
			if i == j:
				continue
			temp = self.cards[i]
			self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
	
	def deal_card(self):
		return self.cards.pop(0)