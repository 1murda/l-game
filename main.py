import random
from colorama import Fore
import os

# requiere instalar colorarma: 
#         pip3 install colorama


def cls() -> None:
    """Limpia la terminal segun el sistema operativo"""

    command: str = 'clear'

    if os.name in ('nt', 'dos'):
        command = 'cls'

    os.system(command)


def validate_option(options: list) -> str:
    """Valida si la opción esta en la lista de opciones

    Args:
        options (list): Lista con las opciones disponibles

    Returns:
        str: Opción elegida
    """

    option: str = input("-> ")

    while (option not in options):
        option = input("Opción invalida, intente nuevamente: ")

    return option


def turns(past_turn: str) -> str:
    """ Recibe el turno pasado y devuelve el siguiente turno
        si el turno anterior es un str vacio, elige uno al azar

    Args:
        past_turn (str): Turno anterior

    Returns:
        str: Turno siguiente
    """

    if (past_turn == ''):
        next_turn: str = random.choice(['B', 'R'])

    else:

        if (past_turn == 'R'):
            next_turn = 'B'

        else:
            next_turn = 'R'

    return next_turn


def check_able_rows(board: dict, ables: list) -> list:
    """ Busca las secuencias de 3 slots seguidos disponibles en las 4 rows

    Args:
        board (dict): Tablero
        ables (list): Lista con los slots disponibles segun el turno

    Returns:
        list: Secuencias encontradas
    """

    posible_rows: list = []

    for i in range(1,5):
        row: list = [board[f'a{i}'], board[f'b{i}'], board[f'c{i}'], board[f'd{i}']]

        if (row[0] in ables and row[1] in ables and row[2] in ables):
            posible_rows.append([f'a{i}', f'b{i}', f'c{i}'])
        
        if (row[1] in ables and row[2] in ables and row[3] in ables):
            posible_rows.append([f'b{i}', f'c{i}', f'd{i}'])
    
    return posible_rows


def check_able_columns(board: dict, ables: list) -> list:
    """ Busca las secuencias de 3 slots seguidos disponibles en forma vertical
    Args:
        board (dict): Tablero
        ables (list): Lista con los slots disponibles segun el turno

    Returns:
        list: Secuencias encontradas
    """
    posible_columns: list = []

    for w in ['a','b','c','d']:
        column: list = [board[f'{w}1'], board[f'{w}2'], board[f'{w}3'], board[f'{w}4']]

        if (column[0] in ables and column[1] in ables and column[2] in ables):
            posible_columns.append([f'{w}1', f'{w}2', f'{w}3'])
            
        if (column[1] in ables and column[2] in ables and column[3] in ables):
            posible_columns.append([f'{w}2', f'{w}3', f'{w}4'])
    
    return posible_columns
    

def check_slots(board: dict, row: list, places: list, posible_ls: list, able_slots: list) -> None:
    """ Recibe una lista con los slots que se desea verificar si estan disponibles
        para completar la L, si lo encuentra agrega la posible L a posibles_places

    Args:
        board (dict): tablero
        row (list): fila que se desea verificar
        places (list): fila siguiente a la row en la que se busca el slot disponible
        posible_ls (list): lista con las L posibles
        able_slots (list): slots disponibles segun el turno
    """
    for s in places:

        if (board[s] in able_slots):
            posible_ls.append(row + [s])
    

def check_rows_l(board: dict, able_rows: list, posible_ls: list, able_slots) -> None:
    """ Busca las L's completas en forma horizontal que se pueden posicionar y las almacena en 'posible_ls'

    Args:
        board (dict): Tablero
        able_rows (list): Secuencias completas disponibles en forma horizontal
        posible_ls (list): Lista con las L completas posibles
        able_slots (list): Lista con los slots disponibles segun el turno 
    """

    for row in able_rows:
                #checkeo si la secuencia esta en la primera row o en la ultima
        if (row[0] in ['a1','b1', 'a4', 'b4']):

            if (row[0] == 'a1'):
                check_slots(board, row, ['a2','b2','c2'], posible_ls, able_slots)
                                
            elif (row[0] == 'b1'): 
                check_slots(board, row, ['b2','c2','d2'], posible_ls, able_slots)
                    
            elif (row[0] == 'a4'):
                check_slots(board, row, ['a3','b3','c3'], posible_ls, able_slots)
            
            else:
                check_slots(board, row, ['b3', 'c3', 'd3'], posible_ls, able_slots)
                        
        else:
            print(row)
            n_row: int = int(row[0][1]) #numero de row
            down_next_row: list = []
            up_next_row: list = []
            
            if (row[0][0] == 'a'): 
                # checkea los slots disponibles para completar la L en la row de arriba
                # y en la row de abajo de la secuencia de 3
                down_next_row = [f'a{n_row + 1}',f'b{n_row + 1}',f'c{n_row + 1}']
                up_next_row = [f'a{n_row - 1}',f'b{n_row - 1}',f'c{n_row - 1}']

                check_slots(board, row, down_next_row, posible_ls, able_slots)
                check_slots(board, row, up_next_row, posible_ls, able_slots)
            
            else:
                down_next_row = [f'b{n_row + 1}',f'c{n_row + 1}',f'd{n_row + 1}']
                up_next_row = [f'b{n_row + 1}',f'c{n_row + 1}',f'd{n_row + 1}']

                check_slots(board, row, down_next_row, posible_ls, able_slots)
                check_slots(board, row, up_next_row, posible_ls, able_slots)


