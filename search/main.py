"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching
Module: main
Created by ThePinkCoder (Yongfeng Qin & Yun-Chi Hsiao) on Mar.23rd 2021

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). It would execute the initialization of a new
RoPaSci360 game with the provided board and start printing out the solution as
the project required. 
"""

import sys
import json
import search.utility as utility
import search.game as game
import search.state as state
import search.algorithm as algorithm


# Main function
def main():
    
    try:
        with open(sys.argv[1]) as file:
            init_board = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # Start run the game
    new_game = game.Game(init_board)
    init_state = state.State(new_game, init_board)
    solution_state, expend_node = algorithm.a_star(new_game, init_state)
    if solution_state is not None:
        utility.print_transcript_text(solution_state)
        # utility.print_transcript_board(solution_state)





