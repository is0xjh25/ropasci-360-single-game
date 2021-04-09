"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching
Module: algorithm
Created by ThePinkCoder (Yongfeng Qin & Yun-Chi Hsiao) on Mar.23rd 2021

This module contains algorithms which would assisst the user to find the 
solution in Single-player RoPaSci360 game. 
"""
from queue import PriorityQueue
import statistics
import math
import heapq

# Breadth_first_search
def bfs(game, init_state):

    # Initialization
    expend_node = 0
    explore_list = []
    explore_list.append(init_state)
    explored_board = []
    explored_board.append(init_state.board)

    # Explore_list is a queue
    while explore_list:
        expend_node = expend_node + 1
        state = explore_list.pop(0)
        explored_board.append(state.board)

        for child_state in state.expand_state():
           
            game.update_board(child_state.board)  

            # Check the state is repeated or not
            if child_state.board not in explored_board:                
                
                # Game over!
                if game.victory(child_state.board):
                    return child_state, expend_node

                # Otherwise put the child state into queue
                explore_list.append(child_state)
                explored_board.append(child_state.board)

    return None, expend_node

# A start search - the one used in this project
def a_star(game, init_state):
    expend_node = 0
    # Initialization
    explore_queue = PriorityQueue()
    explore_queue.put((init_state.fn_cost, init_state))
    explored_board = []
    explored_board.append(init_state.board)

    # Explore_list is a queue
    while not explore_queue.empty():
        
        expend_node = expend_node + 1
        state = explore_queue.get(0)[1]
        explored_board.append(state.board)

        for child_state in state.expand_state():
           
            game.update_board(child_state.board)  

            # Check the state is repeated or not
            if child_state.board not in explored_board:                
                
                # Game over!
                if game.victory(child_state.board):
                    return child_state, expend_node


                # Otherwise put the child state into queue
                if not game.tie_or_defeated(child_state.board):
                    explore_queue.put((child_state.fn_cost, child_state))
                    explored_board.append(child_state.board)


    return None, expend_node 

# Distance function, 
def dist(piece_1, piece_2):
    return math.sqrt(math.pow((piece_1[1] - piece_2[1]), 2) + math.pow((piece_1[2] - piece_2[2]) ,2)) 

# Heuristic function
def hn(game, board):
    
    dist_list = []
    hn_cost = 0

    # Calculate the approximate cost for every upper token to defeat all
    # those lower token it could
    for i in board[game.ally]:
        temp_list = []        
        for j in board[game.enemy]:
            if game.defeated(i, j) == 'win':
                temp_list.append(dist(i, j))
        total_distance = []
        if temp_list:
            for j in board[game.enemy]:
                if game.defeated(i,j) is 'win' and dist(i,j) == min(temp_list):
                    for z in board[game.enemy]:
                        if game.defeated(i,z) is 'win' and z != j:
                            total_distance.append(dist(z, j))
        if temp_list:
            dist_list.append(min(temp_list)+sum(total_distance))
        else:
            pass
    
    if dist_list:    
        hn_cost = sum(dist_list)

    # When there is too many blocks, assume it cost more for upper to 
    # eliminate the lower
    if len(board[game.block]) >= 5:
        hn_cost *= 2

    
    return hn_cost 

