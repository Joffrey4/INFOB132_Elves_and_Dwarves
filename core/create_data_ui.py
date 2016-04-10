# -*- coding: utf-8 -*-
from colorama import Fore, Back, Style


# FONCTIONNE UNIQUEMENT AVEC UN TABLEAU DE 20x20
def display_map(data_map):
    """Display the map of the game.

    Parameters:
    -----------
    data_map: the whole database of the game (dict)

    Version:
    --------
    specification: Laurent Emilie v.1 (12/02/16)
    implementation: Bienvenu Joffrey v.3 (01/04/16)
    """
    clear_output()

    # Check which player have to play and define displaying constants.
    player = 'player' + str((data_map['main_turn'] % 2) + 1)
    ui_color = data_map[player + 'info'][0]

    data_cell = {'ui_color': ui_color}

    # Generate the units to be displayed.
    for i in range(1, data_map['map_size'] + 1):
        for j in range(1, data_map['map_size'] + 1):

            # Coloration black/white of the cells.
            background_cell = ''
            if (i + j) % 2 == 0:
                background_cell = Back.WHITE

            if (i, j) in data_map['player1']:
                data_cell['(' + str(i) + ',' + str(j) + ')'] = data_map['player1'][(i, j)][1] + background_cell + ' ☻' + str(data_map['player1'][(i, j)][0]) + (str(data_map['player1'][(i, j)][2]) + ' ')[:2]
            elif (i, j) in data_map['player2']:
                data_cell['(' + str(i) + ',' + str(j) + ')'] = data_map['player2'][(i, j)][1] + background_cell + ' ☻' + str(data_map['player2'][(i, j)][0]) + (str(data_map['player2'][(i, j)][2]) + ' ')[:2]
            else:
                data_cell['(' + str(i) + ',' + str(j) + ')'] = background_cell + (' ' * 5)

    # Generate the statistics to be displayed.
    player1_cell = data_map['player1'].keys()
    cell1_couter = 0
    player2_cell = data_map['player2'].keys()
    cell2_couter = 0
    unit_name = {'E': 'Elf', 'D': 'Dwarf'}

    for i in range(1, 5):
        for j in range(1, 3):
            data_cell['stat' + str(i) + str(j)] = (('0' + str(player1_cell[cell1_couter][0]))[-2:] + '-' + ('0' + str(player1_cell[cell1_couter][1]))[-2:] + ' ' + unit_name[data_map['player1'][player1_cell[cell1_couter]][0]] + ' hp: ' + str(data_map['player1'][player1_cell[cell1_couter]][2]) + ' ' * 20)[:20]
            cell1_couter += 1
        for j in range(3, 5):
            data_cell['stat' + str(i) + str(j)] = (('0' + str(player2_cell[cell2_couter][0]))[-2:] + '-' + ('0' + str(player2_cell[cell2_couter][1]))[-2:] + ' ' + unit_name[data_map['player2'][player2_cell[cell2_couter]][0]] + ' hp: ' + str(data_map['player2'][player2_cell[cell2_couter]][2]) + ' ' * 20)[:20]
            cell2_couter += 1

    # Generate the title of the map to be displayed.
    data_cell['turn'] = str(data_map['main_turn']/2 + 1)
    data_cell['playername'] = data_map[player + 'info'][1]
    data_cell['blank'] = ((data_map['map_size'] * 5) - 19 - len(data_cell['turn']) - len(data_cell['playername'])) * ' '

    # Print the top of the UI.
    for line in data_map['data_ui']:
        print line % data_cell
