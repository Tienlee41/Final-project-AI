import pygame
import random
import queue
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
        self.depth = 3

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
    
    

    def find_best_move(self, board,valid_moves,moves_queue):
        global next_move
        next_move = None
        #random.shuffle(valid_moves)
        #print(type(valid_moves[0]))
        self.MegaMaxAlphaBeta(board, valid_moves,1 if board.player_turn else -1)
        #print(next_move.start_row,next_move.start_col,next_move.end_row,next_move.end_col)
        moves_queue.put(next_move)
    
    def score(self,board_state):
        if board_state.is_in_checkmate(self.machine_side):
            return -self.checkmate
        elif board_state.is_in_checkmate(self.player_side):
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
    
    
    
    def MegaMaxAlphaBeta(self,board,valid_moves,depth,alpha,beta,turn):
        global next_move
        if depth == 0:
            return (1 if turn == self.machine_side else -1) * self.score(board.get_board_state())
        max_score = -self.checkmate
        for move in valid_moves:
            new_board_state = self.make_move(move)
            next_moves = new_board_state.get_valid_moves()
            score = -self.MegaMaxAlphaBeta(new_board_state, next_moves, depth-1, -alpha, -beta, -turn)
            if score > max_score:
                max_score = score
                if depth == self.depth:
                    next_move = move
        return max_score
    
    def randomMove(valid_moves):
        return random.choice(valid_moves)