# -*- coding: ascii -*-


def ia_reflexion(data_ia, data_map):
    """Brain of the Artificial Intelligence.

    Parameters:
    -----------
    ia_data: the whole database (dict)

    Returns:
    --------
    action_type_formation: actions with number of points for the group (dict)
    action_type_elf: actions with number of points for each elf (dict)
    action_type_dwarf: actions with number of points for each dwarf (dict)

    Versions:
    ---------
    specification: Bienvenu Joffrey & Laurent Emilie v.1 (20/04/16)
    implementation:
    """
    commands = []

    unit_has_attacked = 0
    for ia_unit in data_ia['ia']:
        for enemy_unit in data_ia['enemy']:

            # Find each possible target for the Elves.
            unit_targets = []
            if data_ia['ia'][ia_unit][0] == 'E':
                for i in range(2):
                    if (ia_unit[0] - (1 + i)) <= enemy_unit[0] <= (ia_unit[0] + (1 + i)) and (ia_unit[1] - (1 + i)) <= enemy_unit[1] <= (ia_unit[1] + (1 + i)):
                        # Add the unit to the target list.
                        unit_targets.append(enemy_unit)

            # Find each possible target for the Dwarves.
            else:
                if (ia_unit[0] - 1) <= enemy_unit[0] <= (ia_unit[0] + 1) and (ia_unit[1] - 1) <= enemy_unit[1] <= (ia_unit[1] + 1):
                    # Add the unit to the target list.
                    unit_targets.append(enemy_unit)

        # Find the weakest units.
        target = unit_targets[0]
        for enemy_unit in unit_targets:
            if data_ia['enemy'][enemy_unit][0] == 'D' or data_ia['enemy'][enemy_unit][1] < data_ia['enemy'][target][1]:
                target = enemy_unit

        # Write the attack.
        commands.append([ia_unit, ' -a-> ', target])
        unit_has_attacked += 1

    # Find the weakest of all enemy's units.
    if not (unit_has_attacked and data_map['remote'] == 2):
        target_list = data_ia['enemy'].keys()
        target = target_list[0]

        for enemy_unit in data_ia['enemy']:
            if data_ia['enemy'][enemy_unit][0] == 'D' or data_ia['enemy'][enemy_unit][1] < data_ia['enemy'][target][1]:
                target = enemy_unit

        # Write the move
        for ia_unit in data_ia['ia']:
            commands.append([ia_unit, ' -m-> ', target])

    return commands
