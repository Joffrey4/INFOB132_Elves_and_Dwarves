# coding=utf-8
from colorama import Fore, Back, Style
import pyaudio
import wave
#from IPython.display import clear_output
import time
import random

import pickle
import socket



def get_IP():
    """Returns the IP of the computer where get_IP is called.

    Returns
    -------
    computer_IP: IP of the computer where get_IP is called (str)

    Notes
    -----
    If you have no internet connection, your IP will be 127.0.0.1.
    This IP address refers to the local host, i.e. your computer.

    """

    return socket.gethostbyname(socket.gethostname())


def connect_to_player(player_id, remote_IP='127.0.0.1', verbose=False):
    """Initialise communication with remote player.

    Parameters
    ----------
    player_id: player id of the remote player, 1 or 2 (int)
    remote_IP: IP of the computer where remote player is (str, optional)
    verbose: True only if connection progress must be displayed (bool, optional)

    Returns
    -------
    connection: sockets to receive/send orders (tuple)

    Notes
    -----
    Initialisation can take several seconds.  The function only
    returns after connection has been initialised by both players.

    Use the default value of remote_IP if the remote player is running on
    the same machine.  Otherwise, indicate the IP where the other player
    is running with remote_IP.  On most systems, the IP of a computer
    can be obtained by calling the get_IP function on that computer.

    """

    # init verbose display
    if verbose:
        print '\n-------------------------------------------------------------'

    # open socket (as server) to receive orders
    socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # deal with a socket in TIME_WAIT state

    if remote_IP == '127.0.0.1':
        local_IP = '127.0.0.1'
    else:
        local_IP = get_IP()
    local_port = 42000 + (3-player_id)

    if verbose:
        print 'binding on %s:%d to receive orders from player %d...' % (local_IP, local_port, player_id)
    socket_in.bind((local_IP, local_port))

    socket_in.listen(1)
    if verbose:
        print '   done -> now waiting for a connection on %s:%d\n' % (local_IP, local_port)

    # open client socket used to send orders
    socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # deal with a socket in TIME_WAIT state

    remote_port = 42000 + player_id

    connected = False
    msg_shown = False
    while not connected:
        try:
            if verbose and not msg_shown:
                print 'connecting on %s:%d to send orders to player %d...' % (remote_IP, remote_port, player_id)
            socket_out.connect((remote_IP, remote_port))
            connected = True
            if verbose:
                print '   done -> now sending orders to player %d on %s:%d' % (player_id, remote_IP, remote_port)
        except:
            if verbose and not msg_shown:
                print '   connection failed -> will try again every 100 msec...'
            time.sleep(.1)

            msg_shown = True

    if verbose:
        print

    # accept connection to the server socket to receive orders from remote player
    print 'sutck on accept'
    socket_in, remote_address = socket_in.accept()
    if verbose:
        print 'now listening to orders from player %d' % (player_id)

    # end verbose display
    if verbose:
        print '\nconnection to remote player %d successful\n-------------------------------------------------------------\n' % player_id

    # return sockets for further use
    return (socket_in, socket_out)


def disconnect_from_player(connection):
    """End communication with remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (tuple)

    """

    # get sockets
    socket_in = connection[0]
    socket_out = connection[1]

    # shutdown sockets
    socket_in.shutdown(socket.SHUT_RDWR)
    socket_out.shutdown(socket.SHUT_RDWR)

    # close sockets
    socket_in.close()
    socket_out.close()


def notify_remote_orders(connection, orders):
    """Notifies orders of the local player to a remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (tuple)
    orders: orders of the local player (str)

    Raises
    ------
    IOError: if remote player cannot be reached

    """

    # get sockets
    socket_in = connection[0]
    socket_out = connection[1]

    # deal with null orders (empty string)
    if orders == '':
        orders = 'null'

    # send orders
    try:
        socket_out.sendall(orders)
    except:
        raise IOError, 'remote player cannot be reached'


