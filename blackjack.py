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
from random import randint
from player_class import Player
from dealer_class import Dealer

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
def deal(players):
	# TODO: create a 'Deck' which actually gets shuffled and delt
	cards = [1,2,3,4,5,6,7,8,9,10,10,10,10,11]
	print("Dealing Cards...")
	for player in players:
		card = cards[randint(0,len(cards) - 1)]
		player.receive_card(card)

	for player in players:
		card = cards[randint(0,len(cards) - 1)]
		player.receive_card(card)

# Rest of Hand after initial deal
def play(dealer, players):
	cards = [1,2,3,4,5,6,7,8,9,10,10,10,10,11]
	for player in players:
		player.quick_show()
		ask = True
		while ask:
			hit_stand = raw_input("Hit or Stand? (h/s): ")
			if 'h' in hit_stand.lower():
				card = cards[randint(0,13)] # generate card
				player.receive_card(card) # give player card
				print("Card: {c}".format(c = card))
				if player.check_bust():
					print("Player Bust!")
					ask = False
				else:
					player.quick_show()
			elif 's' in hit_stand.lower():
				ask = False
			else:
				print("Invalid. Hit 'h' or 's'")
	deciding = True
	while deciding:
		if dealer.highest(players):
			dealer.quick_show()
			print('dealer stand')
			deciding = False
		else:
			if dealer.hit():
				print('dealer hit')
				card = cards[randint(0,13)]
				dealer.receive_card(card)
				print("Card: {c}".format(c = card))
				dealer.quick_show()
				if dealer.check_bust():
					print("Dealer Bust!")
					deciding = False
			else:
				dealer.quick_show()
				print('dealer stand')
				deciding = False
				
# check how each player finished the hand
def win_lose(dealer, players):
	dealer_score = dealer.get_score()
	for player in players:
		if player.get_score() < dealer_score:
			player.cash = player.cash - 10 # add method in player class for this
		elif player.get_score() > dealer_score:
			player.cash = player.cash + 10 # add method in player class for this
		else:
			print player.name + " Tie!"
	show_player_info(players)

# reset every players cards
def reset_cards(players):
	for player in players:
		player.reset_cards()

# initial message
def intro_msg():
	pnd = "#"
	print(pnd*50)
	print(pnd*50)
	print("         Welcome to Blackjack Terminal") # TODO: Better intro
	print(pnd*50)
	print(pnd*50)	

# Main Method. Program Starts and Ends Here
if __name__ == "__main__":

	#TODO: This starting setting up game should be in a separate function!!!
	parser = argparse.ArgumentParser(description="Blackjack Terminal Game")
	start = False

	intro_msg()
	# ask user how many players, can't have more than 5
	while start == False:
		number_of_players = int(raw_input("How many players? (up to 5)"))
		# check if not more than 5 players
		if number_of_players < 6:
			start = True
		else:
			print("Too many players")
	
	players = create_players(number_of_players)
	#show_player_info(player_list)
	
	# Create the dealer
	dealer = Dealer()
	dealer.greeting()
	
	people = []
	for player in players:
		print player.name
		people.append(player)
	
	people.append(dealer)
	#for p in people:
	#	print p.name
	
	# TODO: let them add/delete players here.. aka change game setup
	# Let players join mid game just like real blackjack
	####################################
	# Game Loop
	####################################
	end_game = False
	round = 1
	while not end_game:
		deal(people)
		show_player_info(people)
		play(dealer, players)
		win_lose(dealer, players)
		reset_cards(people)
		
		again = raw_input("Continue Playing? (y/n)")
		if again != 'y':
			end_game = True
		
		
		
		
		
		
		
		