#!/usr/bin/env python

import sqlite3
import argparse
import sys
import time

from player_class import Player, Fore, randint
from bot_player_class import BotPlayer
from dealer_class import Dealer
from deck_class import Deck

"""
Global Game Functions
"""
def create_players(p, bots, minimum, maximum):
	""" Create and append players and bots and return list of players."""
	players = []
	for i in range(0, p):
		n, b = get_user_info(i)
		players.append(Player(n, b, "Human", minimum, maximum))
	for i in range(0, bots):
		entering = True
		while entering:
			try:
				cash = int(
						raw_input(
							"Enter starting cash for Bot {num} "
							"(20, 50, 100, 200, 500, 1000, 2000): "
							.format(num = i+1)))
				if cash in [20, 50, 100, 200, 500, 1000, 2000]:
					entering = False
				else:
					print(
					"Please enter one of these: (20, 50, 100, 200, 500): "
					)
			except ValueError, e:
				print("Enter a number please")
		players.append(BotPlayer("",cash, "Bot", minimum, maximum))
	return players

def get_user_info(i):
	""" Get Name and Starting Cash from player and Return."""
	buy_in_list = [20,50,100,200,500, 1000, 2000]
	name = raw_input("Enter player {number}'s name: ".format(number = i+1))
	choosing = True
	while choosing:
		try:
			buy = int(
					raw_input("Select Starting Cash: 20, 50, 100, 200, "
													"500, 1000, 2000: ")
					)
		except ValueError, e:
			print("Invalid. Choose one of the above")
			continue
		if buy not in buy_in_list:
			print("Invalid. Choose again")
		else:
			choosing = False
	return name, buy

def show_player_info(players, dealer = None):
	""" Print each player's information to the console."""
	pnd = '#'
	for player in players:
		player.show_info()
	if dealer != None:
		dealer.show_card()
	print(pnd*50)

def deal(players, shoe):
	""" Initial deal. Deal Two cards to each player, check for blackjack."""
	dealer_blackjack = False
	print("Dealing Cards...")
	for player in players:
		card = deal_card(shoe)
		player.receive_card(card)

	for player in players:
		card = deal_card(shoe)
		player.receive_card(card)
		if player.get_score() == 21:
			player.blackjack = True

def play(dealer, players, shoe):
	""" Container for player/dealer turns. Return value from player_turn."""
	busted = player_turn(dealer, players, shoe)
	dealer_turn(players, shoe, busted)
	return busted

def player_split(player, shoe):
	""" Split player's hand, receive user unput for the next action."""
	print("Split")
	player.split_hand()
	card1 = deal_card(shoe)
	card2 = deal_card(shoe)
	player.split_receive_cards(card1, card2)
	player.split_show()
	i = 0 # hand counter
	for hand in player.hand:
		print("{n}: {h}: {c}".format(
								n = player.name,
								h = [card.display for card in hand],
								c = player.get_split_score()[i])
								)
		deciding = True
		while deciding:
			try:
				action = int(raw_input(
								"1: Hit, 2: Stand,"
								"3: DoubleDown, 4: Info: ")
								)
			except ValueError, e:
				action = 0
			if action == 1:
				player.split_hit_count[i] = player.split_hit_count[i] + 1
				print("Hit")
				card = deal_card(shoe)
				hand.append(card)
				print("Card: {c}".format(c = card.display))
				if check_hand_bust(hand):
					print("Hand Busted!")
					deciding = False
				else:
					player.split_show()
			elif action == 2:
				print("Stand")
				deciding = False
				continue
			elif action == 3:
				if player.split_hit_count[i] == 0:
					total_bet = 0
					for bet in player.split_bet:
						total_bet = total_bet + bet
					if total_bet + player.split_bet[i] <= player.cash:
						print("Double Down")
						player.split_bet[i] = player.split_bet[i] * 2
						print("Bet for hand {i} is now: {b}"\
									.format(i = i+1, b = player.split_bet[i]))
						card = deal_card(shoe)
						hand.append(card)
						print("Card: {c}".format(c = card.display))
						if check_hand_bust(hand):
							print("Hand {i} Busted!".format(i = i + 1))
						else:
							player.split_show()
						deciding = False
					else:
						print("Not Enough cash to double down")
				else:
					print("You can only double down if you haven't hit yet")
			elif action == 4:
				player.split_show()
			else:
				print("Invalid. Enter a number 1 - 4")
		i = i + 1

