# -*- coding: ascii -*-

def is_not_game_ended(data_map):
	"""Check if the game is allow to continue.

	Paremeter:
	----------
	data_map: the whole database (dict)

	Returns:
	--------
	continue_game : booleen value who said if the game need to continue(bool)
	loser : the player who lose the game(str)
	winner : the player who won the game(str)
	Notes:
	------
	The game stop when is player run out of unit or if 20 turn have been played without an attack, in this case the first player lose
	Version:
    -------
    specification: Maroit Jonathan(v.1 21/03/16)
    implementation: Maroit Jonathan (v.1 21/03/16)
	"""

	continue_game = True

	if not(len(data_map['player1']):
        loser = 'player 1'
		winner = 'player 2'
		continue_game = False

	elif not(len(data_map['player2']):
		loser = 'player 2'
		winner = 'player 1'
		continue_game = False

	elif attack_turn >= 20:
		loser = 'player 1'
		winner = 'player 2'
		continue_game = False

	return continue_game,loser,winner