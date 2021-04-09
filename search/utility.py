"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching
Module: utility
Created by ThePinkCoder (Yongfeng Qin & Yun-Chi Hsiao) on Mar.23rd 2021

This module contains algorithms which would assisst the user to find the 
solution in Single-player RoPaSci360 game. It is referenced to the provided 
module util.py.
"""
import time
from search.util import print_board, print_slide, print_swing

# Get coordinates from one piece
def get_coord(piece):
    return (piece[1], piece[2])

# Check if two pieces at same spot
def same_coord(coord_1, coord_2):
    
    if coord_1[0] == coord_2[0] and coord_1[1] == coord_2[1]:
        return True
    else:
        return False
    
# Check if two pieces beside each other
def beside_coord(coord_1, coord_2):
        
    row = coord_1[0]
    col = coord_1[1]

    possible_coord = [(row + 1, col - 1), (row + 1, col), (row, col - 1), (row, col + 1), (row - 1, col), (row - 1, col + 1)]
    
    if coord_2 in possible_coord:
        return True
    else:
        return False

# Transfer the following format
# {'upper': [['r', 0, -3], ['p', 0, 1]], 'lower': [['p', -2, 1], 'block': []}
# To
# {(0, -3): "(Ur)", (0, 1): "(Up)", (-2,1): "(Lp)"}
def reformat(data):
    
    dict = {}
    
    # Upper pieces 
    for i in data['upper']:
        
        tuple_data = (i[1], i[2])
        value = '(' + 'U' + i[0] + ')'

        if tuple_data in dict.keys():
            dict[tuple_data] = dict.get(tuple_data) + value
        else:
            dict[tuple_data] = value

    # Lower pieces   
    for j in data['lower']:

        tuple_data = (j[1], j[2])
        value = '(' + 'L' + j[0] + ')'

        if tuple_data in dict.keys():
            dict[tuple_data] = dict.get(tuple_data) + value
        else:
            dict[tuple_data] = value

    # Block pieces 
    for k in data['block']:

        tuple_data = (k[1], k[2])
        value = '(' + 'B' + ')'

        if tuple_data in dict.keys():
            dict[tuple_data] = dict.get(tuple_data) + value
        else:
            dict[tuple_data] = value

    return dict

# Print out the process from the beginning to the current state by text
def print_transcript_text(current_state):

    states = []
    
    while current_state is not None:
        states.append(current_state)
        current_state = current_state.parent_state
    
    # Reverse to correct order
    states = list(reversed(states))

    # Do not need initial state 
    states.pop(0)

    while states:
        
        current_state = states.pop(0)
        parent_state = current_state.parent_state

        for (current, parent) in zip(current_state.board[current_state.game.ally], parent_state.board[parent_state.game.ally]):
            # If ally is alive
            if parent[0] != 'x':
                if beside_coord(get_coord(current), get_coord(parent)) is True:
                    print_slide(current_state.depth, parent[1], parent[2], current[1], current[2])
                else:
                    print_swing(current_state.depth, parent[1], parent[2], current[1], current[2])

# Print out the process from the beginning to the current state by board
def print_transcript_board(current_state):
        
    boards = []
        
    while current_state is not None:
        boards.append(current_state.board)
        current_state = current_state.parent_state
        
    for i in reversed(boards):
        print_board(reformat(i))
        time.sleep(1)


def get_ordered_list(index_upper, x, y):
    index_upper.sort(key = lambda p: (p[1] - x)**2 + (p[2] - y)**2)
    return index_upper
    