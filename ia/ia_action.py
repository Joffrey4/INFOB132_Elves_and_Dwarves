# -*- coding: ascii -*-
import random

def ia_action(player,enemy, data_map):
    """The artificial intelligence of the game. Generate an instruction .

    Parameters:
    -----------
    data_map: the whole database of the game (dict)

    Version:
    --------
    specification: Laurent Emilie and Bienvenu Joffrey v. 1 (02/03/16)
    implementation: Bienvenu Joffrey and Maroit Jonathan v. 1 (21/03/16)
    """
    command = ''
    action_type = ['-a->','-m->']
    used_units = []


    for units in data_map[player]:
        start_x_pos = (('0' + str(units[0]))[-2:])
        start_y_pos = (('0' + str(units[1]))[-2:])
        unit_type = data_map[player][units][0]
        enable_move_x=[0]
        enable_move_y=[0]
        if int(start_x_pos) == 1:
            enable_move_x.append(1)
        elif int(start_x_pos) == data_map['map_size']:
            enable_move_x.append(-1)
        else:
            enable_move_x.append(-1)
            enable_move_x.append(1)

        if int(start_y_pos) == 1:
            enable_move_y.append(1)
        elif int(start_y_pos) == data_map['map_size']:
            enable_move_y.append(-1)
        else:
            enable_move_y.append(-1)
            enable_move_y.append(1)


        if unit_type == 'E':

            for target in data_map[enemy]:

                if (int(start_x_pos) - 2, int(start_y_pos) - 2) <= target <= (int(start_x_pos) + 2, int(start_y_pos) + 2):

                    used_units.append(units)

                    command += str(start_x_pos) + '_' + str(start_y_pos) + ' ' + action_type[0] + ('0'+str(target[0]))[-2:] + '_' + ('0'+str(target[1]))[-2:]+ '   '

            if units not in used_units:

                target_x_pos = int(start_x_pos)+enable_move_x[random.randint(0, (len(enable_move_x)-1))]
                target_y_pos = int(start_y_pos)+enable_move_y[random.randint(0, (len(enable_move_y)-1))]

                if (target_x_pos,target_y_pos) not in data_map[player] and (target_x_pos,target_y_pos) not in data_map[enemy]:
                    print 'done'
                    command += str(start_x_pos) + '_' + str(start_y_pos) + ' ' + action_type[1] +(('0'+str(target_x_pos))[-2:]) + '_' + (('0'+str(target_y_pos))[-2:]) + '   '

        if unit_type == 'D':


            for target in data_map[enemy]:

                if  (int(start_x_pos) - 1, int(start_y_pos) - 1) <= target <= (int(start_x_pos) + 1, int(start_y_pos) + 1):
                    used_units.append(units)
                    command += str(start_x_pos) + '_' + str(start_y_pos) + ' ' + action_type[0] + ('0'+str(target[0])[-2:] + '_' + ('0'+str(target[1]))[-2:] + '   '

            if units not in used_units:

                target_x_pos = int(start_x_pos)+enable_move_x[random.randint(0, (len(enable_move_x)-1))]
                if target_x_pos == int(start_x_pos):
                    target_y_pos = int(start_y_pos)+enable_move_y[random.randint(0, (len(enable_move_y)-1))]
                if (target_x_pos,target_y_pos) not in data_map[player] and (target_x_pos,target_y_pos) not in data_map[enemy]:
                    print 'done'
                    command += str(start_x_pos) + '_' + str(start_y_pos) + ' ' + action_type[1] +(('0'+str(target_x_pos))[-2:]) + '_' + (('0'+str(target_y_pos))[-2:]) + '   '

    return command



