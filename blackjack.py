# Blackjack Terminal Game
# Python 2.7.11

import argparse
import time
from random import randint
from player_class import Player
from bot_player_class import BotPlayer
from dealer_class import Dealer
from deck_class import Deck
"""
TODO: 
0. Minimum Bet/Maximum Bet Rules -> Potentially add to house rules
1. Add Different House Rules
2. Create different BotPlayer Profiles (Strategies)
3. Better manage the way bots make bets
4. Double down should only be an action if player has not hit yet!
5. Import colorama module for colored terminal output
6. Save all output strings into variables and replace print statement strings with vars
	a. this will be for quick fixing and reusability. right now its kind of a mess
"""
"""
# Global Game Functions
"""
# create the players
def create_players(p, bots):
	players = []
	for i in range(0, p):
		n, b = get_user_info(i)
		players.append(Player(n, b, 'Human'))
	for i in range(0, bots):
		entering = True
		while entering:
			try:
				cash = int(raw_input("Enter starting cash for Bot {num} (20, 50, 100, 200, 500): ".format(num = i+1)))
				if cash in [20, 50, 100, 200, 500]:
					entering = False
				else:
					print("Please enter one of these: (20, 50, 100, 200, 500): ")
			except ValueError, e:
				print("Enter a number please")
		players.append(BotPlayer(cash, 'Bot'))
	return players

# ask user for name and buy in amount
def get_user_info(i):
	buy_in_list = [20,50,100,200,500]
	name = raw_input("Enter player {number}'s name: ".format(number = i+1))
	choose_buy_in = True
	while choose_buy_in:
		try:
			buy = int(raw_input("How much will you buy in with: 20, 50, 100, 200, 500? "))
		except:
			print("Invalid. Setting default buy in: 20")
			buy = 20
		if buy not in buy_in_list:
			print("Invalid. Choose again")
		else:
			choose_buy_in = False
	return name, buy
	
# output player info to console
def show_player_info(players, dealer = None):
	pnd = '#'
	for player in players:
		player.show_info()
	if dealer != None:
		dealer.show_card()
	print(pnd*50)

# TODO: better way to iterate list twice aka deal two cards
def deal(players, shoe):
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
		
# Rest of Hand after initial deal
def play(dealer, players, shoe):
	busted = player_turn(dealer, players, shoe)
	dealer_turn(players, shoe, busted)
	return busted

def player_split(player, shoe):
	print("Split")
	player.split_hand() # split hand
	card1 = deal_card(shoe)
	card2 = deal_card(shoe)
	player.split_receive_cards(card1, card2)
	player.split_show()
	i = 0
	for hand in player.hand:
		print("{n}: {h}: {c}".format(n = player.name, h = [card.display for card in hand], c = player.get_split_score()[i]))
		deciding = True
		while deciding:
			try:
				action = int(raw_input("1: Hit, 2: Stand, 3: DoubleDown, 4: Surrender, 5: Info: "))
			except ValueError, e:
				action = 0
			if action == 1:
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
				total_bet = 0
				for bet in player.split_bet:
					total_bet = total_bet + bet
				if total_bet + player.split_bet[i] <= player.cash: #total bet plus 1 more
					print("Double Down")
					player.split_bet[i] = player.split_bet[i] * 2 # double the current bet
					print("Bet for hand {i} is now: {b}".format(i = i+1, b = player.split_bet[i]))
					card = deal_card(shoe)
					hand.append(card)
					print("Card: {c}".format(c = card.display))
					if check_hand_bust(hand):
						print("Hand {i} Busted!".format(i = i + 1))
						#bust_count = bust_count + 1 # still deciding wether to keep this or not
					else:
						player.split_show()
					deciding = False
				else:
					print("Not Enough cash to double down")
			elif action == 4:
				print("Surrender")
				print("{n} surrender's hand.".format(n = player.name))
				tmp = player.split_bet[i]/2
				player.cash = player.cash - tmp
				player.split_surrender[i] = True
				deciding = False
			elif action == 5:
				player.split_show()
			else:
				print("Invalid. Enter a number 1 - 4")
		i = i + 1 # increment hand counter
		
def check_hand_bust(hand):
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
			