def check_columns_l(board: dict, able_columns: list, posible_ls: list, able_slots: list) -> None:
    """ Busca las L's completas en forma vertical que se pueden posicionar y las almacena en 'posible_ls'

    Args:
        board (dict): Tablero
        able_columns (list): Secuencias de 3 slots seguidos en forma vertical
        posible_ls (list): Lista con las L completas posibles
        able_slots (list): Lista de los slots disponibles segun el turno
    """
    right_next_col: list = []
    left_next_col: list = []

    for col in able_columns:
        n_col: int = int(col[0][1])
        
        if (col[0][0] == 'a'):
            right_next_col = [f'b{n_col}',f'b{n_col + 1}',f'b{n_col + 2}']
            check_slots(board, col, right_next_col, posible_ls, able_slots)
        
        elif (col[0][0] == 'b'):
            left_next_col = [f'a{n_col}',f'a{n_col + 1}',f'a{n_col + 2}']
            right_next_col = [f'c{n_col}',f'c{n_col + 1}',f'c{n_col + 2}']
            check_slots(board, col, left_next_col, posible_ls, able_slots)
            check_slots(board, col, right_next_col, posible_ls, able_slots)

        elif (col[0][0] == 'c'):
            right_next_col = [f'd{n_col}',f'd{n_col + 1}',f'd{n_col + 2}']
            left_next_col = [f'b{n_col}',f'b{n_col + 1}',f'b{n_col + 2}']
            check_slots(board, col, right_next_col, posible_ls, able_slots)
            check_slots(board, col, left_next_col, posible_ls, able_slots)

        elif (col[0][0] == 'd'):
            left_next_col = [f'c{n_col}',f'c{n_col + 1}',f'c{n_col + 2}']
            check_slots(board, col, left_next_col, posible_ls, able_slots)
 

def is_l_in_posibles_l(pos: list, posible_ls: list) -> str:
    """ Verifica si una posicion de L esta en posible_ls
        si no la encuentra devuelve un str vacio

    Args:
        pos (list): Coordenadas que se quieren validar
        posible_ls (list): Lista con todas las combinaciones posibles

    Returns:
        str: El indice en donde se encuentra esa posicion en posible_ls
    """
    index: str = ''
    have_rep: bool = False

    #checkeo que no hayan posiciones repetidas en las coordenadas
    
    for p in pos:
        if (pos.count(p) > 1):
            have_rep = True

    ###############################################################

    if (not have_rep):
        for l_index, l in enumerate(posible_ls):

            if (len(pos) == 4):

                if (pos[0] in l and pos[1] in l and pos[2] in l and pos[3] in l):
                    
                    index =  str(l_index)
    
    return index


def find_posible_ls(board: dict, turn: str) -> list:
    """ Busca las L posibles en el tablero

    Args:
        board (dict): Tablero
        turn (str): Turno del jugador

    Returns:
        list: Movimientos de L posibles
    """

    slots_ables: list = []
    posible_ls: list = []

    if (turn == 'R'):
        able_slots = ['R',' ']

    else:
        able_slots = ['B',' ']

    row_able_secuences: list = check_able_rows(board, able_slots)
    column_able_secuences: list = check_able_columns(board, able_slots)

    check_rows_l(board, row_able_secuences, posible_ls, able_slots)
    check_columns_l(board, column_able_secuences, posible_ls, able_slots)
    
# elimino las secuencias que no forman una L
#   ej:  o
#        o o
#        o
                                                       #
    for l in posible_ls:                               #
        if (l[1][1] == l[3][1] or l[1][0] == l[3][0]): #
            posible_ls.remove(l)                       #
