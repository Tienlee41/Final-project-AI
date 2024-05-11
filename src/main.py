import pygame

from Board import Board
from model.machine import Machine

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

#side = str(input())

player_side = "white"
machine_side = "black"
human_turn = True

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1],player_side)

font = pygame.font.Font(None, 36)

background_image = pygame.image.load("res/images/background.png")
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

def draw_start_menu():
    screen.blit(background_image, (0, 0))

    title_text = font.render('Chess', True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WINDOW_SIZE[0] // 2, 100))
    screen.blit(title_text, title_rect)

    # Vẽ nút "2 player"
    human_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 100, 250, 200, 50)
    pygame.draw.rect(screen, (200, 200, 200), human_button)
    human_text = font.render('Player vs Player', True, (0, 0, 0))
    human_text_rect = human_text.get_rect(center=human_button.center)
    screen.blit(human_text, human_text_rect)

    # Vẽ nút "1 player"
    ai_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 100, 350, 200, 50)
    pygame.draw.rect(screen, (200, 200, 200), ai_button)
    ai_text = font.render('Player vs Computer', True, (0, 0, 0))
    ai_text_rect = ai_text.get_rect(center=ai_button.center)
    screen.blit(ai_text, ai_text_rect)

    # Vẽ nút "Quit"
    exit_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 100, 450, 200, 50)
    pygame.draw.rect(screen, (200, 200, 200), exit_button)
    exit_text = font.render('Quit', True, (0, 0, 0))
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_text_rect)

board_states = [board.get_board_state()]

machine = Machine(machine_side)

def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()

def choose_man_side():
    global human_turn
    choosing_side = True
    
    background_image = pygame.image.load("res/images/background.png")  # Thay đổi đường dẫn tới hình nền của bạn
    background_image = pygame.transform.scale(background_image, WINDOW_SIZE)
    
    while choosing_side:
        screen.blit(background_image, (0, 0))
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)

        title_text = font_large.render('Choose Your Side', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_SIZE[0] // 2, 100))
        screen.blit(title_text, title_rect)

        # Vẽ nút "Black"
        black_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 100, 350, 200, 50)
        pygame.draw.rect(screen, (0, 0, 0), black_button)
        black_text = font_small.render('Black', True, (255, 255, 255))
        black_text_rect = black_text.get_rect(center=black_button.center)
        screen.blit(black_text, black_text_rect)

        # Vẽ nút "White"
        white_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 100, 250, 200, 50)
        pygame.draw.rect(screen, (255, 255, 255), white_button)
        white_text = font_small.render('White', True, (0, 0, 0))
        white_text_rect = white_text.get_rect(center=white_button.center)
        screen.blit(white_text, white_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Nút trái chuột
                    mx, my = pygame.mouse.get_pos()
                    if black_button.collidepoint((mx, my)):
                        human_turn = False
                        choosing_side = False
                    elif white_button.collidepoint((mx, my)):
                        human_turn = True
                        choosing_side = False
    

def player_vs_player():
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
    
def player_vs_computer():
    global human_turn  # Thêm dòng này để sử dụng biến human_turn từ phạm vi toàn cục
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # Quit the game if the user presses the close button
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if human_turn and event.button == 1:
                    board.handle_click(mx, my)
                    human_turn = False
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

        if board.get_board_state() != board_states[len(board_states)-1]:
            board_states.append(board.get_board_state())
            for row in board.get_board_state():
                print(row)
            print()

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Chess')
    
    draw_start_menu()
    pygame.display.update()
    
    running = True
    draw_start_menu()
    pygame.display.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Nút trái chuột
                    mx, my = pygame.mouse.get_pos()
                    # Kiểm tra xem người dùng có nhấn vào nút "2 player" không
                    if 250 <= my <= 300:
                        player_vs_player()
                        draw(screen)
                    # Kiểm tra xem người dùng có nhấn vào nút "1 player" không
                    elif 350 <= my <= 400:
                        choose_man_side()
                        player_vs_computer()
                        draw(screen)
                    # Kiểm tra xem người dùng có nhấn vào nút "Quit" không
                    elif 450 <= my <= 500:
                        running = False  # Dừng vòng lặp và thoát game

    pygame.quit()

if __name__ == '__main__':
    main()