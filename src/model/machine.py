import random

class Machine:
    def __init__(self,machine_side):
        self.machine_side = machine_side
    def get_next_move(self, board_state):
        #random moves
        empty_squares = []
        empty_squares = []
        for y, row in enumerate(board_state):
            for x, piece in enumerate(row):
                if piece == '':
                    empty_squares.append((x, y))
        
        if empty_squares:
            return random.choice(empty_squares)
        else:
            return None 