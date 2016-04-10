# -*- coding: ascii -*-


def ia_action(data_map, ia, player):
    """The artificial intelligence of the game. Generate an instruction and return it.

    Parameters:
    -----------
    data_map: the whole database of the game (dict).
    ia: the ia identifier ('player1' or 'player2', string).
    player: the player identifier ('player1' or 'player2', string).

    Return:
    -------
    command: the instruction of the ia (string).

    Version:
    --------
    specification: Laurent Emilie and Bienvenu Joffrey v. 1 (02/03/16)
    implementation: Bienvenu Joffrey and Jonathan Maroit v. 3 (21/03/16)
    """
    command = ''
    unit_type = ['D', 'E']

    # ATTACK PART: Take each ia's unit and each player's unit.
    for unit in data_map[ia]:
        unit_has_attacked_or_moved = False
        for enemy_unit in data_map[player]:

            # If the unit hasn't already find a target, check if the player's unit is in its area.
            if not unit_has_attacked_or_moved:
                for i in range(2):
                    if data_map[ia][unit][0] == unit_type[i] and (unit[0] - (1 + i)) <= enemy_unit[0] <= (unit[0] + (1 + i)) and (unit[1] - (1 + i)) <= enemy_unit[1] <= (unit[1] + (1 + i)):

                        # Write the attack.
                        command += ('0' + str(unit[0]))[-2:] + '_' + ('0' + str(unit[1]))[-2:] + ' -a-> ' + ('0' + str(enemy_unit[0]))[-2:] + '_' + ('0' + str(enemy_unit[1]))[-2:] + '   '
                        unit_has_attacked_or_moved = True

        # MOVE PART: Check if the unit hasn't attacked yet.
        if not unit_has_attacked_or_moved:
            target_cell = []

            # Generate a list with the allowed cell to move of the unit.
            for x_pos in range(unit[0] - 1, unit[0] + 2):
                for y_pos in range(unit[1] - 1, unit[1] + 2):
                    target_cell.append(x_pos, y_pos)

            # For each generated cell, check if the cell is free and if the unit can move.
            for cell in target_cell:
                if not unit_has_attacked_or_moved and cell not in data_map[ia]:
                    if (data_map[ia][unit][0] == 'D' and abs(cell[0] - unit[0]) + abs(cell[1] - unit[1]) == 1) or data_map[ia][unit][0] == 'E':

                        # Write the move.
                        command += ('0' + str(unit[0]))[-2:] + '_' + ('0' + str(unit[1]))[-2:] + ' -m-> ' + ('0' + str(cell[0]))[-2:] + '_' + ('0' + str(cell[1]))[-2:] + '   '
                        unit_has_attacked_or_moved = True

    return command