def check_hand_bust(hand):
	""" Check if a hand has busted and return boolean."""
	sum = 0
	ace = False
	for card in hand:
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

def player_turn(dealer, players, shoe):
	"""Get input from user on what action to take on their hand."""
	bust_count = 0
	deciding = True
	for player in players:
		if not player.blackjack:
			if player.type != 'Bot':
				dealer.show_card()
				player.quick_show()
				ask = True
				while ask:
					try:
						action = int(
									raw_input(
										"1: Hit, 2: Stand, 3: Split,"
										"4: DoubleDown, 5: Surrender,"
										"6: Insurance, 7: Self Info,"
										"8: All Info: "
										)
									)
					except ValueError, e:
						print("Please type a number")
						action = 0
					if action == 1: # HIT
						player.hit_count = player.hit_count + 1
						card = deal_card(shoe)
						player.receive_card(card)
						print("Card: {c}".format(c = card.display))
						if WAIT_TIME > 0:
							time.sleep(WAIT_TIME)
						if player.check_bust():
							print("{n} Busts!".format(n = player.name))
							bust_count = bust_count + 1
							ask = False
						else:
							player.quick_show()
					elif action == 2: #STAND
						ask = False
					elif action == 3: #SPLIT
						if player.hand[0].value == player.hand[1].value:
							if player.bet*2 <= player.cash:
								player.split = True
								player.split_bet = [player.bet, player.bet]
								player_split(player, shoe)
								ask = False
							else:
								print("Not enough cash to do that bet")
						else:
							print("Cannot do that action")
					elif action == 4: #DOUBLE DOWN
						if player.hit_count == 0:
							if player.bet*2 <= player.cash:
								player.double_down()
								card = deal_card(shoe)
								player.receive_card(card)
								print("Card: {c}".format(c = card.display))
								if player.check_bust():
									print("{n} Busts!".format(n = player.name))
									bust_count = bust_count + 1
								else:
									player.quick_show()
								ask = False
							else:
								print("Not enough cash!")
						else:
							print("You've already hit, cannot double down.")
					elif action == 5: #SURRENDER
						if player.hit_count == 0:
							print("{n} surrender's hand.".\
											format(n = player.name))
							tmp = player.bet/2
							player.cash = player.cash - tmp
							player.surrender = True
							ask = False
						else:
							print("You've already hit, cannot surrender.")
					elif action == 6: #INSURANCE
						if player.hit_count == 0:
							if dealer.hand[0].value == 11:
								print("Insurance")
								player.insurance = True
								player.insurance_bet = player.bet/2
								if (player.insurance_bet
									+ player.bet) > player.cash:
									print("Cannot afford insurance")
									player.insurance = False
									player.insurance_bet = 0
							else:
								print("Not allowed")
						else:
							print("You've already hit, cannot buy insurance.")
					elif action == 7: # PLAYER INFO
						player.show_info()
					elif action == 8:
						show_player_info(players, dealer)
					else:
						print("Invalid. Enter a number 1 - 7")
			else:
				while 1:
					player.quick_show()
					if player.hit():
						print('{n} hits'.format(n = player.name))
						card = deal_card(shoe)
						player.receive_card(card)
						print("Card: {c}".format(c = card.display))
						if WAIT_TIME > 0:
							time.sleep(WAIT_TIME)
						player.quick_show()
						if player.check_bust():
							print("{n} Bust!".format(n = player.name))
							break
					else:
						player.quick_show()
						print("{n} stands".format(n = player.name))
						break
	return bust_count

def dealer_turn(players, shoe, bust_count):
	""" Dealer action function."""
	dealer.quick_show()
	deciding = True
	while deciding:
		if dealer.check_hit():
			print('Dealer hit')
			card = deal_card(shoe)
			dealer.receive_card(card)
			print("Card: {c}".format(c = card.display))
			if WAIT_TIME > 0:
				time.sleep(WAIT_TIME)
			dealer.quick_show()
			if dealer.check_bust():
				print("Dealer Bust!")
				deciding = False
		else:
			dealer.quick_show()
			print('Dealer stand')
			deciding = False

