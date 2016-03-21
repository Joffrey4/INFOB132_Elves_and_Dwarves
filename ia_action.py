# -*- coding: ascii -*-
import random

def ia_action(player, data_map):
    """The artificial intelligence of the game. Generate an instruction and execute it.

    Parameters:
    -----------
    data_map: the whole database of the game (dict)

    Version:
    --------
    specification: Laurent Emilie and Bienvenu Joffrey v. 1 (02/03/16)
    implementation: Bienvenu Joffrey v. 1 (21/03/16)
    """
    command = ''
    action_type = {1: '-a->', 2: '-m->'}

    for cell in data_map[player]:
        # Generate the starting position and the kind of action.
        start_x_pos = ('0' + str(cell[0]))[-2:]
        start_y_pos = ('0' + str(cell[1]))[-2:]
        action = action_type[random.randint(1, 2)]

        # Generate the ending position.
        end_x_pos = random.randint(1, data_map['map_size'])
        end_y_pos = random.randint(1, data_map['map_size'])
        command += start_x_pos + '_' + start_y_pos + ' ' + action + end_x_pos + '_' + end_y_pos + '   '

    return command
