import pygame

from Square import Square
from pieces.Rook import Rook
from pieces.Bishop import Bishop
from pieces.Knight import Knight
from pieces.Queen import Queen
from pieces.King import King
from pieces.Pawn import Pawn
from model.machine import Machine



# Game state checker
class Board:
	def __init__(self, width, height,player_side):
		self.width = width
		self.height = height
		self.player_side = player_side

		self.tile_width = width // 8
		self.tile_height = height // 8
		self.selected_piece = None
		self.turn = 'white'
		self.en_passant_target_square = None

		self.config_white_start = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
			['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
		]
		self.config_black_start = [
			['wR', 'wN', 'wB', 'wK', 'wQ', 'wB', 'wN', 'wR'],
			['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
			['bR', 'bN', 'bB', 'bK', 'bQ', 'bB', 'bN', 'bR'],
		]

		self.squares = self.generate_squares()

		self.setup_board()

	def get_player_side(self):
		return self.player_side	

	def set_en_passant_target_square(self, square):
		self.en_passant_target_square = square

	def generate_squares(self):
		output = []
		for y in range(8):
			for x in range(8):
				output.append(
					Square(x,  y, self.tile_width, self.tile_height)
				)
		return output


	def get_square_from_pos(self, pos):
		for square in self.squares:
			if (square.x, square.y) == pos:
				return square



	def get_piece_from_pos(self, pos):
		return self.get_square_from_pos(pos).occupying_piece


	def setup_board(self):
		# iterating 2d list
		if self.player_side == "white":
			config = self.config_white_start
		else :
			config = self.config_black_start
		#self.board_config = config
		for y, row in enumerate(config):
			for x, piece in enumerate(row):
				if piece != '':
					square = self.get_square_from_pos((x, y))

					# looking inside contents, what piece does it have
					if piece[1] == 'R':
						square.occupying_piece = Rook(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					# as you notice above, we put `self` as argument, or means our class Board

					elif piece[1] == 'N':
						square.occupying_piece = Knight(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'B':
						square.occupying_piece = Bishop(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'Q':
						square.occupying_piece = Queen(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'K':
						square.occupying_piece = King(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'P':
						square.occupying_piece = Pawn(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

	def get_board_state(self): # tra ve trang thai thuc cua ban co
		board_state = []
		for y in range(8):
			row = []
			for x in range(8):
				square = self.get_square_from_pos((x, y))
				if square.occupying_piece is not None:
					row.append(square.occupying_piece.color[0] + square.occupying_piece.notation[0])
				else:
					row.append('')
			board_state.append(row)
		return board_state

	def handle_click(self, mx, my):
		x = mx // self.tile_width
		y = my // self.tile_height
		clicked_square = self.get_square_from_pos((x, y))
		if self.selected_piece is None:
			if clicked_square.occupying_piece is not None:
				if clicked_square.occupying_piece.color == self.turn:
					self.selected_piece = clicked_square.occupying_piece
		elif self.selected_piece.move(self, clicked_square):
			self.turn = 'white' if self.turn == 'black' else 'black'
		elif clicked_square.occupying_piece is not None:
			if clicked_square.occupying_piece.color == self.turn:
				self.selected_piece = clicked_square.occupying_piece

	def handle_click_pvc(self, mx, my,player_side):
		x = mx // self.tile_width
		y = my // self.tile_height
		clicked_square = self.get_square_from_pos((x, y))
		if self.selected_piece is None:
			if clicked_square.occupying_piece is not None:
				if clicked_square.occupying_piece.color == player_side:
					self.selected_piece = clicked_square.occupying_piece
		elif self.selected_piece.move(self, clicked_square):
			return True
		elif clicked_square.occupying_piece is not None:
			if clicked_square.occupying_piece.color == player_side:
				self.selected_piece = clicked_square.occupying_piece
		return False

	def is_in_check(self, color, board_change=None): # board_change = [(x1, y1), (x2, y2)]
		output = False
		king_pos = None

		changing_piece = None
		old_square = None
		new_square = None
		new_square_old_piece = None

		if board_change is not None:
			for square in self.squares:
				if square.pos == board_change[0]:
					changing_piece = square.occupying_piece
					old_square = square
					old_square.occupying_piece = None
			for square in self.squares:
				if square.pos == board_change[1]:
					new_square = square
					new_square_old_piece = new_square.occupying_piece
					new_square.occupying_piece = changing_piece

		pieces = [
			i.occupying_piece for i in self.squares if i.occupying_piece is not None
		]

		if changing_piece is not None:
			if changing_piece.notation == 'K':
				king_pos = new_square.pos
		if king_pos == None:
			for piece in pieces:
				if piece.notation == 'K' and piece.color == color:
						king_pos = piece.pos
		for piece in pieces:
			if piece.color != color:
				for square in piece.attacking_squares(self):
					if square.pos == king_pos:
						output = True

		if board_change is not None:
			old_square.occupying_piece = changing_piece
			new_square.occupying_piece = new_square_old_piece
		return output

	def is_in_checkmate(self, color):
		# Kiểm tra xem vua của bên đang bị tấn công hay không
		if not self.is_in_check(color):
			return False  # Không phải checkmate nếu vua không bị tấn công

		# Lặp qua tất cả các quân cờ của bên
		for piece in [i.occupying_piece for i in self.squares if i.occupying_piece is not None and i.occupying_piece.color == color]:
			# Kiểm tra từng nước đi hợp lệ của từng quân cờ
			for move in piece.get_valid_moves(self):
				# Tạo một bản sao của bảng để thử nghiệm nước đi
				test_board = self.copy_board()
				test_board.move_piece(piece.pos, move)

				# Kiểm tra xem vua đã không còn bị tấn công
				if not test_board.is_in_check(color):
					return False

		# Kiểm tra xem có nước đi nào để bảo vệ vua không
		opposite_color = 'white' if color == 'black' else 'black'
		for piece in [i.occupying_piece for i in self.squares if i.occupying_piece is not None and i.occupying_piece.color == color]:
			for move in piece.get_valid_moves(self):
				test_board = self.copy_board()
				test_board.move_piece(piece.pos, move)

				# Kiểm tra xem sau nước đi này, có cách nào để bảo vệ vua không
				if not any(test_board.is_in_checkmate(opposite_color) for piece in [i.occupying_piece for i in test_board.squares if i.occupying_piece is not None and i.occupying_piece.color == opposite_color] for move in piece.get_valid_moves(test_board)):
					return False

		# Nếu không có bất kỳ nước đi nào cho bất kỳ quân cờ nào và vua vẫn bị tấn công, là checkmate
		return True

	def move_piece(self, start_pos, end_pos):
		start_square = self.get_square_from_pos(start_pos)
		end_square = self.get_square_from_pos(end_pos)

		# Kiểm tra xem ô đầu có quân cờ không và quân cờ có thể di chuyển đến ô cuối không
		if start_square.occupying_piece is None or not start_square.occupying_piece.move(self, end_square):
			return False  # Không thể di chuyển quân cờ

		# Di chuyển quân cờ từ ô đầu đến ô cuối
		end_square.occupying_piece = start_square.occupying_piece
		start_square.occupying_piece = None
		return True

	def copy_board(self):
		# Tạo một bản sao mới của bảng và sao chép trạng thái của mỗi ô và quân cờ
		copied_board = Board(self.width, self.height, self.player_side)
		for y in range(8):
			for x in range(8):
				original_square = self.get_square_from_pos((x, y))
				copied_square = copied_board.get_square_from_pos((x, y))
				if original_square.occupying_piece is not None:
					copied_square.occupying_piece = original_square.occupying_piece.copy(copied_board)
		return copied_board


	def draw(self, display):
		if self.selected_piece is not None:
			self.get_square_from_pos(self.selected_piece.pos).highlight = True
			for square in self.selected_piece.get_valid_moves(self):
				square.highlight = True

		for square in self.squares:
			square.draw(display)

	def get_name_pos(self,x,y):
		if self.player_side == "white":
			return str(chr(ord('a')+x)+str(8-y))
		else :
			return str(chr(ord('h')-x)+str(y+1))

	def update_board(self, board_state):
		for y in range(8):
			for x in range(8):
				piece = board_state[y][x]
				square = self.get_square_from_pos((x, y))

				if piece != '':
					# Xóa quân cờ hiện tại trên ô cờ
					square.occupying_piece = None

					# Đặt quân cờ mới lên ô cờ
					if piece[1] == 'R':
						square.occupying_piece = Rook(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					elif piece[1] == 'N':
						square.occupying_piece = Knight(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					elif piece[1] == 'B':
						square.occupying_piece = Bishop(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					elif piece[1] == 'Q':
						square.occupying_piece = Queen(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					elif piece[1] == 'K':
						square.occupying_piece = King(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					elif piece[0] == 'w':
						square.occupying_piece = Pawn(
							(x, y), 'white', self
						)
					elif piece[0] == 'b':
						square.occupying_piece = Pawn(
							(x, y), 'black', self
						)
				else:
					square.occupying_piece = None
