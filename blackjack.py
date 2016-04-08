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

#TODO: Create abstracted 'player' class for both player and dealer to extend
"""
# Player Class
"""
class Player(object):

	# constructor
	def __init__(self, n, c):
		self._name = n
		self._cash = c
		self._cards = []
	@property
	def name(self):
		return self._name

	@property
	def cash(self):
		return self._cash

	@cash.setter
	def cash(self, c):
		self._cash = c
	
	@property
	def cards(self):
		return self._cards
	
	# receive card
	def receive_card(self, card):
		self.cards.append(card)
	
	# check if player has gone over 21
	def check_bust(self):
		sum = 0
		for card in cards:
			sum = sum + card
			if sum > 21:
				return True
		return False
		
	def show_info(self):
		tick = '-'
		print(tick*20)
		print("Name: {n}".format(n = self.name))
		print("Cash: {c}".format(c = self.cash))
		print("Hand: {h}".format(h = self.cards)) #TODO format hand better
		print(tick*20)

"""
# Dealer Class
"""		
class Dealer(object):

	# constructor
	def __init__(self, name_list):
		# initialize
		self._name = name_list[0] # TODO: make random
		self._cards = []
		
	@property
	def name(self):
		return self._name
	
	def greeting(self):
		star ='*'
		print("{name}: Hello I'm your dealer {name}".format(name = self.name))

	@property
	def cards(self):
		return self._cards
	
	# receive card
	def receive_card(self, card):
		self.cards.append(card)
	
	def show_info(self):
		tick = '-'
		print(tick*20)
		print("Name: {n} (Dealer)".format(n = self.name))
		print("Hand: {h}".format(h = self.cards)) #TODO format hand better
		print(tick*20)
	
"""
# Global Functions
"""
# create the players
def create_players(p):
	players = []
	random_name_list = ['Muffin','Poop','Fartface','Daipy','Turd','Cake','Skunk']
	buy_in_list = [20,50,100,200,500]
	for i in range(0, p):
		name = raw_input("Enter player {number}'s name:".format(number = i+1))
		if name == "":
			print("Shouldn't have let me choose your name... kek")
			name = random_name_list[i] # TODO: make random
		choose_buy_in = True
		while choose_buy_in:
			try:
				buy = int(raw_input("How much do you want to start with: 20, 50, 100, 200, 500?"))
			except:
				print("Please Enter a number. setting buyin to 100")
				buy = 100
			if buy not in buy_in_list:
				print("Invalid. Choose again")
			else:
				choose_buy_in = False
		tmp = Player(name, buy)
		players.append(tmp)
	return players
	
# output player info to console
def show_player_info(players):
	pnd = '#'
	print(pnd*20)
	print("Players:")
	for player in players:
		player.show_info()
	print(pnd*20)
	
# deal each player, including dealer, two cards
# TODO: better way to iterate list twice aka deal two cards
def initial_deal(players, cards):
	print("Dealing Cards...")
	for player in players:
		card = cards[randint(0,13)]
		player.receive_card(card)
	for player in players:
		card = cards[randint(0,13)]
		player.receive_card(card)

# Rest of Hand after initial deal
def play_hand(players, cards):
	for player in players:
		ask = True
		while ask:
			player.show_info()
			hit_stand = raw_input("Hit or Stand? (h/s")
			if hit_stand.lower() == 'h' or hit_stand.lower() == 'hit':
				card = cards[randint(0,13)]
				player.receive_card(card)
				if player.check_bust():
					print("Player Bust!")
					player.cash = player.cash - 10 # TODO allow bets
					player.show_info()
					ask = False
				else:
					player.show_info()
			elif hit_stand.lower() == 's' or hit_stand.lower() == 'stand':
				print "stand"
				ask = False
			else:
				print("Invalid. Hit 'h' or 's'")
				
# Main Method. Program Starts and Ends Here
if __name__ == "__main__":

	#TODO: This starting setting up game should be in a separate function!!!
	parser = argparse.ArgumentParser(description="Blackjack Terminal Game")
	start = False
	print("Welcome to Blackjack Terminal") # TODO: Better intro
	
	# ask user how many players, can't have more than 5
	while start == False:
		players = int(raw_input("How many players? (up to 5)"))
		# check if not more than 5 players
		if players < 6:
			start = True
		else:
			print("Too many players")
	
	player_list = create_players(players)
	show_player_info(player_list)
	
	# Create the dealer
	random_name_list = ['Paul','George','John','Ringo']
	dealer = Dealer(random_name_list)
	player_list.append(dealer)
	
	
	# TODO: create a 'Deck' which actually gets shuffled and dealed
	cards = [1,2,3,4,5,6,7,8,9,10,10,10,10,11]
	
	# TODO: let them add/delete players here.. aka change game setup
	# Let players join mid game just like real blackjack
	####################################
	# Game Loop
	####################################
	dealer.greeting()
	initial_deal(player_list, cards)
	show_player_info(player_list)
	play_hand(player_list, cards)