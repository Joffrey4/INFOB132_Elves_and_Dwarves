# -*- coding: ascii -*-


def ia_action(data_map, data_ia):
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
    raw_commands = ia_reflexion(data_ia, data_map)

    commands = ''
    for command in raw_commands:


    return command


