"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching
Module: game
Created by ThePinkCoder (Yongfeng Qin & Yun-Chi Hsiao) on Mar.23rd 2021

This module contains a class named called Game which includes functions for
checking win condition by RoPaSci360 rule and generateing next valid moves.
"""
from search.utility import get_coord, same_coord, beside_coord

class Game:

    def __init__(self, init_board, ally='upper', enemy='lower', block='block'):
        self.init_board = init_board
        self.ally = ally
        self.enemy = enemy
        self.block = block

    # RoPaSci360 (or normal RoPaSci?!) combat rules
    def defeated(self, piece_1, piece_2):
        
        if ((piece_1[0] == 'r') and (piece_2[0] == 's')) or ((piece_1[0] == 's') and (piece_2[0] == 'p')) or ((piece_1[0] == 'p') and (piece_2[0] == 'r')):
            return 'win' 
        elif ((piece_1[0] == 'r') and (piece_2[0] == 'p')) or ((piece_1[0] == 's') and (piece_2[0] == 'r')) or ((piece_1[0] == 'p') and (piece_2[0] == 's')):
            return 'lose'
        elif ((piece_1[0] == 'r') and (piece_2[0] == 'r')) or ((piece_1[0] == 'p') and (piece_2[0] == 'p')) or ((piece_1[0] == 's') and (piece_2[0] == 's')):
            return 'draw'
        else:
            return 'invalid'

    # Update pieces on board (via defeated function)
    def update_board(self, board):

        for i in board[self.ally]:
            # Ally v.s Ally
            for ally in board[self.ally]:
                
                if same_coord(get_coord(i), get_coord(ally)):
                    
                    if self.defeated(i, ally) == 'win':
                        ally[0] = 'x'
                    
                    elif self.defeated(i, ally) == 'lose':
                        i[0] = 'x'
            # Ally v.s Enemy            
            for enemy in board[self.enemy]:
                
                if same_coord(get_coord(i), get_coord(enemy)):
                   
                    if self.defeated(i, enemy) == 'win':
                        enemy[0] = 'x'
                   
                    elif self.defeated(i, enemy) == 'lose':
                        i[0] = 'x'

        return board

    # Check the user has won
    def victory(self, board):
        
        for enemy in board[self.enemy]:
            if (enemy[0] != 'x'):
                return False

        # print(board)
        return True

    # Do slide action
    def slide(self, piece, board):
        
        row = get_coord(piece)[0]
        col = get_coord(piece)[1]

        possible_result_coord = [(row + 1, col - 1), (row + 1, col), (row, col - 1), (row, col + 1), (row - 1, col), (row - 1, col + 1)]

        result_pieces = []

        for i in possible_result_coord:
            if self.is_valid_move(i, board):
                result_pieces.append([piece[0], i[0], i[1]])

        return result_pieces
    
    # Do swing action 
    def swing(self, piece, board):
        
        possible_trans_pieces = self.slide(piece, board)
        possible_trans_coord = []
        trans_pieces = []
        possible_result_pieces = []
        result_pieces = []

        # Check transport spot is ally
        for i in possible_trans_pieces:
            # Get coordinates for later use
            possible_trans_coord.append(get_coord(i))
            for j in board[self.ally]:
                if same_coord(get_coord(i), get_coord(j)) is True:
                    trans_pieces.append(i)
        

        # Extand from transport spot
        for i in trans_pieces:
            possible_result_pieces += self.slide(i, board)

        # Check not staying at same spot and not repeating from slide move
        for i in possible_result_pieces: 
            coord = get_coord(i)
            if same_coord(get_coord(piece), coord) is False and coord not in possible_trans_coord:
                i[0] = piece[0]
                result_pieces.append(i) 
        
        return result_pieces

    # Generate all possible move for one piece
    def move(self, piece, board):
        return self.slide(piece, board) + self.swing(piece, board)

    # Check the spot is blocked or not
    def is_blocked(self, coord, board):     
        
        for i in board[self.block]:
            if same_coord(coord, get_coord(i)):
                return True 
        
        return False

    # Check the spot is out of boundary or not
    def out_boundary(self, coord):
   
        row = coord[0]
        col = coord[1]

        dict_valid = {4: (-4, 0), 3: (-4, 1), 2: (-4, 2), 1: (-4, 3), 0: (-4, 4), -1: (-3, 4), -2: (-2, 4), -3: (-1, 4), -4: (0, 4)}
        
        if (row not in dict_valid.keys()):
            return True

        min_col = dict_valid[coord[0]][0]
        max_col = dict_valid[coord[0]][1]
               
        if col < min_col or col > max_col:
            return True
        
        return False

    # Check the new spot is valid or not
    def is_valid_move(self, coord, board):
        if (self.is_blocked(coord, board) or self.out_boundary(coord)) is True:
            return False
        return True

    # Extended function for future use(Project-B?)
    def tie_or_defeated(self, board):
        defeated = 0
        lower = 0
        for j in board[self.enemy]:
            if j[0] != 'x':
                lower += 1
        for i in board[self.ally]:
            for j in board[self.enemy]:
                if self.defeated(i,j) is 'win':
                    defeated += 1
        if lower <= defeated:
            return False
        return True


    # Extended function for future use(Project-B?)
    def gama_over(self, board):
        if (self.victory(board) or self.tie_or_defeated(board)) is True:
            return True
        return False