def get_remote_orders(connection):
    """Returns orders from a remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (tuple)

    Returns
    ----------
    player_orders: orders given by remote player (str)

    Raises
    ------
    IOError: if remote player cannot be reached

    """

    # get sockets
    socket_in = connection[0]
    socket_out = connection[1]

    # receive orders
    try:
        orders = socket_in.recv(4096)
    except:
        raise IOError, 'remote player cannot be reached'

    # deal with null orders
    if orders == 'null':
        orders = ''

    return orders



#======================================================================================================================
#======================================================================================================================
#======================================================================================================================
#======================================================================================================================

def start_game(remote=1, player1='player 1', player2='player_2', map_size=7, file_name=None, sound=False, clear=False):
    """Start the entire game.
    Parameters:
    -----------
    player1: Name of the first player or IA (optional, str).
    player2: Name of the second player or IA (optional, str).
    map_size: Size of the map that players wanted to play with (optional, int).
    file_name: File of the name to load if necessary (optional, str).
    sound: Activate the sound or not (optional, bool).
    clear: Activate the "clear_output" of the notebook. Game looks more realistic, but do not work properly on each computer (optional, bool).
    Notes:
    ------
    It is the main function that gonna call the other functions.
    map_size must be contained between 7 and 30
    file_name load a game only if the game was saved earlier
    Version:
    -------
    specification: Laurent Emilie & Maroit Jonathan v.1 (10/03/16)
    implementation: Maroit Jonathan & Bienvenu Joffrey v.1(21/03/16)
    """
    # Creation of the database or load it.
    if file_name:
        data_map = load_data_map()
    else:
        data_map = create_data_map(remote, map_size, player1, player2, clear)

    # If we play versus another ia, connect to her.
    if remote:
        connection = connect_to_player(remote)
        data_ia = create_data_ia(map_size)
    else:
        connection = None
        data_ia = None

    # Diplay introduction event and the map.
    event_display(data_map, 'intro')

    # Run de game turn by turn
    continue_game = True
    while continue_game:
        display_map(data_map, clear)
        data_map = choose_action(data_map, connection, data_ia)
        save_data_map(data_map)
        continue_game, loser, winner = is_not_game_ended(data_map)

    # Once the game is finished, disconnect from the other player.
    if remote:
        disconnect_from_player(connection)

    # Display the game-over event (versus IA).
    if player1 == 'IA' or player2 == 'IA':
        player = loser
        event_display(data_map, 'game_over', player)
    # Display the win event (versus real player).
    else:
        player = winner
        event_display(data_map, 'win', player)

def play_event(sound, player, player_name, event):
    """Play a selected sound
    Parameters:
    -----------
    sound: argument who active or deactivate the sound, true or false (bool)
    sound_name:the name of the sound file that will be played (str)
    Versions:
    ---------
    spécification: Maroit Jonathan (v.1 17/02/16)
    implémentation: Maroit Jonathan(v.1 17/02/16)
    """
    if sound:
        sound_name = event + '.wav'
        chunk = 1024
        wf = wave.open(sound_name, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)

        data = wf.readframes(chunk)
        time_count = 0
        count_line = 0

        while data != '':
            time_count += 1
            if time_count == 18:
                time_count = 0
                event_display(player, player_name, event) #Cannot have 4 arguments, count_line has been deleted.
                count_line += 1
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
    else:
        for count_line in range(20):
            event_display(player, player_name, event)
            time.sleep(0)
    time.sleep(2)
    #clear_output()