def win_lose(dealer, players, busted):
	""" Check if each player has won, tied, or lost. Payout bets."""
	if not dealer.blackjack:
		dealer_score = dealer.get_score()
		for player in players:
			if not player.blackjack:
				if not player.surrender:
					if not player.split:
						if player.check_bust():
							player.lose()
						elif player.get_score() < dealer_score \
							and dealer_score < 22:
							player.lose()
						elif player.get_score() == dealer_score:
							player.tie()
						else:
							player.win()
					else:
						for i in range (0, len(player.hand)):
							if not player.split_surrender[i]:
								if check_hand_bust(player.hand[i]):
									player.lose()
								elif \
								player.get_split_score()[i] < dealer_score \
										and dealer_score < 22:
									player.lose()
								elif\
								player.get_split_score()[i] == dealer_score:
									player.tie()
								else:
									player.win()
							else:
								print("{n} already surrendered this hand"\
													.format(n = player.name))
			else:
				player.blackjack_win()
			if player.insurance:
				player.insurance_lose()
	else:
		print("Dealer Blackjack!")
		for player in players:
			if player.blackjack:
				print("{n} Blackjack -> Push".format(n = player.name))
				player.tie()
			else:
				player.lose()
			if player.insurance:
				player.insurance_win()

def reset(players):
	""" Reset each player's attributes to prepare for next deal."""
	for player in players:
		player.reset()

def intro_msg():
	""" Print a welcome message to the console."""
	pnd = "#"
	print(Fore.BLUE + pnd*50)
	print(pnd*50)
	print("         Welcome to Blackjack Terminal")
	print(pnd*50)
	print(pnd*50 + Fore.WHITE)

def show_table_rules(dealer, minimum, maximum):
	""" Print the house rules to the console"""
	print('+'*25)
	print("House Rules:")
	print("Dealer play: {p}".format(p = dealer.house_rule_name))
	print("Minimum Bet: {m}".format(m = minimum))
	print("Maximum Bet: {m}".format(m = maximum))
	print('+'*25)

def place_bets(players, dealer, minimum, maximum):
	""" Prompt user to input their bet for the next hand."""
	for player in players:
		if player.type == "Bot":
			player.place_bet()
			continue
		deciding = True
		while deciding:
			print("Type 'd' or 'done' to cash out.")
			print("Type 'i' or 'info' to see your information")
			print("Type 's' to show all player information")
			print("Type 'h' to see table rules")
			try:
				bet = raw_input("{n} place your bet: "\
									.format(n = player.name))
				if 'd' in bet:
					out = players.pop(players.index(player))
					print("{n} cashed out with: {c}"\
								.format(n = out.name, c = out.cash))
					deciding = False
					continue
				elif 'i' in bet:
					player.show_info()
					continue
				elif 's' in bet:
					show_player_info(players)
					continue
				elif 'h' in bet:
					show_table_rules(dealer, minimum, maximum)
					continue
				else:
					bet = int(bet)
			except ValueError, e:
				print("Invalid bet. Retry")
				continue
			if bet < minimum or bet > maximum:
				print('-'*20)
				print("Bet out of allowed range.")
				print("Table Minimum: {min}, Table Maximum: {max}"\
								.format(min = minimum, max = maximum))
				print('-'*20)
				continue
			elif player.cash - bet >= 0 and bet > 0:
				player.place_bet(bet)
				deciding = False
			else:
				print("Can't do that bet.")
	return players

def out_of_money(players, out):
	""" Check if any player's have 0 cash and remove then from the game."""
	keep = []
	for player in players:
		if player.cash > 0:
			keep.append(player)
		else:
			player.out_of_money()
			out.append(player)
			print("Player out of money. bye {n}.".format(n = player.name))
	return keep

def how_many_playing():
	""" Prompt user to enter the number of human players."""
	deciding = True
	while deciding:
		try:
			number_of_players = int(raw_input(
										"How many players? (up to 7): ")
									)
			if number_of_players < 6: # maximum 5 players
				deciding = False
			else:
				print("Too many players")
		except ValueError, e:
			print("Please enter a number")
	return number_of_players

