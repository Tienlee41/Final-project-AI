from Board import Board
from Square import Square

WINDOW_SIZE = (600, 600)
board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1],"white")
piece = board.get_square_from_pos((2,1)).occupying_piece
val_moves = piece.get_possible_moves(board) 
board_states = board.get_board_state()
board_states.append(board.get_board_state())
b = board.get_board_state()
b[1][2] = 'aa'
for row in b:
    print(row)
print()
for i in val_moves:
    print((i.y,i.x))
s = "e7e5"
x = 8 - int(s[3])
y = ord(s[2])-ord('a')
print(x,y)