def event_display(data_map, event, player=0):
    """Print a line of the screen which representst the actualy situation with the name of the concerned player.

    Parameters:
    -----------
    data_map: the whole database (dict)
    event : the event who represent the situation ; introduction , game over or winner screen (str)
    player: which player has an event to display (int, optional)

    Version:
    -------
    specification: Maroit Jonathan and Laurent Emilie (v.2 03/04/16)
    implementation: Maroit Jonathan (v.1 16/02/16)
    """

    if event == 'intro':

        l0 = '                                                                                                                                '
        l1 = '    ██████  ████                                     ███            ████                                                        '
        l2 = '    ██        ██                                    ██ ██           ██ ██                                                       '
        l3 = '    ██        ██    ██  ██   ████    █████          ██ ██           ██  ██  ██   ██  ████   ██  ██  ██  ██   ████    █████      '
        l4 = '    ██        ██    ██  ██  ██  ██  ██               ███            ██  ██  ██ █ ██     ██  ██ ███  ██  ██  ██  ██  ██          '
        l5 = '    █████     ██    ██  ██  ██  ██  ██              ██              ██  ██  ██ █ ██     ██  ███     ██  ██  ██  ██  ██          '
        l6 = '    ██        ██    ██  ██  ██████   ████           ██ ████         ██  ██  ██ █ ██  █████  ██      ██  ██  ██████   ████       '
        l7 = '    ██        ██    ██  ██  ██          ██          ██  ██          ██  ██  ██ █ ██ ██  ██  ██      ██  ██  ██          ██      '
        l8 = '    ██        ██     ████   ██          ██          ██  ██          ██ ██    ██ ██  ██  ██  ██       ████   ██          ██      '
        l9 = '    ██████  ██████    ██     ████   █████            ███ ██         ████     ██ ██   █████  ██        ██     ████   █████       '
        l10 = '                                                                                                                                '
        l11 = '                        GROUPE 42 : EMILIE LAURENT, JOFFREY BIENVENU, JONATHAN MAROIT ET SYLVAIN PIRLOT                         '

        line_list = [l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11]
        final_list = []

        for line in line_list:
            if line == l11:
                print (Fore.BLACK + Back.YELLOW + line)
            elif line == l0 or line == l10:
                print (Fore.BLACK + Back.BLACK + line)
            else:
                print (Fore.YELLOW + Back.BLACK + line)

            time.sleep(0.5)
        time.sleep(4)
        #clear_output()

    else:
        player_name = data_map[player + 'info'][1]

        if len(player_name) < 9:
            player_name += (9 - len(player_name)) * ' '
        player_name = player_name[0:9]
        color_player = Back.RED
        if player == 'player1':
            color_player = Back.BLUE


        if event == 'game_over':
            d0 = (Fore.BLACK + Back.WHITE) + '                             ' + (
            'The loser is: ' + player_name) + '                        '
            d1 = '████████████        ████████████████████████████████████        ████████████'
            d2 = '████████████        ████████████████████████████████████        ████████████'
            d3 = '████████████████████    ████                    ████    ████████████████████'
            d4 = '████████████████████    ████                    ████    ████████████████████'
            d5 = '████████████████████████                            ████████████████████████'
            d6 = '████████████████████████    ████████    ████████    ████████████████████████'
            d7 = '████████████████████████    ████████    ████████    ████████████████████████'
            d8 = '████████████████████████    ████████    ████████    ████████████████████████'
            d9 = '████████████████████████    ████            ████    ████████████████████████'
            d10 = '████████████████████████    ████            ████    ████████████████████████'
            d11 = '████████████████████████            ████            ████████████████████████'
            d12 = '████████████████████████            ████            ████████████████████████'
            d13 = '████████████████████    ████                    ████    ████████████████████'
            d14 = '████████████████████    ████                    ████    ████████████████████'
            d15 = '████████████        ████████    ████    ████    ████████        ████████████'
            d16 = '████████████        ████████    ████    ████    ████████        ████████████'
            d17 = (Fore.BLACK + Back.WHITE) + '                                                                            '
            death_list = [d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17]

            for line in death_list:
                print (Fore.BLACK + color_player + line)
                time.sleep(0.5)

        else:
            w0 = Back.BLACK + Fore.WHITE + '                          THE                           '
            wa = '                                                        '
            w1 = '     ██   ██  ████   ██   ██ ██   ██ ██████  █████      '
            w2 = '     ██   ██   ██    ██   ██ ██   ██ ██      ██  ██     '
            w3 = '     ██   ██   ██    ███  ██ ███  ██ ██      ██  ██     '
            w4 = '     ██ █ ██   ██    ████ ██ ████ ██ ██      ██  ██     '
            w5 = '     ██ █ ██   ██    ██ ████ ██ ████ █████   █████      '
            w6 = '     ██ █ ██   ██    ██  ███ ██  ███ ██      ██ ██      '
            w7 = '      ██ ██    ██    ██   ██ ██   ██ ██      ██  ██     '
            w8 = '      ██ ██    ██    ██   ██ ██   ██ ██      ██  ██     '
            w9 = '      ██ ██   ████   ██   ██ ██   ██ ██████  ██  ██     '
            wb = '                                                        '
            w10 = Back.BLACK + Fore.WHITE + '                          IS                            '
            w11 = (Fore.WHITE + Back.BLACK) + '                        ' + player_name + '                       '
            win_list = [w0, wa, w1, w2, w3, w4, w5, w6, w7, w8, w9, wb, w10, w11]

            for win_line in win_list:
                print (Fore.BLACK + color_player + win_line)
                time.sleep(0.5)

