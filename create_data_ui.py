# -*- coding: ascii -*-
from colorama import Fore, Back, Style


def create_data_ui(map_size):

    data_ui = []
    #Conditionne la taille du tableau à 10 lignes minimum -> Laisse de l'espace pour les statistiques.
    min_size = 10
    if map_size >= min_size:
        min_size = map_size

    #cell_size, multiplicateur qui permet d'allonger les cellules du damier.
    cell_sizer = ((map_size -1)/ 10) +1

    #board_width, longueur (en caractères) du damier.
    board_width = (3 + cell_sizer) * map_size

    #Initialisation des variables d'affichage.
    LINE_COLORED = ui_color + ('█' * 130) + Style.RESET_ALL
    LINE_BLACK = Back.BLACK + ' ' * (board_width + 9) + Style.RESET_ALL
    BORDER_COLORED = ui_color + '███' + ('█' * 2 * cell_sizer) + Style.RESET_ALL
    BORDER_BLACK = Back.BLACK + '  ' + Style.RESET_ALL
    LINE_FILL = ui_color + (127 - (board_width + 12 + (4 * cell_sizer))) * '█' + Style.RESET_ALL
    LINE_BLANK = ui_color + (127 - (board_width + 35 + (4 * cell_sizer))) * '█' + Style.RESET_ALL

    #Enregistrement - haut de l'ui, lignes colorées.
    for i in range(3):
        data_ui[i] =  ui_color + ('█' * 130) + Style.RESET_ALL

    #Enregistrement - haut de l'ui, bord supérieur des cadres.
    turn_message = 'Tour %s - %s, à vous de jouer ! %s'
    colored_turn_line = Fore.WHITE + Back.BLACK + turn_message + Style.RESET_ALL + Back.BLACK + ' ' * (board_width + 7 - len(turn_message)) + Style.RESET_ALL
    colored_stats_line = BORDER_BLACK + Fore.WHITE + Back.BLACK + 'Statistiques:' + Style.RESET_ALL + Back.BLACK + (' ' * 5) + Style.RESET_ALL + BORDER_BLACK
    data_ui[3] = BORDER_COLORED + BORDER_BLACK + colored_turn_line + BORDER_BLACK + BORDER_COLORED + colored_stats_line + LINE_FILL

    #Enregistrement - haut du damier et titre "Elves".
    elves_subtitle = 'Elves:' + ' ' * 13
    data_ui[4] = BORDER_COLORED + BORDER_BLACK + ' ' * (board_width +5) + BORDER_BLACK + BORDER_COLORED + BORDER_BLACK + elves_subtitle + BORDER_BLACK + LINE_FILL

    #Enregistrement - damier
    for line in range(1, min_size + 1):
        if line <= map_size:
            data_ui[line + 5] = BORDER_COLORED + BORDER_BLACK + Fore.BLACK + ('0' + str(line))[-2:] + ' ' + Style.RESET_ALL
            data_ui[line + 5] += '%s  ' + BORDER_BLACK + BORDER_COLORED

        if line <= 10:

    return data_ui