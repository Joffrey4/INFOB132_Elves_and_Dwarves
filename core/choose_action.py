# -*- coding: ascii -*-


def choose_action(data_map):
    """Ask and execute the instruction given by the players to move or attack units.

    Parameters:
    ----------
    data_map: the whole database (dict)

    Returns:
    -------
    data_map: the database changed by moves or attacks (dict)

    Notes:
    -----
    Instructions must be in one line, with format xx_xx -a-> xx_xx for an attack and xx_xx -m-> xx_xx for a movement.

    Version:
    -------
    specification: Laurent Emilie v.1 (11/02/16)
    implementation: Laurent Emilie v.3 (21/03/16)
    """

    player = 'player' + str((data_map['main_turn'] % 2) + 1)
    enemy = 'player' + str(2 - (data_map['main_turn'] % 2))


    print 'It is the turn of %s' % (data_map[str(player) + '_info'][1])

    # AJOUTER IF POUR DEFINIR SI PLAYER OU IA JOUE.
    if data_map[str(player+'_info')][1] == 'IA':
        game_instruction = ia_action(player, data_map)
    # APPELE IA_ACTION
    else:
        game_instruction = raw_input(player + 'enter your commands in format xx_xx -a-> xx_xx or xx_xx -m-> xx_xx')

    # Split commands string by string.
    list_action = game_instruction.split('   ')

    # Call attack_unit or move_unit in function of instruction.
    for i in range(len(list_action)):
        if '-a->' in list_action[i]:
            attack_unit(data_map, (int(list_action[i][0][:2]), int(list_action[i][0][3:])),
                        (int(list_action[i][2][:2]), int(list_action[i][2][3:])), player, enemy)
        elif '-m->' in list_action[i]:
            move_unit(data_map, (int(list_action[i][0][:2]), int(list_action[i][0][3:])),
                      (int(list_action[i][2][:2]), int(list_action[i][2][3:])), player)

    data_map['main_turn'] += 1

    display_map(data_map, map_size)
