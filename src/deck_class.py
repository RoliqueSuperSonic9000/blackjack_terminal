
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

	def shuffle(self):
		""" Shuffle cards using Fisher-Yates shuffle."""
		n = len(self.cards)
		for i in range(n - 1, 0, -1):
			j = randint(0, i)
			if i == j:
				continue
			self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

	def deal_card(self):
		""" Remove top card from the deck."""
		return self.cards.pop(0)

	def new_deck(self):
		""" Create a new deck and shuffle."""
		self.cards = []
		for suit in Card.suits:
			for rank in Card.ranks:
				card = Card(suit, rank)
				self._cards.append(card)
		self.shuffle()
		return self.cards
