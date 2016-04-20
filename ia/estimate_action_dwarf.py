# -*- coding: ascii -*-


def estimate_action_dwarf(data_ia, build_formation, are_enemy, where_enemies):
    """Estimate which is the best action whether the unit is a dwarf.

    Parameters:
    -----------
    data_ia: the whole database (dict)
    build_formation: tells whether the situation requieres to build the formation (bool)
    are_enemy: tells whether there are enemy in the surroundings (bool)
    where_enemies: position of the enemy's units (list)

    Returns:
    --------
    start_coord: ia's unit will do action coordinates format xx_xx (str)
    end_coord: coordinates of attacked unit or to end the movement format xx_xx (str)

    Versions:
    ---------
    specification: Laurent Emilie v1 (19/04/16)
    implementation:
    """