#######################################################

# elimino de las posibles L a las coordenadas de la L actual del jugador
    actual_l_pos: list = []

    for slot, value in board.items():

        if (value == turn):
            actual_l_pos.append(slot)

    l_index: str = is_l_in_posibles_l(actual_l_pos, posible_ls)

    if (l_index != ''):
        posible_ls.remove(posible_ls[int(l_index)])

    return posible_ls


def change_l_pos(board: dict, pos: list, turn: str) -> None:
    """ Cambia la posicion de la L a las coordenadas a donde se la desea mover

    Args:
        board (dict): Tablero
        pos (list): Coordenadas a donde se la quiere mover
        turn (str): Turno del jugador
    """
    # primero limpio la posicion anterior de la L en el board
    for slot, value in board.items():
        if value == turn:
            board[slot] = ' '
        
    for slot in pos:
        board[slot] = turn
    

def move_neutral(board: dict, turn: str, movements_counter: int) -> None:
    """ Recibo el board actualizado, el turno y los movimientos realizados
        si los movimientos superan 20 el juego entra en muerte subita

    Args:
        board (dict): Tablero
        turn (str): Turno del jugador
        movements_counter (int): Contador de movimientos
    """
    able_movements: int = 0
    move: str = ''

    if (movements_counter < 20):
        show_board(board)
        print('Desea mover una ficha neutral? (s/n)')
        move = validate_option(['s', 'n'])
        able_movements = 1

    else:
        show_board(board)
        print('El juego esta en modo muerte subita!')
        print('Puede mover 2 fichas neutrales')
        print('Desea mover una ficha neutral? (s/n)')
        
        move = validate_option(['s', 'n'])
        able_movements = 2
    
    if (move == 's'):

        while (able_movements > 0):

            able_movements -= 1
            show_board(board)

            print("Ingrese 1 para mover la ficha neutral '1' o 2 para la ficha '2'")
            option: str = validate_option(['1','2'])

            # limpio la posicion actual de la ficha neutral que se quiere mover
            for slot, value in board.items():

                if (value == option):
                    board[slot] = ' '

            ###################################################################

            show_board(board)
            print("Ingrese la posicion a donde desee mover la ficha neutral")
            move_to: str = validate_option(board.keys())
            
            while (board[move_to] != ' '):
                print("Esa posición no esta disponible, intente con otra")
                move_to = validate_option(board.keys())

            # muevo la ficha neutral a la posicion ingresada
            board[move_to] = option

            if (able_movements == 1):
                show_board(board)
                print('Desea mover otra ficha neutral? (s/n)')
                move = validate_option(['s', 'n'])
                
                if (move == 'n'):
                    able_movements = 0



def play(board: dict) -> str:
    """ Recibo el board con las posiciones por defecto e inicio el juego

    Args:
        board (dict): Tablero

    Returns:
        str: Ganador de la partida
    """

    turn: str = ''
    winner: str = ''
    
    playing: bool = True
    movements_counter: int = 0
    
    while (playing):
        show_board(board)
        movements_counter += 1
        turn = turns(turn)
        posible_ls: list = find_posible_ls(board, turn)

        # si no hay movimientos de L posibles termina el juego
        if (len(posible_ls) == 0):
            
            if (turn == 'R'):
                show_board(board)
                print("No quedan movimientos disponibles, el jugador azul gana.")
                input("Pulse ENTER para volver al menu ")
                winner = 'B'
            
            else:
                show_board(board)
                print("No quedan movimientos disponibles, el jugador rojo gana.")
                input("Pulse ENTER para volver al menu ")
                winner = 'R'
            
            playing = False
        ####################################################################
            
        else:
    
            show_board(board)
            print(f"Turno del jugador {turn}")
            print("Ingrese las coordenadas en donde desea ubicar su L separandolas por una coma: ")
            print("Ejemplo: a1,a2,a3,b1")
            
            movement: list = input("->").split(",")

            # valido el movimiento ingresado
            index_l: str = is_l_in_posibles_l(movement, posible_ls)

            while (index_l == ''):
                show_board(board)
                print(f"Turno del jugador {turn}")
                print("Ese movimiento no es posible, intente con otro.")
                print("Ejemplo: a1,a2,a3,b1")
                movement: list = input("->").split(",")
                index_l: str = is_l_in_posibles_l(movement, posible_ls)

            # actualizo el tablero con la L ingresada
            change_l_pos(board, movement, turn)
            move_neutral(board, turn, movements_counter)
                
    return winner
          

