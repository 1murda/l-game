import random
from colorama import Fore
import os


def cls() -> None:
    command = 'clear'

    if os.name in ('nt', 'dos'):
        command = 'cls'

    os.system(command)


def validate_option(options: list) -> int:
    option: int = input("-> ")

    while(option not in options):
        option = input("Opción invalida, intente nuevamente: ")

    return option


def turns(past_turn: str) -> str:

    if (past_turn == ''):
        turn: int = random.choice(['B', 'R'])

    else:

        if (past_turn == 'R'):
            turn = 'B'

        else:
            turn = 'R'

    return turn


def check_able_rows(board: dict, ables: list) -> list:
    posible_rows: list = []

    for i in range(1,5):

        if (board[f'a{i}'] in ables and board[f'b{i}'] in ables and board[f'c{i}'] in ables):
            posible_rows.append([f'a{i}', f'b{i}', f'c{i}'])
        
        if (board[f'b{i}'] in ables and board[f'c{i}']in ables and board[f'd{i}'] in ables):
            posible_rows.append([f'b{i}', f'c{i}', f'd{i}'])
    
    return posible_rows


def check_able_columns(board: dict, ables: list) -> list:
    posible_columns: list = []

    for w in ['a','b','c','d']:
        if (board[f'{w}1'] in ables and board[f'{w}2'] in ables and board[f'{w}3'] in ables):
            posible_columns.append([f'{w}1',f'{w}2',f'{w}3'])
            
        if (board[f'{w}2'] in ables and board[f'{w}3'] in ables and board[f'{w}4'] in ables):
            posible_columns.append([f'{w}2',f'{w}3',f'{w}4'])
    
    return posible_columns
    

def check_slots(board: dict, row: list, places: list, l_posibles: list, able_slots: list) -> None:
    # recibe una lista con los slots que se desea verificar si estan disponibles
    # para completar la L, si lo encuentra agrega la posible L a posibles_places
    for s in places:
        if (board[s] in able_slots):
            l_posibles.append(row + [s])
    


def check_rows_l(board: dict, able_rows: list, l_posibles: list, able_slots) -> None:
    for row in able_rows:
                #checkeo si la secuencia esta en la primera row o en la ultima
        if (row[0] in ['a1','b1', 'a4', 'b4']):
            if (row[0] == 'a1'):
                check_slots(board, row, ['a2','b2','c2'], l_posibles, able_slots)
                                
            elif (row[0] == 'b1'): 
                check_slots(board, row, ['b2','c2','d2'], l_posibles, able_slots)
                    
            elif (row[0] == 'a4'):
                check_slots(board, row, ['a3','b3','c3'], l_posibles, able_slots)
            
            else:
                check_slots(board, row, ['b3', 'c3', 'd3'], l_posibles, able_slots)
                        
        else:
            n_row: int = int(row[0][1]) #numero de row
            down_next_row: list = []
            up_next_row: list = []
            
            if (row[0][0] == 'a'): 
                # checkea los slots disponibles para completar la L en la row de arriba
                # y en la row de abajo de la secuencia de 3
                down_next_row = [f'a{n_row + 1}',f'b{n_row + 1}',f'c{n_row + 1}']
                up_next_row = [f'a{n_row - 1}',f'b{n_row - 1}',f'c{n_row - 1}']

                check_slots(board, row, down_next_row, l_posibles, able_slots)
                check_slots(board, row, up_next_row, l_posibles, able_slots)
            
            else:
                down_next_row = [f'b{n_row + 1}',f'c{n_row + 1}',f'd{n_row + 1}']
                up_next_row = [f'b{n_row + 1}',f'c{n_row + 1}',f'd{n_row + 1}']

                check_slots(board, row, down_next_row, l_posibles, able_slots)
                check_slots(board, row, up_next_row, l_posibles, able_slots)



def check_columns_l(board: dict, able_columns: list, l_posibles: list, able_slots) -> None:
    right_next_col: list = []
    left_next_col: list = []

    for col in able_columns:
        n_col: int = int(col[0][1])
        
        if (col[0][0] == 'a'):
            right_next_col = [f'b{n_col}',f'b{n_col + 1}',f'b{n_col + 2}']
            check_slots(board, col, right_next_col, l_posibles, able_slots)
        
        elif (col[0][0] == 'b'):
            left_next_col = [f'a{n_col}',f'a{n_col + 1}',f'a{n_col + 2}']
            right_next_col = [f'c{n_col}',f'c{n_col + 1}',f'c{n_col + 2}']
            check_slots(board, col, left_next_col, l_posibles, able_slots)
            check_slots(board, col, right_next_col, l_posibles, able_slots)

        elif (col[0][0] == 'c'):
            right_next_col = [f'd{n_col}',f'd{n_col + 1}',f'd{n_col + 2}']
            left_next_col = [f'b{n_col}',f'b{n_col + 1}',f'b{n_col + 2}']
            check_slots(board, col, right_next_col, l_posibles, able_slots)
            check_slots(board, col, left_next_col, l_posibles, able_slots)

        elif (col[0][0] == 'd'):
            left_next_col = [f'c{n_col}',f'c{n_col + 1}',f'c{n_col + 2}']
            check_slots(board, col, left_next_col, l_posibles, able_slots)
 


