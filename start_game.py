# -*- coding: ascii -*-


def start_game(player1='player 1', player2='AI', map_size=7, file_name=None, sound=False, clear=False):
    """Start the entire game.
    Parameters:
    -----------
    player1: Name of the first player (str).
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
        data_map = create_data_map(map_size, player1, player2, clear)

    # Diplay introduction event and the map.
    event_display(data_map, 'intro')
    # Run de game turn by turn
    continue_game, loser, winner = is_not_game_ended(data_map)
    while continue_game:
        display_map(data_map, clear)
        data_map = choose_action(data_map)
        save_data_map(data_map)

    # Find the loser and the winner for the end game event.
    continue_game, loser, winner = is_not_game_ended()

    # Display the game-over event (versus IA).
    if player1 == 'IA' or player2 == 'IA':
        player = loser
        event_display(data_map, 'game_over', player)
    # Display the win event (versus real player).
    else:
        player = winner
        event_display(data_map, 'win', player)