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
        self.a = 0
        piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

        self.knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                        [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                        [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                        [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                        [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                        [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                        [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                        [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

        self.bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                        [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                        [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                        [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                        [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                        [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                        [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                        [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

        self.rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                    [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                    [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

        self.queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                        [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                        [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                        [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                        [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                        [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                        [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                        [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

        self.pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                    [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                    [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                    [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                    [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                    [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                    [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                    [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

        self.piece_position_scores = {"wN": self.knight_scores,
                                "bN": self.knight_scores[::-1],
                                "wB": self.bishop_scores,
                                "bB": self.bishop_scores[::-1],
                                "wQ": self.queen_scores,
                                "bQ": self.queen_scores[::-1],
                                "wR": self.rook_scores,
                                "bR": self.rook_scores[::-1],
                                "wp": self.pawn_scores,
                                "bp": self.pawn_scores[::-1]}
        self.checkmate = 1000
        self.stalemate = 0
        self.depth = 5
    
    

    def make_move(self, board_state):
        new_board_state = board_state
            # test 1 nuoc di
        if self.machine_side == "black":
            if self.a == 0:
                new_board_state[1][7] = ''
                new_board_state[2][7] = 'b '
                self.a +=1 
            else :
                new_board_state[1][4] = ''
                new_board_state[3][4] = 'b '
        else :
            new_board_state[1][7] = ''
            new_board_state[2][7] = 'w '
        return new_board_state