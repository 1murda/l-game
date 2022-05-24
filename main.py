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
        option = input("Please, enter a valid option: ")

    return option


def turns(past_turn: str) -> str:

    if (past_turn == ''):
        turn: int = random.choice(['blue','red'])

    else:

        if (past_turn == 'red'):
            turn = 'blue'

        else:
            turn = 'red'

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
                check_slots(board, row, ['a2','b2','c2'],l_posibles, able_slots)
                                
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
                # y en la de abajo de la secuencia
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


def clean_l(l_posibles: list) -> None:
    # eliminan las secuencias que no forman una L
    #   ej:  o
    #        o o
    #        o
    
    for l in l_posibles:
        if (l[1][1] == l[3][1] or l[1][0] == l[3][0]):
            l_posibles.remove(l)
            


def find_posible_l(board: dict, turn: str) -> list:
    slots_ables: list = []
    l_posibles: list = []

    if (turn == 'blue'):
        able_slots = ['blue','void']

    else:
        able_slots = ['red','void']

    row_able_secuences: list = check_able_rows(board, able_slots)
    column_able_secuences: list = check_able_columns(board, able_slots)

    check_rows_l(board, row_able_secuences, l_posibles, able_slots)
    check_columns_l(board, column_able_secuences, l_posibles, able_slots)
    clean_l(l_posibles)


    return l_posibles


def play(board: dict) -> None:
    turn: str = ''
    turn = turns(turn)
    playing: bool = True
    
    while (playing):
        show_board(board)
        print("Ingrese las posiciones donde desea ubicar su L separando los casilleros por una coma: ")
        print("Ejemplo: a1,a2,a3,b1")
        movement: list = input("->").split(",")
        print(movement)
        input()




def show_board(board: list) -> None:
    cls()
    print(f"""
      A       B      C      D
     ___________________________
    |      |      |      |      |
 1  |  {board['a1']}   |   {board['b1']}  |  {board['c1']}   |  {board['d1']}   |
    |______|______|______|______|
    |      |      |      |      |
 2  |  {board['a2']}   |   {board['b2']}  |  {board['c2']}   |  {board['d2']}   |
    |______|______|______|______|
    |      |      |      |      |
 3  |  {board['a2']}   |   {board['b3']}  |  {board['c3']}   |  {board['d3']}   |
    |______|______|______|______|
    |      |      |      |      |
 4  |  {board['a2']}   |   {board['b4']}  |   {board['c4']}  |  {board['d4']}   |
    |______|______|______|______| 
     
    """)

    

def main() -> None:
    v = ' ' # able slot
    r = 'R' # red player
    b = 'B' # blue pĺayer
    n = 'N' # neutral

    board = {   
                'a1': n, 'b1': r,'c1': r, 'd1': v,
                'a2': v, 'b2': b,'c2': r, 'd2': v,
                'a3': v, 'b3': b,'c3': r, 'd3': v,
                'a4': v, 'b4': b,'c4': b, 'd4': n 
            }

    scores_history: list = []

    flag: bool = True

    while(flag):
        cls()
        turn: int = 0
        print("""
        1) Play a new game
        2) Show past 3 game scores
        3) Quit""")
        option: str = validate_option(['1', '2', '3'])
       
        if (option == '1'):
            # l_posible: list = find_posible_l(board, turn)
            show_board(board)
            game_info: list = play(board)
            scores_history.append(game_info)

        elif (option == '1'):
            pass

        else:
            flag = False
    



main()