# players turns	
def player_turn(dealer, players, shoe):
	bust_count = 0
	deciding = True
	for player in players:
		if player.type != 'Bot':
			dealer.show_card()
			player.quick_show()
			ask = True
			while ask:
				try:
					action = int(raw_input("1: Hit, 2: Stand, 3: Split, 4: DoubleDown, 5: Surrender, 6: Insurance, 7: Self Info, 8: All Info: "))
				except ValueError, e:
					print("Please type a number")
					action = 0
				if action == 1: # HIT
					card = deal_card(shoe)
					player.receive_card(card) # give player card
					print("Card: {c}".format(c = card.display))
					time.sleep(1)
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
					if player.bet*2 <= player.cash:
						player.bet = player.bet * 2
						print("Double down!")
						print("{n}'s bet is now: {b}".format(n = player.name, b = player.bet))
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
				elif action == 5: #SURRENDER
					print("{n} surrender's hand.".format(n = player.name))
					tmp = player.bet/2
					player.cash = player.cash - tmp
					player.surrender = True
					ask = False
				elif action == 6: #INSURANCE
					if dealer.hand[0].value == 11:
						print("Insurance")
						player.insurance = True
						bet_not_place = True
						while bet_not_place:
							try:
								insurance = int(raw_input("Place your insurance bet: "))
								if insurance + player.bet <= player.cash:
									bet_not_place = False
								else:
									print("You cant afford that bet")
							except:
								print("Please print a number")
						player.insurance_bet = insurance					
					else:
						print("Not allowed")
				elif action == 7: # PLAYER INFO
					player.show_info()
				elif action == 8:
					show_player_info(players, dealer)
				else:
					print("Invalid. Enter a number 1 - 7")
		else:
			player.quick_show()
			if player.hit():
				print('{n} hits'.format(n = player.name))
				card = deal_card(shoe)
				player.receive_card(card)
				print("Card: {c}".format(c = card.display))
				time.sleep(1)
				player.quick_show()
			if player.check_bust():
				print("{n} Bust!".format(n = player.name))
				deciding = False
			else:
				player.quick_show()
				print("{n} stands".format(n = player.name))
				deciding = False
	return bust_count

# dealer decision turn	
def dealer_turn(players, shoe, bust_count):
	dealer.quick_show()
	time.sleep(1) # this should be made optional. if only bots, no wait
	deciding = True
	while deciding:
		if dealer.check_hit():
			print('Dealer hit')
			card = deal_card(shoe)
			dealer.receive_card(card)
			print("Card: {c}".format(c = card.display))
			time.sleep(1)
			dealer.quick_show()
			if dealer.check_bust():
				print("Dealer Bust!")
				deciding = False
		else:
			dealer.quick_show()
			print('Dealer stand')
			deciding = False
				
# check how each player finished the hand
def win_lose(dealer, players, busted):
	if not dealer.blackjack:
		dealer_score = dealer.get_score()
		for player in players:
			if not player.blackjack:
				if not player.surrender:
					if not player.split:
						if player.check_bust():
							player.lose()
						elif player.get_score() < dealer_score and dealer_score < 22:
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
								elif player.get_split_score()[i] < dealer_score and dealer_score < 22:
									player.lose()
								elif player.get_split_score()[i] == dealer_score:
									player.tie()
								else:
									player.win()
							else:
								print("{n} already surrendered this hand".format(n = player.name))
			else:
				player.blackjack_win()
			if player.insurance:
				print("{n} loses insurance money -> Dealer does not have blackjack".format(n = player.name))
				player.cash = player.cash - player.insurance_bet # this could be moved to player class
	else:
		print("Dealer Blackjack!")
		for player in players:
			if player.blackjack:
				print("{n} Blackjack -> Push".format(n = player.name))
				player.tie()
			else:
				player.lose()
			if player.insurance:
				print("{n} Insurance pays off!".format(n = player.name))
				player.cash = player.cash + player.insurance_bet # this could be moved to player class
				
# reset every players cards
def reset(players):
	for player in players:
		player.reset()

# initial message
def intro_msg():
	pnd = "#"
	print(pnd*50)
	print(pnd*50)
	print("         Welcome to Blackjack Terminal") # TODO: Better intro
	print(pnd*50)
	print(pnd*50)	

#place bets
def place_bets(players):
	for player in players:
		if player.type == "Bot":
			bet = 10 # need to make this more of a real bet instead of 10 each time
			player.bet = bet
			continue
		deciding = True
		while deciding:
			print("Type 'd' or 'done' to cash out.")
			print("Type 'i' or 'info' to see your information")
			print("Type 's' to show all player information")
			try:
				bet = raw_input("{n} place your bet: ".format(n = player.name))
				if 'd' in bet:
					out = players.pop(players.index(player))
					print("{n} cashed out with: {c}".format(n = out.name, c = out.cash))
					deciding = False
					continue
				elif 'i' in bet:
					player.show_info()
					continue
				elif 's' in bet:
					show_player_info(players)
					continue
				else:
					bet = int(bet)
			except:
				print("Invalid bet. setting bet as 10")
				bet = 10
			if player.cash - bet >= 0 and bet > 0:
				player.bet = bet
				deciding = False
			else:
				print("Can't do that bet.")
	return players
		