def display_map(data_map, clear):
    """Display the map of the game.

    Parameters:
    -----------
    data_map: the whole database of the game (dict)
    clear: Activate the "clear_output" of the notebook. Game looks more realistic (bool)

    Version:
    --------
    specification: Laurent Emilie v.1 (12/02/16)
    implementation: Bienvenu Joffrey v.3 (01/04/16)
    """
    # if clear:
        #clear_output()

    # Check which player have to play and define displaying constants.
    player = 'player' + str((data_map['main_turn'] % 2) + 1)
    ennemy = 'player' + str(2 - (data_map['main_turn'] % 2))
    ui_color = data_map[player + 'info'][0]

    data_cell = {'ui_color': ui_color}

    # Generate the units to be displayed.
    for i in range(1, data_map['map_size'] + 1):
        for j in range(1, data_map['map_size'] + 1):

            # Coloration black/white of the cells.
            background_cell = ''
            if (i + j) % 2 == 0:
                background_cell = Back.WHITE

            if (i, j) in data_map['player1']:
                data_cell['(' + str(i) + ',' + str(j) + ')'] = data_map['player1'][(i, j)][1] + background_cell + ' ☻' + str(data_map['player1'][(i, j)][0]) + (str(data_map['player1'][(i, j)][2]) + ' ')[:2]
            elif (i, j) in data_map['player2']:
                data_cell['(' + str(i) + ',' + str(j) + ')'] = data_map['player2'][(i, j)][1] + background_cell + ' ☻' + str(data_map['player2'][(i, j)][0]) + (str(data_map['player2'][(i, j)][2]) + ' ')[:2]
            else:
                data_cell['(' + str(i) + ',' + str(j) + ')'] = background_cell + (' ' * 5)

    # Generate the statistics to be displayed.
    player1_cell = data_map[player].keys()
    cell1_couter = 0
    player2_cell = data_map[ennemy].keys()
    cell2_couter = 0
    unit_name = {'E': 'Elf', 'D': 'Dwarf'}

    for i in range(1, 5):
        for j in range(1, 3):
            if len(player1_cell) > cell1_couter:
                data_cell['stat' + str(i) + str(j)] = (('0' + str(player1_cell[cell1_couter][0]))[-2:] + '-' + ('0' + str(player1_cell[cell1_couter][1]))[-2:] + ' ' + unit_name[data_map[player][player1_cell[cell1_couter]][0]] + ' hp: ' + str(data_map[player][player1_cell[cell1_couter]][2]) + ' ' * 20)[:20]
                cell1_couter += 1
            else:
                data_cell['stat' + str(i) + str(j)] = ' ' * 20
        for j in range(3, 5):
            if len(player2_cell) > cell2_couter:
                data_cell['stat' + str(i) + str(j)] = (('0' + str(player2_cell[cell2_couter][0]))[-2:] + '-' + ('0' + str(player2_cell[cell2_couter][1]))[-2:] + ' ' + unit_name[data_map[ennemy][player2_cell[cell2_couter]][0]] + ' hp: ' + str(data_map[ennemy][player2_cell[cell2_couter]][2]) + ' ' * 20)[:20]
                cell2_couter += 1
            else:
                data_cell['stat' + str(i) + str(j)] = ' ' * 20

    # Generate the title of the map to be displayed.
    data_cell['turn'] = str(data_map['main_turn']/2 + 1)
    data_cell['playername'] = data_map[player + 'info'][1]
    data_cell['blank'] = ((data_map['map_size'] * 5) - 19 - len(data_cell['turn']) - len(data_cell['playername'])) * ' '

    # Print the top of the UI.
    for line in data_map['data_ui']:
        print line % data_cell

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

    # Rewrite the command into a single string.
    string_commands = ''
    for command in raw_commands:
        string_commands += ('0' + str(command[0][0]))[-2:] + '_' + ('0' + str(command[0][1]))[-2:] + command[1] + ('0' + str(command[2][0]))[-2:] + '_' + ('0' + str(command[2][1]))[-2:] + '   '

    return string_commands

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
               'attack_turn': 0,
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

