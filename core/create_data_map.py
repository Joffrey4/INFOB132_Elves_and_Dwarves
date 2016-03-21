# -*- coding: ascii -*-
from colorama import Fore


def create_data_map(map_size=7, name_player1='Benoit', name_player2='Isaac'):
    """ Create a dictionary that the game will use as database.

    Parameters:
    ----------
    map_size : the lenght of the board game, every unit add one unit to vertical axis and horizontal axis (int, optional)

    Returns:
    -------
    data_map : dictionary that contain information's of every cells of the board(dict)
    data_ui : list with data to display the ui (list of strings)

    Notes:
    -----
    The game board is a square, the size must be a positive integer, minimum 7 and maximum 30 units,
    or the game will be stopped after 20 turns if nobody attack

    Version:
    -------
    specification: Maroit Jonathan & Bienvenu Joffrey (v.1.1 04/03/16)
    implementation: Maroit Jonathan & Bienvenu Joffrey (v.3 04/03/16)
    """

    # Initialisation of variables
    data_map = {'player1E': {},
                'player1D': {},
                'player1info': [],
                'player2E': {},
                'player2D': {},
                'player2info': [],
                'main_turn': 1,
                'attack_turn': 0}

    # Place units to their initial positions.
    player_data = [Fore.BLUE, Fore.RED, name_player1, name_player2]
    for i in range(2):
        for line in range(1, 4):
            for column in range(1, 4):
                unit = 'E'
                life = 4

                if line >= 2 and column >= 2:
                    unit = 'D'
                    life = 10

                if line + column != 6:
                    x_pos = abs(i * map_size - line + i)
                    y_pos = abs(i * map_size - column + i)

                    data_map['player' + str(i + 1) + unit][(x_pos, y_pos)] = [unit, player_data[i], life]
        data_map['player' + str(i + 1) + 'info'].extend([player_data[i], player_data[i + 2]])

    return data_map
