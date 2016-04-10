# -*- coding: ascii -*-


def start_game(player1='player 1', player2='AI', map_size=7, file_name=None, sound=False):
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
    implementation: Maroit Jonathan v.1 (21/03/16)
    """
    # Creation of the database or load it.
    if file_name:
        data_map = load_map()
    else:
        data_map = create_data_map(map_size, player1, player2)

    # Diplay introduction event and the map.
    play_event(sound, player, player_name, 'intro') #None has been replaced by player and player_name. TODO: initialize player and player _name !
    # Run de game turn by turn
    continue_game = is_not_game_ended(data_map)
    while continue_game:
        display_map(data_map)
        data_map = choose_action(data_map)
        save_data_map(data_map)

    # Find the loser and the winner for the end game event.
    continue_game, loser, winner = is_not_game_ended()

    # Display the game-over event (versus IA).
    if player1 == 'IA' or player2 == 'IA':
        play_event(sound, loser, data_map[str(loser + 'info')][1], 'game_over')
    # Display the win event (versus real player).
    else:
        play_event(sound, winner, data_map[str(winner + 'info')][1], 'win')
