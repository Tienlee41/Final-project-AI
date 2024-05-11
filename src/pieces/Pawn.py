import pygame
from pieces.Piece import Piece
from pieces.Queen import Queen

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)

        img_path = 'res/images/' + color[0] + '_pawn.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 35, board.tile_height - 35))

        self.notation = ' '

    def get_possible_moves(self, board):
        output = []
        moves = []

        # Di chuyển về phía trước
        if self.color == 'white':
            moves.append((0, -1))
            if not self.has_moved:
                moves.append((0, -2))

        elif self.color == 'black':
            moves.append((0, 1))
            if not self.has_moved:
                moves.append((0, 2))

        for move in moves:
            new_pos = (self.x, self.y + move[1])
            if new_pos[1] < 8 and new_pos[1] >= 0:
                output.append(
                    board.get_square_from_pos(new_pos)
                )

        return output

    def get_moves(self, board):
        output = []
        possible_moves = self.get_possible_moves(board)

        # Kiểm tra di chuyển về phía trước
        for square in possible_moves:
            if square.occupying_piece is not None:
                break
            else:
                output.append(square)

        # Kiểm tra di chuyển chéo để bắt quân
        diagonal_moves = self.attacking_squares(board)
        for square in diagonal_moves:
            output.append(square)

        # Kiểm tra bắt tốt qua đường
        if board.en_passant_target_square is not None:
            en_passant_square = board.en_passant_target_square
            target_x, target_y = en_passant_square.pos

            if self.color == 'white':
                # Kiểm tra xem ô mục tiêu cho en passant có nằm ở bên trái hoặc bên phải của quân tốt không
                if (target_x - 1, target_y) == (self.x, self.y - 1) or (target_x + 1, target_y) == (self.x, self.y - 1):
                    output.append(en_passant_square)
            elif self.color == 'black':
                # Kiểm tra xem ô mục tiêu cho en passant có nằm ở bên trái hoặc bên phải của quân tốt không
                if (target_x - 1, target_y) == (self.x, self.y + 1) or (target_x + 1, target_y) == (self.x, self.y + 1):
                    output.append(en_passant_square)

        return output
    
    def promote(self, board):
        if (self.color == 'white' and self.y == 0) or (self.color == 'black' and self.y == 7):
            promoted_piece = Queen((self.x, self.y), self.color, board)
            board.set_piece_on_square(promoted_piece, self.x, self.y)
            board.remove_piece(self)

    def attacking_squares(self, board):
        moves = []

        if self.color == 'white':
            moves.append((self.x - 1, self.y - 1))
            moves.append((self.x + 1, self.y - 1))
        elif self.color == 'black':
            moves.append((self.x - 1, self.y + 1))
            moves.append((self.x + 1, self.y + 1))

        # Lọc ra các ô nằm ngoài bàn cờ
        moves = [(x, y) for x, y in moves if 0 <= x < 8 and 0 <= y < 8]

        # Lọc ra các ô có quân địch
        output = []
        for x, y in moves:
            square = board.get_square_from_pos((x, y))
            if square.occupying_piece is not None and square.occupying_piece.color != self.color:
                output.append(square)

        return output
