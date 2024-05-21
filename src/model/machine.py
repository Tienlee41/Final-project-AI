import pygame
import random
from pieces.Piece import Piece
from pieces.Rook import Rook
from pieces.Bishop import Bishop
from pieces.Knight import Knight
from pieces.Queen import Queen
from pieces.King import King
from pieces.Pawn import Pawn
#from Board import Board
from Square import Square

class Machine:
    def __init__(self, machine_side):
        self.machine_side = machine_side
        self.player_side = "white" if machine_side == "black" else "white"
        self.a = 0
        piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
        self.checkmate = 1000
        self.stalemate = 0
        self.depth = 5

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
                                "wP": self.pawn_scores,
                                "bP": self.pawn_scores[::-1]}
    
    def move_to_coordinate(self,s):
        x = 8 - int(s[3])
        y = ord(s[2])-ord('a')
        return (x,y)

    def make_move(self, board):
        # 1 move có dạng : e3xe7 hoặc e3e5 (x là ăn)
        # move = self.findMoveMegaMaxAlphaBeta(board_state)
        # if ("x" in move):
        #     ewq
        # else :
        moves = "e7e5"
        atmoves = "bPe5xd4"
        new_board_state = board.get_board_state()
        #move = 
        new_board_state[self.move_to_coordinate(moves[-2])[0]][self.move_to_coordinate(moves[-2])[1]] = new_board_state[self.move_to_coordinate(moves[2:4])[0]][self.move_to_coordinate(moves[2:4])[1]]
            # test 1 nuoc di
        # if self.machine_side == "black":
        #     if self.a == 0:
        #         new_board_state[1][7] = ''
        #         new_board_state[2][7] = 'bP'
        #         new_board_state[3][2] = 'bP'
        #         self.a +=1 
        #     else :
        #         new_board_state[1][4] = ''
        #         new_board_state[3][4] = 'bP'
        # else :
        #     new_board_state[1][7] = ''
        #     new_board_state[2][7] = 'wP '
        return new_board_state
    
    def score(self,board_state):
        if board_state.is_in_checkmate(self.machine_side):
            return -self.checkmate
        elif board_state.is_in_checkmate(play):
            return self.checkmate
        score = 0
        for x in range(8):
            for y in range(9):
                piece = board_state[x][y]
                if piece != '':
                    piece_position_score = 0
                    if piece[1] != "K":
                        piece_position_score = self.piece_position_scores[piece][x][y]
                    if piece[0] == self.machine_side[0]:
                        score += self.piece_score[piece[1]] + piece_position_score
                    if piece[0] == self.player_side[0]:
                        score -= self.piece_score[piece[1]] + piece_position_score
        return score
    
    
    
    def findMoveMegaMaxAlphaBeta(self,board_states):
        pass
    
    def randomMove(valid_moves):
        return random.choice(valid_moves)