def save_data_map(data_map):
    """Load a saved game.

    Parameters:
    -----------
    data_map_saved: name of the file to load (str)

    Version:
    --------
    specification: Laurent Emilie v.1 (11/02/16)
    implementation: Pirlot Sylvain v.1 & Bienvenu Joffrey (21/03/16)
    """
    pickle.dump(data_map, open("save.p", "wb"))



def load_data_map():
    """Save the game.

    Parameters:
    -----------
    data_map: the whole database of the game (dict)

    Version:
    --------
    specification: Laurent Emilie v.1 (11/02/16)
    implementation: Pirlot Sylvain v.1 & Bienvenu Joffrey (21/03/16)
    """

    return pickle.load(open("save.p", "rb"))

def move_unit(data_map, start_coord, end_coord, player, enemy):
    """Move an unit from a cell to another cell. And check if the move is legal.

    Parameters:
    -----------
    data_map: the whole database (dict)
    start_coord: coordinates at the origin of the movement (tuple)
    end_coord: coordinates at the destination of the movement (tuple)
    player: the player who is moving the unit (str)
    enemy: the other player (str)

    Returns:
    --------
    data_map: the database modified by the move (dict)

    Notes:
    ------
    The database will only change the coordinate of the units concerned.
    start_coord and end_coord will be tuple of int

    Version:
    --------
    specification: Laurent Emilie & Bienvenu Joffrey v.2 (17/02/16)
    implementation: Laurent Emilie & Bienvenu Joffrey v.2 (17/03/16)
    """

    # Check if there's a unit on the starting cell, and if the destination cell is free.
    if start_coord in data_map[player] and end_coord not in data_map[player]and end_coord not in data_map[enemy]:

        # Check if the move is rightful and save it.
        if start_coord[0] - 1 <= end_coord[0] <= start_coord[0] + 1 and start_coord[1] - 1 <= end_coord[1] <= start_coord[1] + 1:
            if data_map[player][start_coord][0] == 'E' or (sum(start_coord) - 1 <= sum(end_coord) <= sum(start_coord) + 1):
                data_map[player][end_coord] = data_map[player].pop(start_coord)
    return data_map

