"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching
Created by ThePinkCoder (Yongfeng Qin & Yun-Chi Hsiao) on Mar.23rd 2021
Module: state

This module contains a class named called State which contains board attribute.
Most states would have a parent state and generate child states based on move
function from a game object. The state also records the spended path costs and 
how many turn has runned (depth).
"""

from itertools import product
from search.algorithm import hn
from search.utility import get_ordered_list
from search.algorithm import dist

class State:

    def __init__(self, game, board, parent_state=None, gn_cost=0, depth=0):
        self.game = game
        self.board = board
        self.parent_state = parent_state
        self.gn_cost = gn_cost
        self.fn_cost = gn_cost + hn(self.game, board)
        self.depth = depth

        if parent_state is not None:
            self.depth = parent_state.depth + 1
        else:
            self.depth = 0

    # Generate all possible valid boards from one board
    def expand_board(self):
        
        expand_list = []
        result_list = []
        
        # Generate all possible moves from all allies 
        for i in self.board[self.game.ally]:
            attack = 0;
            for j in self.board[self.game.enemy]:
                if self.game.defeated(i,j) is 'win':
                    attack = 1
                    break

            if i[0] == 'x' or attack==0:
                expand_list.append([self.game.move(i, self.board)[0]])
            else:
                close_defeated_index = self.get_closest_defeated_index(i, self.board);
                if close_defeated_index is not None:
                    possible_move = self.game.move(i, self.board)
                    possible_move = get_ordered_list(possible_move,close_defeated_index[1], close_defeated_index[2])
                    expand_list.append(possible_move)
                else:
                    expand_list.append(possible_move)
        
        # Find all combinations
        for i in product(*expand_list):
            temp = []
            temp = [list(j) for j in list(i)]
            result_list.append(temp)
        return result_list

    # Generate all child states for all new boards
    def expand_state(self):
        board_temp = {}
        child_states = []
        for i in self.expand_board():
            board_temp = {}
            board_temp[self.game.ally] = i
            board_temp[self.game.enemy] = [list(j) for j in self.board[self.game.enemy]]
            board_temp[self.game.block] = [list(j) for j in self.board[self.game.block]]
            child_states.append(State(self.game, board_temp, self, self.gn_cost +1))
        return child_states

    def __f(self):
        lower_self = 0
        for j in self.board[self.game.enemy]:
            if j[0] == 'x':
                lower_self += 1
        return lower_self

    def __lt__(self, other):
        return self.depth < other.depth
    
    # get closest point lower which could be defeated
    def get_closest_defeated_index(self, upper_index, board):
        distance = float('inf');
        cloest_index = None;
        for j in board[self.game.enemy]:
            if self.game.defeated(upper_index, j) is 'win' and dist(upper_index,j)<distance:
                cloest_index = j
        return cloest_index
                
