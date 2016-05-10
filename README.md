# Blackjack Terminal

## Introduction

Play blackjack from terminal by yourself, with friends, or with 'bots'. Blackjack Terminal can also be used to run simulations of 'bots' playing blackjack while saving the statistics from each game.

## Questions
Questions can be sent to joe.pasquantonio@gmail.com

## Issues
Use the [github issue tracker](https://github.com/pasquantonio/blackjack_terminal_game/issues) for bug reports and feature requests.

## Install
#### From Source:
````bash
$ git clone https://github.com/pasquantonio/blackjack_terminal_game.git
$ cd blackjack_terminal_game/
$ cd src/
$ chmod +x blackjack.py
````
Note: The last step 'chmod +x blackjack.py' may not be necessary

## Usage
Navigate to src/ directory
````
usage: blackjack.py [-h] [-p PLAYERS] [-s SHOE] [--house HOUSE] [-b BOTS]
                    [-t TIME] [--minimum MINIMUM] [--maximum MAXIMUM]

Blackjack Terminal: A game for fun or a simulator for putting strategies to
the test

optional arguments:
  -h, --help            show this help message and exit
  -p PLAYERS, --players PLAYERS
                        Number of Human players
  -s SHOE, --shoe SHOE  set how many decks used in the shoe
  --house HOUSE         1: Dealer stand on all 17, 2: Dealer hit on soft 17
  -b BOTS, --bots BOTS  Enter number of bots you want. Up to 7
  -t TIME, --time TIME  Wait time for actions such as deal cards, hit, stand,
                        etc. For simulations do 0, for humans playing do 1.5
  --minimum MINIMUM     Table Minimum Bet
  --maximum MAXIMUM     Table Maximum Bet
````

## Examples
To play by yourself with default settings and no bots
````
$ ./blackjack.py --players 1
````
Play with 3 bots
````
$ ./blackjack.py --players 1 --bots 3
````
Run simulation of 5 bots, minimum bet is 50, maximum bet is 500
````
$ ./blackjack.py --bots 5 --minimum 50 --maximum 500
````

## Project Goals
The goal of this project is to create a some what realistic game of Blackjack.
* Cards, Decks, Shoe
* Fisher-Yates shuffling algorithm
* House Rules
  * Dealer Always stands on 17
  * Dealer Hits on soft 17
  * Other rules added after I research
* Can play with multiple people (even though it is through the terminal-line)

Once the game itself is built and rules implemented correctly, my next goal is to:
1) Create Bots that can play while you play or play on there own aka as a simulation
* Each bot will play by a specific set of rules
  * Example:
    * Bot Always stay with any hand of 12 or above.
    * Bot Always hits with any hand below 17
    * Bot Always hits with any hand below 16
    * Etc
2) Then the goal is to make a bot that can count cards and adjusts its actions based on the information it has gained through
counting cards.

Once the bots are built and running and playing as they should, my next goal is to build
a database backend.
1. The main reason behind this is to save the data for all players (bots included) for every hand in every single game they
play
  * This will produce a large amount of data that will be great for analyzing which strategies perform better than others... I know this information is probably already available somewhere but I want to do it for myself.
  * I want to see how well the card counting bot performs
  * I want to later use D3.js to visualize this data in a meaningful way
