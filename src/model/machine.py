import pygame
import random
from pieces.Rook import Rook
from pieces.Bishop import Bishop
from pieces.Knight import Knight
from pieces.Queen import Queen
from pieces.King import King
from pieces.Pawn import Pawn

class Machine:
    def __init__(self, machine_side):
        self.machine_side = machine_side
        self.rook = 5
        self.bishop = 3
        self.knight = 3
        self.queen = 9
        self.pawn = 1
        self.king = 2000


    def get_next_move(self, board_state):
        # return a move (random)
        if self.machine_side == "white" :
            ms = "w"
        else : 
            ms = "b"
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if board_state[y][x] != '':
                    if board_state[y][x][0] == ms:
                        valid_moves.extend(self.get_valid_moves(board_state, (x, y)))
        if valid_moves:
            return random.choice(valid_moves)
        else:
            return None

    def get_valid_moves(self, board_state, pos):
        moves = []
        return moves