def is_l_in_posibles_l(pos: list, l_list: list) -> str:
    # busco si la L pasada por parametros se encuentra en las L posibles
    # devuelvo el indice en donde se encuentra la L en la lista
    # si no la encuentra devuelve 00
    index: str = ''

    for l_index, l in enumerate(l_list):

        if (len(pos) == 4):

            if (pos[0] in l and pos[1] in l and pos[2] in l and pos[3] in l):
                return str(l_index)
    
    return index




def find_posible_l(board: dict, turn: str) -> list:
    slots_ables: list = []
    l_posibles: list = []

    if (turn == 'R'):
        able_slots = ['R',' ']

    else:
        able_slots = ['B',' ']

    row_able_secuences: list = check_able_rows(board, able_slots)
    column_able_secuences: list = check_able_columns(board, able_slots)

    check_rows_l(board, row_able_secuences, l_posibles, able_slots)
    check_columns_l(board, column_able_secuences, l_posibles, able_slots)
    
# elimino las secuencias que no forman una L
#   ej:  o
#        o o
#        o
                                                       #
    for l in l_posibles:                               #
        if (l[1][1] == l[3][1] or l[1][0] == l[3][0]): #
            l_posibles.remove(l)                       #
#######################################################

# elimino de las posibles L a las coordenadas de la L actual del jugador
    actual_l_pos: list = []

    for slot, value in board.items():

        if (value == turn):
            actual_l_pos.append(slot)

    l_index: str = is_l_in_posibles_l(actual_l_pos, l_posibles)

    if (l_index != ''):
        l_posibles.remove(l_posibles[int(l_index)])

    return l_posibles




def change_l_pos(board: dict, pos: list, turn: str) -> None:
    # primero limpio la posicion anterior de la L en el board
    for slot, value in board.items():
        if value == turn:
            board[slot] = ' '
        
    for slot in pos:
        board[slot] = turn
    


def move_neutral(board: dict, turn: str) -> None:
    print("Desea mover una ficha neutral? (s/n)")
    move: str = validate_option(['s','n'])

    if (move == 's'):

        print("Ingrese 1 para mover la ficha neutral '1' o 2 para la ficha '2'")
        option: str = validate_option(['1','2'])

        for slot, value in board.items():
            if (value == option):
                board[slot] = ' '
        
        print("Ingrese la posicion a donde desee mover la ficha neutral")
        move_to: str = validate_option(board.keys())
        
        while (board[move_to] != ' '):
            print("Esa posición no esta disponible, intente con otra")
            move_to = validate_option(board.keys())

        for slot in board:
            if (slot == move_to):
                board[slot] = option



def play(board: dict) -> str:
    turn: str = ''
    winner: str = ''
    
    playing: bool = True
    movements_counter: int = 18
    
    while (playing):
        movements_counter += 1
        turn = turns(turn)
        posible_ls: list = find_posible_l(board, turn)

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
            
        else:
    
            show_board(board)
            print(f"Turno del jugador {turn}")
            print("Ingrese las coordenadas en donde desea ubicar su L separandolas por una coma: ")
            print("Ejemplo: a1,a2,a3,b1")
            
            movement: list = input("->").split(",")
            
            

            index_l: str = is_l_in_posibles_l(movement, posible_ls)

            while (index_l == ''):
                show_board(board)
                print(f"Turno del jugador {turn}")
                print("Ese movimiento no es posible, intente con otro.")
                print("Ejemplo: a1,a2,a3,b1")
                movement: list = input("->").split(",")
                index_l: str = is_l_in_posibles_l(movement, posible_ls)

            change_l_pos(board, movement, turn)
            show_board(board)
            
            #modo muerte súbita
            if (movements_counter >= 20):
                show_board(board)
                print("El juego entro en fase muerte subita!")
                print("Cada jugador ahora luego de mover su L puede mover 2 fichas neutrales si lo desea")
                move_neutral(board, turn)
                move_neutral(board, turn)
            
            else:
                show_board(board)
                move_neutral(board, turn)
                

    return winner
        
        


def show_board(board: list) -> None:
    cls()
    red: str = Fore.RED
    blue: str = Fore.BLUE
    black: str = Fore.BLACK
    
    board_aux: dict = {}

    for k, v in board.items():
        board_aux[k] = v

    for k, v in board_aux.items():
        if (v == 'R'):
            board_aux[k] = red + v + Fore.RESET

        elif (v == 'B'):
            board_aux[k] = blue + v + Fore.RESET

        elif (v in ['1','2']):
            board_aux[k] = black + v + Fore.RESET

        

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
    info_ordered: list = sorted(players_info.items(), key=lambda x: x[1], reverse=True)


    
    print(f"""
 ____________________________
|      ULTIMOS 4 SCORES      |      
|                            |
| Jugador  Partidas ganadas  |
|                            |
| {info_ordered[0][0]}   -   {info_ordered[0][1]}               |
| {info_ordered[1][0]}   -   {info_ordered[1][1]}               |
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
[2] Mostrar los ultimos 3 scores
[3] Salir
""")    
        turn: int = 0
        option: str = validate_option(['1', '2', '3'])
       
        if (option == '1'):
            show_board(board)
            game_info: list = play(board)
            scores_history.append(game_info)

        elif (option == '2'):
            show_past_4_scores(scores_history)

        elif (option == '3'):
            flag = False
    

main()
