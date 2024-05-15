import pygame
from pieces.Piece import Piece
from pieces.Queen import Queen

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.move_direction = 1 if board.get_player_side() == "white" else -1  # Hướng di chuyển của quân tốt
        self.en_passant_move = False  # Thuộc tính để đánh dấu nước đi en passant

        img_path = 'res/images/' + color[0] + '_pawn.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = ' '

    def get_possible_moves(self, board):
        output = []
        moves = []

        # Di chuyển về phía trước
        if self.color == 'white':
            moves.append((0, -1*self.move_direction))
            if not self.has_moved:
                moves.append((0, -2*self.move_direction))

        elif self.color == 'black':
            moves.append((0, 1*self.move_direction))
            if not self.has_moved:
                moves.append((0, 2*self.move_direction))

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
        en_passant_moves = self.en_passant_moves(board)
        for square in en_passant_moves:
            output.append(square)

        return output

    def promote(self, board):
        if (self.color == 'white' and self.y == 0) or (self.color == 'black' and self.y == 7):
            promoted_piece = Queen((self.x, self.y), self.color, board)
            board.set_piece_on_square(promoted_piece, self.x, self.y)
            board.remove_piece(self)

    def en_passant_moves(self, board):
        output = []

        # Lấy vị trí mục tiêu cho en passant
        target_square = board.en_passant_target_square

        if target_square is not None:
            target_x, target_y = target_square.x, target_square.y

            # Kiểm tra xem quân tốt đối phương đã di chuyển 2 ô và nằm ở hàng ngang với quân tốt hiện tại
            if abs(target_y - self.y) == 2 and target_y == 3.5 - 2.5 * self.move_direction:
                # Kiểm tra xem en passant có thể thực hiện về bên trái không
                if self.x - 1 == target_x:
                    # Tạo ô đích cho en passant
                    destination_square = board.get_square_from_pos((self.x - 1, target_y))
                    output.append(destination_square)
                    # Đánh dấu là nước đi en passant
                    destination_square.en_passant_move = True

                # Kiểm tra xem en passant có thể thực hiện về bên phải không
                if self.x + 1 == target_x:
                    # Tạo ô đích cho en passant
                    destination_square = board.get_square_from_pos((self.x + 1, target_y))
                    output.append(destination_square)
                    # Đánh dấu là nước đi en passant
                    destination_square.en_passant_move = True

        return output

    def attacking_squares(self, board):
        moves = []

        if self.color == 'white':
            moves.append((self.x - 1, self.y - 1))
            moves.append((self.x + 1, self.y - 1))
        elif self.color == 'black':
            moves.append((self.x - 1, self.y + 1))
            moves.append((self.x + 1, self.y + 1))

        # Kiểm tra bắt tốt qua đường
        target_square = board.en_passant_target_square
        if target_square is not None:
            # Nếu quân Tốt đối phương đã di chuyển 2 bước và nằm ở hàng ngang với quân Tốt hiện tại
            if abs(target_square.y - self.y) == 2 and target_square.y == 3.5 - 2.5 * self.move_direction:
                # Nếu quân Tốt hiện tại có thể bắt qua đường về bên trái
                if self.x - 1 == target_square.x:
                    moves.append((self.x - 1, self.y - self.move_direction))
                # Nếu quân Tốt hiện tại có thể bắt qua đường về bên phải
                elif self.x + 1 == target_square.x:
                    moves.append((self.x + 1, self.y - self.move_direction))

        # Lọc ra các ô nằm ngoài bàn cờ
        moves = [(x, y) for x, y in moves if 0 <= x < 8 and 0 <= y < 8]

        # Lọc ra các ô có quân địch
        output = []
        for x, y in moves:
            square = board.get_square_from_pos((x, y))
            if square.occupying_piece is not None and square.occupying_piece.color != self.color:
                output.append(square)

        return output
    
    def copy(self, new_board):
        return type(self)(self.pos, self.color, new_board)