# Blackjack Terminal Game
# Python 2.7.11
"""
Game:
1. Run program
2. Welcome to black jack
3. How many players?
4. Set table limit, starting money, bet types
5. players buy in
6. start game loop
7. dealer deals
8. for each player ask hit or stand
9. if hit deal card
10 if stand move to next player
11.dealer will need built in rules -> under 17 hit?
12. check scores
13. take/give earnings/losses
14. if player out of money -> buy back in? if not game over
15. back to line 7 
"""
import argparse
import time
from random import randint
from player_class import Player
from dealer_class import Dealer
from deck_class import Deck
"""
# Global Functions
"""
# create the players
def create_players(p):
	players = []
	for i in range(0, p):
		n, b = get_user_info(i)
		players.append(Player(n, b))
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
def show_player_info(players):
	for player in players:
		player.show_info()

# deal each player, including dealer, two cards
# TODO: better way to iterate list twice aka deal two cards
def deal(players, shoe):
	# TODO: create a 'Deck' which actually gets shuffled and delt
	#cards = [1,2,3,4,5,6,7,8,9,10,10,10,10,11]
	dealer_blackjack = False
	print("Dealing Cards...")
	for player in players:
		#card = cards[randint(0,len(cards) - 1)]
		card = deal_card(shoe)
		player.receive_card(card)

	for player in players:
		card = deal_card(shoe)
		player.receive_card(card)

	if players[-1].score == 21:
		print("Dealer Blackjack")
	
	if dealer_blackjack == True:
		for player in players:
			if player.score != 21:
				player.lose()
			else:
				player.tie()
	return dealer_blackjack

# Rest of Hand after initial deal
def play(dealer, players, shoe):
	#This can be put in its own function too
	#cards = [1,2,3,4,5,6,7,8,9,10,10,10,10,11]
	busted = player_turn(dealer, players, shoe)
	dealer_turn(players, shoe, busted)
	return busted
	
# players turns	
def player_turn(dealer, players, shoe):
	bust_count = 0
	for player in players:
		dealer.quick_show()
		player.quick_show()
		ask = True
		while ask:
			hit_stand = raw_input("Hit or Stand? (h/s): ")
			if 'h' in hit_stand.lower():
				card = deal_card(shoe)
				player.receive_card(card) # give player card
				print("Card: {c}".format(c = card.display))
				time.sleep(1)
				if player.check_bust():
					print("Player Bust!")
					bust_count = bust_count + 1
					ask = False
				else:
					player.quick_show()
			elif 's' in hit_stand.lower():
				ask = False
			else:
				print("Invalid. Hit 'h' or 's'")
	return bust_count

# This should be moved into the dealer class
# dealer decision turn	
def dealer_turn(players, shoe, bust_count):
	deciding = True
	if bust_count == len(players):
		deciding = False
	while deciding:
		"""
		# This is not how blackjack dealers play. removed.
		if dealer.highest(players):
			#dealer.quick_show()
			print('dealer stand')
			deciding = False
		"""
		if dealer.hit():
			print('dealer hit')
			card = deal_card(shoe)
			dealer.receive_card(card)
			print("Card: {c}".format(c = card.display))
			time.sleep(1.5)
			dealer.quick_show()
			if dealer.check_bust():
				print("Dealer Bust!")
				deciding = False
		else:
			dealer.quick_show()
			print('dealer stand')
			deciding = False
				
# check how each player finished the hand
def win_lose(dealer, players, busted):
	skip = False
	if busted == len(players):
		print "Every player busted"
		skip = True
	if not skip:
		dealer_score = dealer.get_score()
		for player in players:
			if player.check_bust():
				player.lose()
			elif player.get_score() < dealer_score and dealer_score < 22:
				player.lose()
			elif player.get_score() == dealer_score:
				player.tie()
			else:
				player.win()
	if skip:
		for player in players:
			player.lose()

# reset every players cards
def reset_cards(players):
	for player in players:
		player.reset_hand()

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
		deciding = True
		while deciding:
			print("Type 'd' or 'done' to cash out.")
			print("Type 'i' or 'info' to see your information")
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

	
# TODO: let them add/delete players here.. aka change game setup
# Let players join mid game just like real blackjack
# initial game setup	
def setup(shoe_size):

	intro_msg()
	print("Number of decks being used in shoe: {s}".format(s = shoe_size))
	number_of_players = how_many_playing()
	players = create_players(number_of_players)
	dealer = Dealer()
	dealer.greeting()
	
	people = []
	for player in players:
		print player.name
		people.append(player)
	people.append(dealer)
	
	return players, dealer, people

"""
# same as below but i think slower
combined_deck = []
for deck in shoe:
	print deck.unique_id
	for card in deck.cards:
		combined_deck.append(card)
"""

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
	parser.add_argument("-s","--shoe",help="set how many decks used in the shoe", type=int)
	args = parser.parse_args()
	
	if args.shoe:
		shoe_size = args.shoe
	else:
		shoe_size = 6
		
	players, dealer, people = setup(shoe_size)
	deck_size = 52
	total_cards = shoe_size * deck_size
	shoe = create_shoe(shoe_size)
	
	
	####################################
	# Game Loop
	####################################

	
	for card in shoe:
		print card.display
	
	#deck = Deck(1) # initialize deck
	#deck.shuffle()
	end_game = False
	round = 1
	while not end_game:
		print("***************************Round {r}*********************************".format(r = round))
		if len(shoe) < total_cards/2:
			shoe = create_shoe(shoe_size)
			#deck.new_deck() # add in reshuffle for shoe
		players = place_bets(players)
		if players:
			dealer_blackjack = deal(people, shoe)
			if dealer_blackjack:
				continue
			else:
				show_player_info(people)
				busted = play(dealer, players, shoe)
				win_lose(dealer, players, busted)
				reset_cards(people)
				players = out_of_money(players)
		if not players:
			print("No players left. Game over.")
			end_game = True
			continue
		
		
		
		
		
		
		
		