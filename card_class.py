"""
Card Class
"""
class Card(object):
	
	suits  = ['Clubs','Diamonds','Hearts','Spades']
	
	#ranks = ['2','3','4','5','6','7','8','9','10','JACK','QUEEN','KING','ACE']
	ranks = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10, 'JACK':10,'QUEEN':10,'KING':10,'ACE':11}
	def __init__(self, suit, rank):
		self._suit = suit
		self._rank = rank
		self._name = str(rank) + " " + str(suit)
		self._value = Card.ranks[self._rank]
		"""
		# This was used when ranks was a list
		if self._rank in ['JACK','QUEEN','KING']:
			self._value = 10
		elif self._rank == 'ACE':
			self._value = 11
		else:
			self._value = str(self._rank)
		"""
		self._display = self._rank + self._suit
		
	@property
	def name(self):
		return self._name
		
	@name.setter
	def name(self, n):
		self._name = n
		
	@property
	def suit(self):
		return self._suit
		
	@suit.setter
	def suit(self, s):
		self._suit = s
	
	@property
	def value(self):
		return self._value
		
	@value.setter
	def value(self, v):
		self._value = v
		
	@property
	def display(self):
		return self._display

	@display.setter
	def display(self, d):
		self._display = d