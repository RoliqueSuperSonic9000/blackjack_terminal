from random import randint
from colorama import init, Fore, Back, Style

"""
Player Class
"""
class Player:

	name_list = [
		'Muffin','Poop','Fartface',
		'Daipy','Turd','Cake',
		'Skunk','Paul','George',
		'John','Ringo'
	]

	def __init__(self, n, c, t, tbl_min, tbl_max):
		if n == "":
			self._name = Player.name_list\
				[randint(0,len(Player.name_list) - 1)]
		else:
			self._name = n
		self._cash = c
		self._start_cash = c
		self._type = t
		self._hand = []
		self._score = 0
		self._bet = 0
		self._split = False
		self._split_bet = []
		self._split_score = []
		self._split_surrender = [False, False]
		self._surrender = False
		self._insurance = False
		self._insurance_bet = 0
		self._blackjack = False
		self._hit_count = 0
		self._split_hit_count = [0,0]
		self._outcome = 'None'
		self._min_bet = tbl_min
		self._max_bet = tbl_max
		self._round_bet_history = []
		self._round_outcome_history = []
		self._round_cash_history = []
		self._highest_cash = c
		self._highest_bet = 0

	@property
	def start_cash(self):
		return self._start_cash

	@start_cash.setter
	def start_cash(self, c):
		self._start_cash = c

	@property
	def outcome(self):
		return self._outcome

	@outcome.setter
	def outcome(self, o):
		self._outcome = o

	@property
	def split_hit_count(self):
		return self._split_hit_count

	@split_hit_count.setter
	def split_hit_count(self, s):
		self._split_hit_count = s

	@property
	def hit_count(self):
		return self._hit_count

	@hit_count.setter
	def hit_count(self, h):
		self._hit_count = h

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
	def split_score(self):
		return self._split_score

	@split_score.setter
	def split_score(self, s):
		self._split_score = s

	@property
	def split_bet(self):
		return self._split_bet

	@split_bet.setter
	def split_bet(self, s):
		self._split_bet = s

	@property
	def split_surrender(self):
		return self._split_surrender

	@split_surrender.setter
	def split_surrender(self, s):
		self._split_surrender = s

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
	@property
	def min_bet(self):
		return self._min_bet

	@property
	def max_bet(self):
		return self._max_bet

	@property
	def round_bet_history(self):
		return self._round_bet_history

	@round_bet_history.setter
	def round_bet_history(self, b):
		self._round_bet_history = b

	@property
	def round_outcome_history(self):
		return self._round_outcome_history

	@round_outcome_history.setter
	def round_outcome_history(self, o):
		self._round_outcome_history = o

	@property
	def round_cash_history(self):
		return self._round_cash_history

	@round_cash_history.setter
	def round_cash_history(self, c):
		self._round_cash_history = c

	def highest_bet(self):
		""" Go through round history, find highest bet and return it."""
		maximum = 0
		for bet in self.round_bet_history:
			if bet > maximum:
				maximum = bet
		self._highest_bet = maximum
		return self._highest_bet

	def highest_cash(self):
		""" Go through round history, find highest cash, return it."""
		maximum = 0
		for cash in self.round_cash_history:
			if cash > maximum:
				maximum = cash
		self._highest_cash = maximum
		return self._highest_cash

	def out_of_money(self):
		""" Find highest cash and bet when a player is out of money."""
		self.highest_cash()
		self.highest_bet()

	def end_game_stats(self):
		""" Print out post game statistics to the console."""
		print("-"*25)
		print("{n}:".format(n = self.name))
		print("Rounds played: {r}".format(r = len(self.round_bet_history)))
		print("Highest Bet made: {b}".format(b = self.highest_bet()))
		print("Highest Cash: {c}".format(c = self.highest_cash()))
		print("-"*25)

	def place_bet(self, b):
		""" Player place a bet."""
		self.bet = b

	def double_down(self):
		""" Double this player's bet."""
		print("Double down!")
		print("{n}'s bet is now: {b}".format(n = self.name, b = self.bet))
		self.bet = self.bet * 2

	"""REWRITTEN BELOW
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
	"""
	def get_score(self):
		""" Calculate and return score of current hand."""
		score = 0
		high_ace_count = 0
		for card in self.hand:
			if card.value == 11:
				high_ace_count = high_ace_count + 1
			score = score + card.value
		while high_ace_count > 0 and score > 21:
			for card in self.hand:
				if card.value == 11:
					card.value = 1
					high_ace_count = high_ace_count - 1
				score = score - 10
				if score <= 21:
					break
		self.score = score
		return self.score

	def get_split_score(self):
		""" Calculate and return both scores for split hands."""
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

	def receive_card(self, card):
		""" Add a card to the player's hand."""
		self.hand.append(card)

	def split_receive_cards(self, card1, card2):
		""" Add a card to each of the player's hands."""
		self.hand[0].append(card1)
		self.hand[1].append(card2)

	def reset(self):
		""" Reset variables that need to be reset each round."""
		self.hand = []
		self.insurance = False
		self.surrender = False
		self.split = False
		self.split_score = []
		self.score = 0
		self.bet = 0
		self.split_bet = []
		self.split_surrender = [False, False]
		self.insurance_bet = 0
		self.blackjack = False
		self.hit_count = 0
		self.split_hit_count = [0,0]
		self.outcome = "None"

	def check_bust(self):
		""" Check if the player's hand is over 21. Return boolean."""
		sum = 0
		ace = False
		for card in self.hand:
			if card.value == 11:
				ace = True
			sum = sum + card.value
			if sum > 21: # TODO: change value of that ace
				if ace:
					sum = sum - 10
					ace = False
				else:
					return True
		return False

	def split_hand(self):
		""" Split the player's hand into an array of two hands."""
		self.hand = [[self.hand[0]], [self.hand[1]]]
		return self.hand

	def add_round(self, o, b, c):
		""" Add round history to corresponding lists."""
		self.round_outcome_history.append(o)
		self.round_bet_history.append(b)
		self.round_cash_history.append(c)

	def lose(self):
		""" Subtract the player's bet from the player's cash total."""
		print(Fore.RED + "{n} loses.".format(n = self.name))
		print(Fore.WHITE)
		self.cash = self.cash - self.bet
		self.outcome = "Lose"
		self.add_round(self.outcome, self.bet, self.cash)

	def win(self):
		""" Add the player's bet to the player's cash total."""
		print(Fore.GREEN + "{n} wins!".format(n = self.name))
		print(Fore.WHITE)
		self.cash = self.cash + self.bet
		self.outcome = "Win"
		self.add_round(self.outcome, self.bet, self.cash)

	def tie(self):
		""" Alert the player they have tied the dealer."""
		print(Fore.BLUE + "{n} ties.".format(n = self.name))
		print(Fore.WHITE)
		self.outcome = "Tie"
		self.add_round(self.outcome, self.bet, self.cash)

	def blackjack_win(self):
		""" Add the players bet plus 1/2 bet to the player's cash total."""
		print("{n} Blackjack!".format(n = self.name))
		self.cash = self.cash + (self.bet * 1.5)
		self.outcome = "Win"
		self.add_round(self.outcome, self.bet, self.cash)

	def insurance_lose(self):
		""" Subtract player's insurance bet from cash."""
		print("{n} loses insurance money -> Dealer does not have blackjack"\
												.format(n = player.name))
		self.cash = self.cash - self.insurance_bet

	def insurance_win(self):
		""" Add a player's insurance bet to cash."""
		print("{n} Insurance pays off!".format(n = player.name))
		self.cash = self.cash + self.insurance_bet

	def show_info(self):
		""" Print useful player information to the console."""
		tick = '-'
		print(tick*20)
		print("Name: {n}".format(n = self.name))
		print("Cash: {c}".format(c = self.cash - self.bet))
		print("Bet:  {b}".format(b = self.bet))
		print("Hand: {h}".format(h = [card.display for card in self.hand]))
		print("Count: {c}".format(c = self.get_score()))
		print(tick*20)

	def quick_show(self):
		""" Print Hand and score information in one line to the console."""
		print("{n}: {h}: {c}".format(
								n = self.name,
								h = [card.display for card in self.hand],
								c = self.get_score())
								)

	def split_show(self):
		""" Print info to console in the case where the player split."""
		hand1 = self.hand[0]
		hand2 = self.hand[1]
		print('-'*30)
		print("Cash: {c}".format(c = self.cash
									- self.split_bet[0]
									- self.split_bet[1])
								)
		print("Hand 1")
		if self.get_split_score()[0] < 22:
			print("{n}: {h}: {c}".format(n = self.name,
										h = [card.display for card in hand1],
										c = self.get_split_score()[0])
										)
		else:
			print("{n}: {h}: {c}: BUSTED!"\
									.format(
										n = self.name,
										h = [card.display for card in hand1],
										c = self.get_split_score()[0])
										)
		print("Hand 1 bet: {b}".format(b = self.split_bet[0]))
		print("Hand 2")
		if self.get_split_score()[1] < 22:
			print("{n}: {h}: {c}".format(
										n = self.name,
										h = [card.display for card in hand1],
										c = self.get_split_score()[1])
										)
		else:
			print("{n}: {h}: {c} -> BUSTED!"\
									.format(
										n = self.name,
										h = [card.display for card in hand1],
										c = self.get_split_score()[1])
										)
		print("Hand 2 bet: {b}".format(b = self.split_bet[1]))
		print('-'*30)
