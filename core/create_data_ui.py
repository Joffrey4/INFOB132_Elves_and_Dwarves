# -*- coding: ascii -*-
from colorama import Fore, Back, Style


def create_data_ui(data_map):
    data_ui = [[]] * (17 + data_map['map_size'])

    # Initialisation of the displaying constants.
    grid_size = 5 * data_map['map_size']
    ui_color = '{1}'

    line_coloured = ui_color + ('█' * 130) + Style.RESET_ALL
    border_black = Back.BLACK + '  ' + Style.RESET_ALL

    border_coloured_left = ui_color + ('█' * 9) + Style.RESET_ALL
    border_coloured_right = ui_color + ('█' * 9) + Style.RESET_ALL
    border_coloured_middle = ui_color + (' ' * 8) + Style.RESET_ALL

    border_white = ' ' * 4

    # Generate and save the top of the UI.
    for i in range(3):
        data_ui[i] = line_coloured

    # Generate and save the top of the grid.
    turn_message = 'Turn {2} - {3}, it\'s up to you ! {4}'
    data_ui[3] = border_coloured_left + Fore.WHITE + Back.BLACK + '  ' + turn_message + '  ' + Style.RESET_ALL + border_coloured_right
    data_ui[4] = border_coloured_left + border_black + ' ' * (grid_size + 6) + border_black + border_coloured_right

    # Generate and save the architecture of the grid.
    for line in range(1, data_map['map_size'] + 1):
        data_ui[line + 5] = border_coloured_left + border_black + Fore.BLACK + ('0' + str(line))[-2:] + ' ' + Style.RESET_ALL + '{2}' + '   ' + border_black + border_coloured_right

    # Generate and save the foot of the grid.
    data_ui[data_map['map_size'] + 5] = border_coloured_left + border_black + Fore.BLACK + '   '
    for i in range(1, data_map['map_size'] + 1):
        data_ui[data_map['map_size'] + 5] += '  ' + ('0' + str(i))[-2:] + ' '
    data_ui[data_map['map_size'] + 5] += '  ' + border_black + border_coloured_right

    data_ui[data_map['map_size'] + 6] = border_coloured_left + Back.BLACK + (grid_size + 10) * ' ' + Style.RESET_ALL + border_coloured_right

    # Generate and save the top of the statistics.
    data_ui[data_map['map_size'] + 7] = line_coloured

    data_ui[data_map['map_size'] + 8] = border_coloured_left + Fore.WHITE + Back.BLACK + '  Your units:' + (' ' * 39) + Style.RESET_ALL + border_coloured_middle
    data_ui[data_map['map_size'] + 8] = Fore.WHITE + Back.BLACK + '  Opponent\'s units:' + (' ' * 33) + Style.RESET_ALL + border_coloured_right

    # Generate and save the content of the statistics.
    for i in range(4):
        data_ui[data_map['map_size'] + 9 + i] = border_coloured_left + border_black + border_white + '{2}' + border_white + '{3}' + border_white + border_black + border_coloured_middle
        data_ui[data_map['map_size'] + 9 + i] += border_black + border_white + '{4}' + border_white + '{5}' + border_white + border_black + border_coloured_right

    # Generate and save the foot of the statistics.
    data_ui[data_map['map_size'] + 13] = border_coloured_left + Back.BLACK + (' ' * 50) + Style.RESET_ALL + border_coloured_middle
    data_ui[data_map['map_size'] + 13] = Back.BLACK + (' ' * 50) + Style.RESET_ALL + border_coloured_right

    for i in range(2):
        data_ui[data_map['map_size'] + 14 + i] = line_coloured

    return data_ui