def setup(shoe_size, house, player_count, bots, minimum, maximum):
	""" Print welcome info and create players, bots, and dealer."""
	intro_msg()
	print("Number of decks being used in shoe: {s}".format(s = shoe_size))
	#number_of_players = how_many_playing()
	players = create_players(player_count, bots, minimum, maximum)
	dealer = Dealer("", 0, "Dealer", house)
	dealer.greeting()

	people = []
	for player in players:
		print player.name
		people.append(player)
	people.append(dealer)

	return players, dealer, people

def create_shoe(shoe_size):
	""" Append each card from each deck to a list. Shuffle and return it."""
	decks = []
	for i in range(shoe_size):
		deck = Deck(i)
		deck.shuffle()
		decks.append(deck)
	shoe = [card for deck in decks for card in deck.cards]
	shoe = shuffle(shoe)
	return shoe

def shuffle(shoe):
	""" Fisher-yates shuffle algorithm. Shuffles the shoe."""
	n = len(shoe)
	for i in range(n-1,0,-1):
		j = randint(0, i)
		if j == i:
			continue
		shoe[i], shoe[j] = shoe[j], shoe[i]
	return shoe

def deal_card(shoe):
	""" Pops a card from the shoe to 'deal' to a player."""
	return shoe.pop(0)

def argument_setup(parser):
	""" Parse through terminal args and assign variables."""
	args = parser.parse_args()

	if args.players:
		if args.bots:
			if args.players + args.bots > 7:
				print("Can only play with at most 7 players and bots")
				while 1:
					try:
						players = int(raw_input("Enter number of players: "))
					except ValueError, e:
						print("Enter a number")
					if players + args.bots > 7:
						print("Still too many players & bots.")
					else:
						break
			else:
				players = args.players
		elif args.players > 7:
			print("Can only play with at most 7 players and bots")
			while 1:
				try:
					players = int(raw_input("Enter number of players: "))
				except ValueError, e:
					print("Enter a number")
				if players > 7:
					print("Still too many players & bots.")
				else:
					break
		else:
			players = args.players
	else:
		players = 0

	if args.shoe:
		SHOE_SIZE = args.shoe
	else:
		SHOE_SIZE = 6

	if args.house:
		house_rules = args.house
	else:
		house_rules = 1

	if args.bots:
		if args.players:
			if args.bots + args.players > 7:
				print("Can only play with at most 7 players and bots")
				while 1:
					try:
						bots = int(raw_input("Enter number of bots: "))
					except ValueError, e:
						print("Enter a number")
					if bots + players > 7:
						print("Still too many players & bots.")
					else:
						break
			else:
				bots = args.bots
		elif args.bots > 7:
			print("Can only play with at most 7 players and bots")
			while 1:
				try:
					bots = int(raw_input("Enter number of players: "))
				except ValueError, e:
					print("Enter a number")
				if bots > 7:
					print("Still too many players & bots.")
				else:
					break
		else:
			bots = args.bots
	else:
		bots = 0

	global WAIT_TIME #messy code
	if args.time:
		WAIT_TIME = args.time
	elif args.time == 0:
		WAIT_TIME = args.time
	else:
		if players == 0:
			WAIT_TIME = 0
		else:
			WAIT_TIME = 1.5

	if args.minimum:
		minimum = args.minimum
	else:
		print("Minimum table bet must be in [10, 20, 50, 100]")
		print("Setting minimum table bet to 10")
		minimum = 10

	if args.maximum:
		maximum = args.maximum
	else:
		print("Maximum table bet must be in [10, 20, 50, 100, 500, 1000]")
		print("Setting maximum table bet to 500")
		maximum = 10000

	if bots + players == 0:
		print("Usage: ./blackjack --players 1 --bots 2")
		print("Enter number of players and bots through command line")
		sys.exit(1)
	return SHOE_SIZE, house_rules, players, bots, minimum, maximum

def connect_to_database():
	""" Attempt to connect to sqlite database. Return connection object."""
	try:
		connection = sqlite3.connect('test_db')
		print("DB Connected!")
	except Exception, e:
		print e
		sys.exit(1)
	return connection