def is_not_game_ended(data_map):
    """Check if the game is allow to continue.

    Parameter:
    ----------
    data_map: the whole database (dict)

    Returns:
    --------
    continue_game : boolean value who said if the game need to continue(bool).
    loser : the player who lose the game(str).
    winner : the player who won the game(str).

    Notes:
    ------
    The game stop when a player run out of unit or if 20 turn have been played without any attack.
    In this case, the player 1 win.

    Version:
    -------
    specification: Maroit Jonathan(v.1 21/03/16)
    implementation: Maroit Jonathan & Bienvenu Joffrey (v.1.1 22/03/16)
    """

    continue_game = True
    loser = None
    winner = None

    # If a player has not any units, the other player win.
    for i in range(2):
        if not len(data_map['player' + str(i + 1)]) and continue_game:
            loser = 'player' + str(i + 1)
            winner = 'player' + str(3 - (i + 1))
            continue_game = False

    # If there's 20 turn without any attack, player1 loose and player2 win.
    if float(data_map['attack_turn']) / 2 > 19:
        loser = 'player1'
        winner = 'player2'
        continue_game = False

    return continue_game, loser, winner

def create_data_ui(data_map, clear):
    """Generate the whole user's interface with the statistics.

    Parameters:
    -----------
    data_map: the whole database (dict)
    clear: Activate the "clear_output" of the notebook. Game looks more realistic (bool)

    Returns:
    --------
    data_ui: the user's interface to print (list)

    Versions:
    ---------
    specification: Laurent Emilie v.1 (15/03/16)
    implementation: Bienvenu Joffrey v.3.1 (24/03/16)
    """
    data_ui = [[]] * (16 + data_map['map_size'])

    # Initialisation of the displaying constants.
    grid_size = 5 * data_map['map_size']
    ui_color = '%(ui_color)s'

    margin = 5
    line_coloured = ui_color + ('█' * (117 + margin)) + Style.RESET_ALL
    if clear:
        margin = 9
        line_coloured = ui_color + ('█' * (121 + margin)) + Style.RESET_ALL


    border_black = Back.BLACK + '  ' + Style.RESET_ALL
    margin_left = ((20 - data_map['map_size']) * 5) / 2
    margin_right = ((20 - data_map['map_size']) * 5) - (((20 - data_map['map_size']) * 5) / 2)
    border_coloured_margin_left = ui_color + ('█' * (margin + margin_left)) + Style.RESET_ALL
    border_coloured_margin_right = ui_color + ('█' * (margin + margin_right)) + Style.RESET_ALL
    border_coloured_left = ui_color + ('█' * margin) + Style.RESET_ALL
    border_coloured_right = ui_color + ('█' * margin) + Style.RESET_ALL
    border_coloured_middle = ui_color + ('█' * 8) + Style.RESET_ALL

    border_white = ' ' * 2

    # Generate and save the top of the UI.
    for i in range(3):
        data_ui[i] = line_coloured

    # Generate and save the top of the grid.
    turn_message = 'Turn %(turn)s - %(playername)s, it\'s up to you ! %(blank)s'
    data_ui[3] = border_coloured_margin_left + Fore.WHITE + Back.BLACK + '  ' + turn_message + '  ' + Style.RESET_ALL + border_coloured_margin_right
    data_ui[4] = border_coloured_margin_left + border_black + ' ' * (grid_size + 8) + border_black + border_coloured_margin_right

    # Generate and save the architecture of the grid.
    for i in range(1, data_map['map_size'] + 1):
        data_ui[i + 4] = border_coloured_margin_left + border_black + Fore.BLACK + ' ' + ('0' + str(i))[-2:] + ' ' + Style.RESET_ALL
        for j in range(1, data_map['map_size'] + 1):
            data_ui[i + 4] += '%((' + str(i) + ',' + str(j) + '))5s' + Style.RESET_ALL
        data_ui[i + 4] += '    ' + border_black + border_coloured_margin_right

    # Generate and save the foot of the grid.
    data_ui[data_map['map_size'] + 5] = border_coloured_margin_left + border_black + Fore.BLACK + '   '
    for i in range(1, data_map['map_size'] + 1):
        data_ui[data_map['map_size'] + 5] += '  ' + ('0' + str(i))[-2:] + ' '
    data_ui[data_map['map_size'] + 5] += '     ' + border_black + border_coloured_margin_right

    data_ui[data_map['map_size'] + 6] = border_coloured_margin_left + Back.BLACK + (grid_size + 12) * ' ' + Style.RESET_ALL + border_coloured_margin_right

    # Generate and save the top of the statistics.
    data_ui[data_map['map_size'] + 7] = line_coloured

    data_ui[data_map['map_size'] + 8] = border_coloured_left + Fore.WHITE + Back.BLACK + '  Your units:' + (' ' * 39) + Style.RESET_ALL + border_coloured_middle
    data_ui[data_map['map_size'] + 8] += Fore.WHITE + Back.BLACK + '  Opponent\'s units:' + (' ' * 33) + Style.RESET_ALL + border_coloured_right

    # Generate and save the content of the statistics.
    for i in range(4):
        data_ui[data_map['map_size'] + 9 + i] = border_coloured_left + border_black + ' ' + border_white + Fore.BLACK + '%(stat' + str(i+1) + '1)s' + border_white + '%(stat' + str(i+1) + '2)s' + border_white + ' ' + border_black + border_coloured_middle
        data_ui[data_map['map_size'] + 9 + i] += border_black + ' ' + border_white + '%(stat' + str(i+1) + '3)s' + border_white + '%(stat' + str(i+1) + '4)s' + border_white + ' ' + border_black + border_coloured_right

    # Generate and save the foot of the statistics.
    data_ui[data_map['map_size'] + 13] = border_coloured_left + Back.BLACK + (' ' * 52) + Style.RESET_ALL + border_coloured_middle
    data_ui[data_map['map_size'] + 13] += Back.BLACK + (' ' * 52) + Style.RESET_ALL + border_coloured_right

    for i in range(2):
        data_ui[data_map['map_size'] + 14 + i] = line_coloured

    return data_ui

