# Blackjack Terminal Game
Python 2.7.11

The goal of this project is to create a some what realistic game of Blackjack.
	* Cards, Decks, Shoe
	* Fisher-Yates shuffling algorithm
	* House Rules
	  * Dealer Always stands on 17
	  * Dealer Hits on soft 17
	  * Other rules added after I research
	* Can play with multiple people (even though it is through the command-line)
	
Once the game itself is built and rules implemented correctly, my next goal is to:
	1) Create Bots that can play while you play or play on there own aka as a simulation
		- Each bot will play by a specific set of rules
			-Example: 
				1. Bot Always stay with any hand of 12 or above.
				2. Bot Always hits with any hand below 17
				3. Bot Always hits with any hand below 16
				4. Etc
		- Then the goal is to make a bot that can count cards and adjusts its actions 
		based on the information it has gained through counting cards.

Once the bots are built and running and playing as they should, my next goal is to build 
a database backend.
	1) The main reason behind this is to save the data for all players (bots included) for 
	every hand in every single game they play
		- This will produce a large amount of data that will be great for analyzing which
		strategies perform better than others... I know this information is probably already
		available somewhere but I want to do it for myself.
		- I want to see how well the card counting bot performs
		- I want to later use D3.js to visualize this data in a meaningful way
	
