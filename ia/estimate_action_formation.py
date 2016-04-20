# -*- coding: ascii -*-


def estimate_action_formation(data_ia, are_enemy, where_enemies, formation_scheme):
    """Estimate whether our units have to keep the formation or to rebuild it.

    Parameters:
    -----------
    data_ia: the whole database (dict)
    are_enemy: tells whether there are enemy in the surroundings (bool)
    where_enemies: position of the enemy's units (list)
    formation_scheme: file with the different situation of formation format .pkl (file)

    Returns:
    --------
    build_formation: tells whether the situation requieres to build the formation (bool)

    Versions:
    ---------
    specification: Laurent Emilie v1 (19/04/16)
    implementation:
    """