def create_data_map(remote, map_size=7, name_player1='player1', name_player2='player2', clear=False):
    """ Create a dictionary that the game will use as database with units at their initial places.

    Parameters:
    ----------
    map_size : the length of the board game, every unit add one unit to vertical axis and horizontal axis (int, optional).
    name_player1: name of the first player (str)
    name_player2: name of the second player (str)
    clear: if you want to activate the clear screen (bool)

    Returns:
    -------
    data_map : dictionary that contain information's of every cells of the board (dict).
    data_ui : list with data to display the ui (list of str).

    Notes:
    -----
    The game board is a square, the size must be a positive integer, minimum 7 and maximum 30 units,
    or the game will be stopped after 20 turns if nobody attack.

    Version:
    -------
    specification: Maroit Jonathan & Bienvenu Joffrey v.2 (04/03/16)
    implementation: Maroit Jonathan & Bienvenu Joffrey & Laurent Emilie v.5 (23/03/16)
    """
    # Initialisation of variables
    data_map = {'player1': {},
                'player1info': [],
                'player2': {},
                'player2info': [],
                'main_turn': 1,
                'attack_turn': 0,
                'map_size': map_size,
                'remote': remote}

    # Place units to their initial positions.
    player_data = [Fore.BLUE, Fore.RED, name_player1, name_player2]
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

                    data_map['player' + str(i + 1)][(x_pos, y_pos)] = [unit, player_data[i], life]
        data_map['player' + str(i + 1) + 'info'].extend([player_data[i], player_data[i + 2]])

    # Randomize which player will start the game.
    number = random.randint(1, 2)
    if number == 1:
        data_map['player1info'][1] = name_player1
        data_map['player2info'][1] = name_player2
    else:
        data_map['player1info'][1] = name_player2
        data_map['player2info'][1] = name_player1

    data_map['data_ui'] = create_data_ui(data_map, clear)

    return data_map