def show_board(board: list) -> None:
    cls()

    ###### colorama  ############
    red: str = Fore.RED
    blue: str = Fore.BLUE
    black: str = Fore.BLACK
    reset: str = Fore.RESET
    ############################

    # creo un tablero auxiliar para no modificar el tablero original original
    board_aux: dict = {}

    for k, v in board.items():
        board_aux[k] = v

    # reemplazo con colores los valores del tablero original auxiliar
    for k, v in board_aux.items():
        if (v == 'R'):
            board_aux[k] = red + v + reset

        elif (v == 'B'):
            board_aux[k] = blue + v + reset

        elif (v in ['1','2']):
            board_aux[k] = black + v + reset

    
    print(f"""
      A       B      C      D
     ___________________________
    |      |      |      |      |
 1  |  {board_aux['a1']}   |   {board_aux['b1']}  |  {board_aux['c1']}   |  {board_aux['d1']}   |
    |______|______|______|______|
    |      |      |      |      |
 2  |  {board_aux['a2']}   |   {board_aux['b2']}  |  {board_aux['c2']}   |  {board_aux['d2']}   |
    |______|______|______|______|
    |      |      |      |      |
 3  |  {board_aux['a3']}   |   {board_aux['b3']}  |  {board_aux['c3']}   |  {board_aux['d3']}   |
    |______|______|______|______|
    |      |      |      |      |
 4  |  {board_aux['a4']}   |   {board_aux['b4']}  |  {board_aux['c4']}   |  {board_aux['d4']}   |
    |______|______|______|______| 
     
    """)


def show_past_4_scores(scores_history: list) -> None:
    """ Recibe una lista con todos los scores de las partidas qu se hayan jugado
    y las procesa para solo mostrar los ultimos 4 scores """

    cls()
    players_info: dict = {'Azul': 0, 'Rojo': 0}

    # doy vuelta la lista ya que los ultimos scores almacenan en 'scores_history' -
    # en las ultimas posiciones de la lista
    scores_history.reverse()
    last_4_scores: list = []

    if (len(scores_history) >= 4):

        for i in range(0,4):
            last_4_scores.append(scores_history[i])
    
    else:

        for score in scores_history:
            last_4_scores.append(score)

    for score in last_4_scores:

        if (score == 'R'):
            players_info['Rojo'] += 1
        
        else:
            players_info['Azul'] += 1

    #ordeno los scores por el jugador con mas victorias
    ordered_info: list = sorted(players_info.items(), key=lambda x: x[1], reverse=True)

    print(f"""
 ____________________________
|      ULTIMOS 4 SCORES      |      
|                            |
| Jugador  Partidas ganadas  |
|                            |
| {ordered_info[0][0]}   -   {ordered_info[0][1]}               |
| {ordered_info[1][0]}   -   {ordered_info[1][1]}               |
|                            |
 ----------------------------
    """)

    input("Pulse ENTER para volver al menu ")


def main() -> None:
    v : str= ' ' # Slot disponible
    r: str = 'R' # Slot rojo
    b: str = 'B' # Slot azul
    n_1: str = '1' # Ficha neutral 1
    n_2: str = '2' # Ficha neutral 2

    scores_history: list = []

    flag: bool = True

    while(flag):
        board = {   
                'a1': n_1, 'b1': r,'c1': r, 'd1': v,
                'a2': v, 'b2': b,'c2': r, 'd2': v,
                'a3': v, 'b3': b,'c3': r, 'd3': v,
                'a4': v, 'b4': b,'c4': b, 'd4': n_2 
                }

        cls()

        print("""
╔╗        ╔═══╗╔═══╗╔═╗╔═╗╔═══╗
║║        ║╔═╗║║╔═╗║║║╚╝║║║╔══╝
║║        ║║ ╚╝║║ ║║║╔╗╔╗║║╚══╗
║║ ╔╗╔═══╗║║╔═╗║╚═╝║║║║║║║║╔══╝
║╚═╝║╚═══╝║╚╩═║║╔═╗║║║║║║║║╚══╗
╚═══╝     ╚═══╝╚╝ ╚╝╚╝╚╝╚╝╚═══╝              
    """)

        
        print("""
[1] Empezar una nueva partida
[2] Mostrar los ultimos 4 resultados
[3] Salir
""")    
        option: str = validate_option(['1', '2', '3'])
       
        if (option == '1'):
            winner: str = play(board)
            scores_history.append(winner)

        elif (option == '2'):
            show_past_4_scores(scores_history)

        elif (option == '3'):
            flag = False

main()
