# -*- coding: ascii -*-


def create_data_ia(map_size=7):
    """Create the ia database.

    Parameters:
    -----------
    map_size: the length of the board game, every unit add one unit to vertical axis and horizontal axis (int, optional)

    Returns:
    --------
    data_ia: the ia database (dict).

    Versions:
    ---------
    specifications: Laurent Emilie v.1 (24/04/16)
    implementation: Laurent Emilie v.1 (24/04/16)
    """
    data_ia = {'ia': {},
               'enemy': {},
               'main_turn': 1,
               'attack_turn':0,
               'map_size': map_size}

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

                    if i == 0:
                        data_ia['ia'][(x_pos, y_pos)] = [unit, life]
                    else:
                        data_ia['enemy'][(x_pos, y_pos)] = [unit, life]

    return data_ia