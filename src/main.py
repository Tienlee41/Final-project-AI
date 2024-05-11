import pygame

from Board import Board
from model.machine import Machine

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

#side = str(input())

human_side = "white"
machine_side = "black"
human_turn = True

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1],human_side)

if human_side == "black" :
    machine_side = "white"
    human_turn = False

board_states = [board.get_board_state()]

machine = Machine(machine_side)

def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()

def check_win(board) :
    if board.is_in_checkmate('black'): # If black is in checkmate
        print('White wins!')
        return False
    elif board.is_in_checkmate('white'): # If white is in checkmate
        print('Black wins!')
        return False
    return True

def man_vs_man():
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1:
                    board.handle_click(mx, my)
        if board.is_in_checkmate('black'): # If black is in checkmate
            print('White wins!')
            running = False
        elif board.is_in_checkmate('white'): # If white is in checkmate
            print('Black wins!')
            running = False
        draw(screen)
        if board.get_board_state() != board_states[len(board_states)-1] :
            board_states.append(board.get_board_state())
            for row in board.get_board_state():
                print(row)
            print()
    for i in board_states:
        for row in i:
            print(row)
        print()
    
def man_vs_computer():
	running = True
	while running:
		mx, my = pygame.mouse.get_pos()
		for event in pygame.event.get():
			# Quit the game if the user presses the close button
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN : 
				if human_turn and event.button == 1 :
						board.handle_click(mx, my)
						human_turn = False
				else:
					next_move = machine.get_next_move(board.get_board_state())
					board.handle_click(next_move[0] * board.tile_width, next_move[1] * board.tile_height)
					human_turn = True
		if board.is_in_checkmate('black'): # If black is in checkmate
			print('White wins!')
		elif board.is_in_checkmate('white'): # If white is in checkmate
			print('Black wins!')
		if not human_turn:
			next_move = machine.get_next_move(board.get_board_state())
			board.handle_click(next_move[0] * board.tile_width, next_move[1] * board.tile_height)
			human_turn = True
		# Draw the board
		draw(screen)

		if board.get_board_state() != board_states[len(board_states)-1] :
			board_states.append(board.get_board_state())
			for row in board.get_board_state():
				print(row)
			print()
	for i in board_states:
		for row in i:
			print(row)
		print()


if __name__ == '__main__':
    man_vs_man()