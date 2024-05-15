import pygame
import sys
import os
from pieces.Piece import Piece
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Bishop import Bishop
from pieces.Knight import Knight

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.move_direction = 1 if board.get_human_side() == "white" else -1  # Hướng di chuyển của quân tốt
        self.en_passant_move = False  # Thuộc tính để đánh dấu nước đi en passant
        self.can_be_taken_en_passant = False  # Cho biết liệu tốt này có thể bị bắt qua đường không

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
    
    def en_passant_moves(self, board):
        output = []

        # Lấy vị trí mục tiêu cho en passant
        target_square = board.en_passant_target_square

        if target_square is not None:
            target_x, target_y = target_square.x, target_square.y

            # Kiểm tra xem en passant có thể thực hiện về bên trái không
            if self.x - 1 == target_x and abs(self.y - target_y) == 1:
                # Tạo ô đích cho en passant
                destination_square = board.get_square_from_pos((self.x - 1, self.y))
                output.append(destination_square)
                # Đánh dấu là nước đi en passant
                destination_square.en_passant_move = True

            # Kiểm tra xem en passant có thể thực hiện về bên phải không
            elif self.x + 1 == target_x and abs(self.y - target_y) == 1:
                # Tạo ô đích cho en passant
                destination_square = board.get_square_from_pos((self.x + 1, self.y))
                output.append(destination_square)
                # Đánh dấu là nước đi en passant
                destination_square.en_passant_move = True

        return output

    def promote(self, board):
        chosen_piece = self.display_promotion_options(self.color)
        if chosen_piece == "Queen":
            return Queen((self.x, self.y), self.color, board)
        elif chosen_piece == "Knight":
            return Knight((self.x, self.y), self.color, board)
        elif chosen_piece == "Bishop":
            return Bishop((self.x, self.y), self.color, board)
        elif chosen_piece == "Rook":
            return Rook((self.x, self.y), self.color, board)

    def display_promotion_options(self, pawn_color):
        pygame.init()
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        WINDOW_WIDTH = 400
        WINDOW_HEIGHT = 200
        BACKGROUND_COLOR = (150, 150, 150)
        TEXT_COLOR = (0, 0, 0)
        FONT_SIZE = 30
        font = pygame.font.SysFont(None, FONT_SIZE)

        title_text = font.render("Choose a piece to promote to:", True, TEXT_COLOR)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, FONT_SIZE))

        # Các lựa chọn
        options = ["Queen", "Knight", "Bishop", "Rook"]
        num_options = len(options)
        OPTION_WIDTH = 100
        OPTION_HEIGHT = 100

        initial_x = (WINDOW_WIDTH - num_options * OPTION_WIDTH) // 2
        initial_y = FONT_SIZE

        images = {}
        option_rects = []  # Tạo list để lưu các hình chữ nhật cho lựa chọn

        for i, option in enumerate(options):
            option_rect = pygame.Rect(initial_x + i * OPTION_WIDTH + 10, initial_y + 10, OPTION_WIDTH - 20, OPTION_HEIGHT - 20)  # Điều chỉnh vị trí và kích thước của hình chữ nhật
            option_rects.append(option_rect)  # Thêm hình chữ nhật vào list

            # Vẽ hình chữ nhật đại diện cho lựa chọn
            pygame.draw.rect(screen, BACKGROUND_COLOR, option_rect, border_radius=5)

            image_path = os.path.join("res/images", f"{pawn_color[0]}_{option.lower()}.png")
            images[option] = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(images[option], (OPTION_WIDTH - 20, OPTION_HEIGHT - 20))  # Giảm kích thước để hiển thị đẹp hơn

            # Vẽ hình ảnh quân cờ lên hình chữ nhật
            screen.blit(image, (option_rect.x + 10, option_rect.y + 10))

        # Vẽ nền và tiêu đề
        screen.fill(BACKGROUND_COLOR)
        screen.blit(title_text, title_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Kiểm tra xem người chơi nhấp chuột vào lựa chọn nào
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(mouse_pos):
                            return options[i]

            clock.tick(30)


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

        # Kiểm tra bắt tốt qua đường
        if self.can_be_taken_en_passant:
            # Nếu tốt này có thể bị bắt qua đường, thêm các ô đích vào danh sách nước đi
            if self.color == 'white':
                target_square = board.get_square_from_pos((self.x, self.y - 1))
                if target_square is not None and target_square.occupying_piece is not None and target_square.occupying_piece.color != self.color:
                    output.append(target_square)
            elif self.color == 'black':
                target_square = board.get_square_from_pos((self.x, self.y + 1))
                if target_square is not None and target_square.occupying_piece is not None and target_square.occupying_piece.color != self.color:
                    output.append(target_square)

        return output

    def update_can_be_taken_en_passant(self, board):
        if self.color == 'white':
            target_square = board.get_square_from_pos((self.x, self.y - 2))
        elif self.color == 'black':
            target_square = board.get_square_from_pos((self.x, self.y + 2))
        if target_square is not None and target_square.occupying_piece is not None and target_square.occupying_piece.color != self.color:
            # Nếu có tốt đối phương nằm ngay bên cạnh và có thể bắt qua đường, đặt thuộc tính can_be_taken_en_passant thành True
            self.can_be_taken_en_passant = True
            ## if không bị bắt ngay sau đó thì can_be_taken_en_passant = False
        else:
            self.can_be_taken_en_passant = False
    
    def copy(self, new_board):
        return type(self)(self.pos, self.color, new_board)