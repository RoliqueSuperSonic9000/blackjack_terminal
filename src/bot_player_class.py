"""
Bot Player Class
"""
from player_class import Player, randint, Fore

class BotPlayer(Player):

	# These could be made into dictionaries
	hand_strategies = [1, 2, 3]
	hand_strategy_names =[
		"Stand on all 12 or greater",
		"Stand on all 17 or greater",
		"Hit on soft 17"
	]
	bet_strategies = [1, 2, 3]
	bet_strategy_names =[
		"Raise bets after wins",
		"Raise bets after losses",
		"Same bet every time"
	]

	def __init__(self, n, c, t, tbl_min, tbl_max,s=None, bs=None):
		Player.__init__(self, n, c, t)
		self._min_bet = tbl_min
		self._max_bet = tbl_max
		if s is not None:
			self._hand_strategy = s
		else:
			self._hand_strategy = BotPlayer \
								.hand_strategies \
								[randint(0, len(BotPlayer.hand_strategies)-1)]
		self._hand_strategy_name = BotPlayer \
								.hand_strategy_names[self.hand_strategy-1]

		if bs is not None:
			self._bet_strategy = s
		else:
			self._bet_strategy = BotPlayer \
								.bet_strategies \
								[randint(0, len(BotPlayer.bet_strategies)-1)]
		#self._bet_strategy_name = BotPlayer \
		#						.bet_strategy_names[self.bet_strategy-1]
		self._round_bet_history = []
		self._round_outcome_history = []


	@property
	def min_bet(self):
		return self._min_bet

	@property
	def max_bet(self):
		return self._max_bet

	@property
	def hand_strategy(self):
		return self._hand_strategy

	@hand_strategy.setter
	def hand_strategy(self):
		self._hand_strategy = s

	@property
	def hand_strategy_name(self):
		return self._hand_strategy_name

	@property
	def bet_strategy(self):
		return self._bet_strategy

	@bet_strategy.setter
	def bet_strategy(self, b):
		self._bet_strategy = b

	@property
	def bet_strategy_names(self):
		return self._bet_strategy_name

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

	def raise_bet_after_win(self):
		if self.previous_round_win():
			self.bet = self.round_bet_history[-1] * 2
		else:
			self.bet = self.min_bet

	def raise_bet_after_loss(self):
		if not self.previous_round_win():
			self.bet = self.round_bet_history[-1] * 2
		else:
			self.bet = self.min_bet

	def same_bet_as_previous_round(self):
		self.bet = self.round_bet_history[-1]

	def previous_round_win(self):
		if self.round_outcome_history[-1] == "Win":
			return True
		else:
			return False

	def previous_round_outcome(self):
		return self.round_outcome_history[-1]

	def previous_round_bet(self):
		return self.round_bet_history[-1]

	def add_round(self, o, b):
		self.round_outcome_history.append(o)
		self.round_bet_history.append(b)

	def lose(self):
		""" Subtract the player's bet from the player's cash total."""
		print(Fore.RED + "{n} loses.".format(n = self.name))
		print(Fore.WHITE)
		self.cash = self.cash - self.bet
		self.outcome = "Lose"
		self.add_round(self.outcome, self.bet)

	def win(self):
		""" Add the player's bet to the player's cash total."""
		print(Fore.GREEN + "{n} wins!".format(n = self.name))
		print(Fore.WHITE)
		self.cash = self.cash + self.bet
		self.outcome = "Win"
		self.add_round(self.outcome, self.bet)

	def tie(self):
		""" Alert the player they have tied the dealer."""
		print(Fore.BLUE + "{n} ties.".format(n = self.name))
		print(Fore.WHITE)
		self.outcome = "Tie"
		self.add_round(self.outcome, self.bet)

	def blackjack_win(self):
		""" Add the players bet plus 1/2 bet to the player's cash total."""
		print("{n} Blackjack!".format(n = self.name))
		self.cash = self.cash + (self.bet * 1.5)
		self.outcome = "Win"
		self.add_round(self.outcome, self.bet)

	def place_bet(self):
		""" Bot place bet amount for next hand."""
		if not self.round_bet_history:
			self.bet = self.min_bet
		elif self.bet_strategy == 1:
			self.raise_bet_after_win()
		elif self.bet_strategy == 2:
			self.raise_bet_after_loss()
		else:
			self.same_bet_as_previous_round()

	def next_move(self):
		""" Return a string of what the bots next move is."""
		if self.hand:
			if self.hit():
				return "Hit"
			else:
				return "Stand"
		else:
			return "Bet"

	def show_info(self):
		""" Print useful player information to the console."""
		tick = '-'
		print(tick*20)
		print("Name: {n}".format(n = self.name))
		print("Cash: {c}".format(c = self.cash - self.bet))
		print("Bet:  {b}".format(b = self.bet))
		print("Hand: {h}".format(h = [card.display for card in self.hand]))
		print("Count: {c}".format(c = self.get_score()))
		print("Strategy: {s}".format(s = self.hand_strategy_name))
		print("Next Move: {m}".format(m = self.next_move()))
		print(tick*20)

	def stand_on_all_12(self):
		""" Bot will hit only if hand is less than 12."""
		if self.score < 12:
			return True
		else:
			return False

	def stand_on_all_17(self):
		""" Bot will hit only if hand is less than 17."""
		if self.score < 17:
			return True
		else:
			return False

	def hit_on_soft_17(self):
		""" Bot will hit if score is less than 17 or 17 with an ace."""
		if self.score < 17:
			return True
		elif self.score == 17:
			for card in self.hand:
				if card.value == 11:
					return True
		else:
			return False

	def hit(self):
		""" Check whether to hit or stay."""
		self.get_score()
		if self.hand_strategy == 1:
			return self.stand_on_all_12()
		elif self.hand_strategy == 2:
			return self.stand_on_all_17()
		elif self.hand_strategy == 3:
			return self.hit_on_soft_17()
		else:
			return False # place holder for now