def choose_action(data_map, connection, data_ia):
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
    Each instruction must be spaced by 3 characters.

    Version:
    -------
    specification: Laurent Emilie v.1 (11/02/16)
    implementation: Laurent Emilie v.3 (21/03/16)
    """
    player = 'player' + str((data_map['main_turn'] % 2) + 1)
    enemy = 'player' + str(2 - (data_map['main_turn'] % 2))
    if data_map['remote']:
        player = 'player' + str(data_map['remote'])
        enemy = 'player' + str(3 - data_map['remote'])

    # Tells whether IA or player's turn.
    if (data_map['main_turn'] % 2) + 2 == data_map['remote'] or data_map['main_turn'] % 2 == data_map['remote'] or data_map[str(player + 'info')][1] == 'IA':
        game_instruction = ia_action(data_map, data_ia)
        notify_remote_orders(connection, game_instruction)
    else:
        if data_map['remote']:
            game_instruction = get_remote_orders(connection)
        else:
            game_instruction = raw_input('Enter your commands in format xx_xx -a-> xx_xx or xx_xx -m-> xx_xx')

    # Split commands string by string.
    list_action = game_instruction.split()

    # grouper instruction par instructions
    list_action2 = []
    for instruction in range(0, len(list_action), 3):
        list_action2.append((list_action[instruction], list_action[instruction + 1], list_action[instruction + 2]))

    # Call attack_unit or move_unit in function of instruction.
    attack_counter = 0
    for i in range(len(list_action2)):
        if '-a->' in list_action2[i]:
            data_map, attacked = attack_unit(data_map, (int(list_action2[i][0][:2]), int(list_action2[i][0][3:])),
                        (int(list_action2[i][2][:2]), int(list_action2[i][2][3:])), player, enemy)
            attack_counter += attacked
        elif '-m->' in list_action2[i]:
            data_map = move_unit(data_map, (int(list_action2[i][0][:2]), int(list_action2[i][0][3:])),
                      (int(list_action2[i][2][:2]), int(list_action2[i][2][3:])), player, enemy)

    # Save if a player have attacked.
    if attack_counter:
        data_map['attack_turn'] = 0
    else:
        data_map['attack_turn'] += 1
    data_map['main_turn'] += 1

    return data_map

def attack_unit(data_map, attacker_coord, target_coord, player, enemy):
    """Attack an adverse cell and check whether it is a legal attack.

    Parameters:
    -----------
    data_map: the whole database (dict)
    attacker_coord: coordinates of the attacker's pawn (tuple)
    target_coord: coordinates of the attacked's pawn (tuple)
    player: the player who is attacking (str)
    enemy: the other player (str)

    Returns:
    --------
    data_map: the database modified by the attack (dict)

    Notes:
    ------
    The database will only change by decrement unit's life and, eventually, decrementing the unit's number of the player.
    attacker_coord and attacked_coord will be tuple of int.

    Version:
    -------
    specification: Laurent Emilie & Bienvenu Joffrey v.2 (17/03/16)
    implementation: Bienvenu Joffrey v.1 (17/03/16)
    """
    damage = {'E': 1, 'D': 3}
    attacked = 0

    # Check if there's a unit on the attacker cell, and if the attacked cell is occupied.
    if attacker_coord in data_map[player] and target_coord in data_map[enemy]:

        # Check if the attack is rightful and save it.
        if attacker_coord[0] - 2 <= target_coord[0] <= attacker_coord[0] + 2 and attacker_coord[1] - 2 <= target_coord[1] <= attacker_coord[1] + 2:
            attacker_type = data_map[player][attacker_coord][0]
            if attacker_type == 'E' or (attacker_coord[0] - 1 <= target_coord[0] <= attacker_coord[0] + 1 and attacker_coord[1] - 1 <= target_coord[1] <= attacker_coord[1] + 1):

                # Decrement the heal point and delete the unit if their hp are equal or less than 0.
                data_map[enemy][target_coord][2] -= damage[attacker_type]
                if data_map[enemy][target_coord][2] <= 0:
                    del data_map[enemy][target_coord]
                attacked = 1

    return data_map, attacked