def create_tables(connection):
	""" Create database tables if they are not yet created."""
	connection.execute(""" CREATE TABLE IF NOT EXISTS ROUNDS
		(ID 	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		NAME 	TEXT,
		BET 	INT,
		CARD1 	TEXT,
		CARD2,	TEXT,
		OUTCOME TEXT);""")

def insert_round(players, connection):
	""" Insert each player's hand, bet, and outcome into table ROUNDS."""
	for player in players:
		if not player.split:
			connection.execute(
				"""INSERT INTO ROUNDS (NAME,BET,CARD1,CARD2,OUTCOME)"""
				"""VALUES ('{n}',{b},'{c1}','{c2}','{o}');"""
					.format(
						n=player.name,
						b=player.bet,
						c1=player.hand[0].name,
						c2=player.hand[1].name,
						o=player.outcome)
			)
		else:
			connection.execute(
				"""INSERT INTO ROUNDS (NAME,BET,CARD1,CARD2,OUTCOME)"""
				"""VALUES ('{n}',{b},'{c1}','{c2}','{o}');"""
					.format(
						n=player.name,
						b=player.split_bet[0],
						c1=player.hand[0][0].name,
						c2=player.hand[0][1].name,
						o=player.outcome)
			)
			connection.execute(
				"""INSERT INTO ROUNDS (NAME,BET,CARD1,CARD2,OUTCOME)"""
				"""VALUES ('{n}',{b},'{c1}','{c2}','{o}');"""
					.format(
						n=player.name,
						b=player.split_bet[1],
						c1=player.hand[1][0].name,
						c2=player.hand[1][1].name,
						o=player.outcome)
			)
	connection.commit()

# Main Method. Program Starts and Ends Here
if __name__ == "__main__":
	""" Game creation, setup and loop contained in here."""
	parser = argparse.ArgumentParser(
		description="Blackjack Terminal: A game for fun or a simulator"
		" for putting strategies to the test"
	)
	parser.add_argument(
		"-p","--players",
		help="Number of Human players",
		type=int
	)
	parser.add_argument(
		"-s","--shoe",
		help="set how many decks used in the shoe",
		type=int
	)
	parser.add_argument(
		"--house",
		help="1: Dealer stand on all 17, 2: Dealer hit on soft 17",
		type=int
	)
	parser.add_argument(
		"-b","--bots",
		help="Enter number of bots you want. Up to 7",
		type=int
	)
	parser.add_argument(
		"-t","--time",
		help="Wait time for actions such as deal cards, hit, stand, etc"
			". For simulations do 0, for humans playing do 1.5",
		type=int
	)
	parser.add_argument("--minimum", help="Table Minimum Bet", type=int)
	parser.add_argument("--maximum", help="Table Maximum Bet", type=int)

	SHOE_SIZE, house_rules, player_count, bots, minimum, maximum = \
													argument_setup(parser)
	connection = connect_to_database()
	create_tables(connection)
	players, dealer, people = setup(
								SHOE_SIZE, house_rules, player_count,
								bots, minimum, maximum
								)
	DECK_SIZE = 52
	TOTAL_CARDS = SHOE_SIZE * DECK_SIZE
	shoe = create_shoe(SHOE_SIZE)

	####################################
	# Game Loop                        #
	####################################
	reshuffle_count = 0
	end_game = False
	round_num = 0
	out = []
	while not end_game:
		round_num = round_num + 1
		print("*******************Round {r}**********************"\
				.format(r = round_num))
		if len(shoe) < TOTAL_CARDS/2:
			print("Dealer Reshuffling Shoe!")

			if WAIT_TIME > 0:
				time.sleep(WAIT_TIME)
			shoe = create_shoe(SHOE_SIZE)
			reshuffle_count = reshuffle_count + 1
		players = place_bets(players, dealer, minimum, maximum)
		if players:
			deal(people, shoe)
			show_player_info(players, dealer)
			busted = play(dealer, players, shoe)
			win_lose(dealer, players, busted)
			insert_round(players, connection)
			reset(people)
			players = out_of_money(players, out)
		else:
			print("No players left. Game over.")
			print("PostGame Statistics")
			print("reshuffle count: {c}".format(c = reshuffle_count))
			for player in out:
				player.end_game_stats()
			end_game = True
			continue

	connection.close()
