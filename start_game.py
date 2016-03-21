def start_game(player1 ='player 1',player2 ='AI', map_size = 7, file_name = None, sound = False):
	"""Start the entire game.
	
	Parameters:
	-----------
	player1: Name of the first player (str)
	player2: Name of the second player or AI (str)
	map_size: Size of the map that players wanted to play with (int)
	file_name: File of the name to load if necessary (str)
	sound: Activate the sound or not (bool)
	
	Notes:
	------
	It is the main function that gonna call the other functions.
	map_size must be contained between 7 and 30
	file_name load a game only if the game was saved earlier
	
	Version:
	-------
	specification: Laurent Emilie & Maroit Jonathan v.1 (10/03/16)
	implementation: 
	"""
	#creation of the database
	data_map, data_ui = create_data_map(map_size, player1, player2)
	
	#diplay introduction event
	event_display(player,player_name,'intro')
	
	#start game by asking commands to players
	while (data_map[player1E].keys() =! [] and data_map[player1D].keys() != []) or (data_map[player2E].keys() != [] and data_map[player2D].keys() != []):
		choose_action(data_map)
	
	