def out_of_money(players):
	keep = []
	for player in players:
		if player.cash > 0:
			keep.append(player)
			#players.pop(players.index(player))
		else:
			print("Player out of money. bye {n}.".format(n = player.name))
	return keep

# ask user how many players, can't have more than 5
def how_many_playing():
	start = False
	while start == False:
		number_of_players = int(raw_input("How many players? (up to 5): "))
		# check if not more than 5 players
		if number_of_players < 6:
			start = True
		else:
			print("Too many players")
	return number_of_players

# initial game setup	
def setup(shoe_size, house, bots):

	intro_msg()
	print("Number of decks being used in shoe: {s}".format(s = shoe_size))
	number_of_players = how_many_playing()
	players = create_players(number_of_players, bots)
	dealer = Dealer(house)
	dealer.greeting()
	
	people = []
	for player in players:
		print player.name
		people.append(player)
	people.append(dealer)
	
	return players, dealer, people

# create shoe
def create_shoe(shoe_size):
	decks = []
	for i in range(shoe_size):
		deck = Deck(i)
		deck.shuffle()
		decks.append(deck)
	shoe = [card for deck in decks for card in deck.cards]
	shoe = shuffle(shoe)	
	return shoe

#fisher-yates shuffle
def shuffle(shoe):
	n = len(shoe)
	for i in range(n-1,0,-1):
		j = randint(0, i)
		if j == i:
			continue
		shoe[i], shoe[j] = shoe[j], shoe[i]
	return shoe

# pop card from shoe	
def deal_card(shoe):
	return shoe.pop(0)
		
# Main Method. Program Starts and Ends Here
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Blackjack Terminal Game")
	parser.add_argument("-s","--shoe", help="set how many decks used in the shoe", type=int)
	parser.add_argument("--house", help="1: Dealer stand on all 17, 2: Dealer hit on soft 17", type=int)
	parser.add_argument("-b","--bots", help="Enter number of bots you want. Up to 5", type=int)
	parser.add_argument("--minimum", help="Table Minimum Bet", type=int)
	parser.add_argument("--maximum", help="Table Maximum Bet", type=int)
	args = parser.parse_args()
	# parse program arguments
	if args.shoe:
		shoe_size = args.shoe
	else:
		shoe_size = 6
	
	if args.house:
		house_rules = args.house
	else:
		house_rules = 1 # default house rules as of right now
	
	if args.bots:
		if args.bots > 5:
			print("Can only play with at most 5 bots.")
			entering = True
			while entering:
				try:
					bots = int(raw_input("Enter number of bots: "))
				except ValueError, e:
					print("Enter a number")
		else:
			bots = args.bots
	else:
		bots = 0
	
	if args.minimum in [10, 20, 50, 100]:
		minimum = args.minimum
	else:
		print("Minimum table bet must be in [10, 20, 50, 100]")
		print("Setting minimum table bet to 10")
		minimum = 10
		
	if args.maximum in [10, 20, 50, 100, 500, 1000, 2000]:
		maximum = args.maximum
	else:
		print("Maximum table bet must be in [10, 20, 50, 100, 500, 1000, 2000]")
		print("Setting maximum table bet to 500")
		maximum = 500
	
	players, dealer, people = setup(shoe_size, house_rules, bots)
	deck_size = 52
	total_cards = shoe_size * deck_size
	shoe = create_shoe(shoe_size)
	
	####################################
	# Game Loop                        #
	####################################
	reshuffle_count = 0
	end_game = False
	round = 0
	while not end_game:
		round = round + 1
		print("***************************Round {r}*********************************".format(r = round))
		if len(shoe) < total_cards/2:
			print("Dealer Reshuffling Shoe!")
			time.sleep(3)
			shoe = create_shoe(shoe_size)
			reshuffle_count = reshuffle_count + 1
		players = place_bets(players)
		if players:
			deal(people, shoe)
			show_player_info(players, dealer)
			busted = play(dealer, players, shoe)
			win_lose(dealer, players, busted)
			reset(people)
			players = out_of_money(players)
		else:
			print("No players left. Game over.")
			print("reshuffle count: {c}".format(c = reshuffle_count))
			end_game = True
			continue