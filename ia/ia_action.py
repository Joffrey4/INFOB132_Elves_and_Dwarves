# -*- coding: ascii -*-
import random


def ia_action(player, data_map):
    """The artificial intelligence of the game. Generate an instruction and execute it.

    Parameters:
    -----------
    data_map: the whole database of the game (dict)

    Returns:
    --------
    command: commands to execute to play (str)

    Version:
    --------
    specification: Laurent Emilie and Bienvenu Joffrey v. 1 (02/03/16)
    implementation: Bienvenu Joffrey and Maroit Jonathan v. 1 (21/03/16)
    """
    command = ''
    action_type = ['-a->','-m->']
    operation = { 1: + , 2: -}


    for units in data_map[player]:
        start_x_pos = ('0' + str(units[0]))[-2:]
        start_y_pos = ('0' + str(units[1]))[-2:]
        unit_type = data_map[player][units][0]

        if unit_type == 'E':
            for target in data_map[enemy]:
                if (start_x_pos- 2, start_y_pos - 2) <= target<= (start_x_pos + 2, start_y_pos + 2) and target not in data_map[player]:
                    command += str(start_x_pos) + '_' + str(start_y_pos) + ' ' + action_type[0] + ('0'+str(target)[0])[-2:] + '_' + ('0'+str(target[1]))[-2:] + '   '
                elif (start_x_pos- 2, start_y_pos - 2) >= target >= (start_x_pos + 2, start_y_pos + 2) and target not in data_map[player]:
                    command += str(start_x_pos) + '_' + str(start_y_pos) + ' ' + action_type[1] + str(start_x_pos+operation[random.randint(1,2)+random.randint(0,1)]) + '_' + str(start_y_pos+operation[random.randint(1,2)+random.randint(0,1)]) + '   '




    return command
ia_action('player1',data_map)
print 'rrr'
