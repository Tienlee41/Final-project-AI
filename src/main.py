import pygame

from Board import Board
from model.machine import Machine

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

player_side = "white"
machine_side = "black"
player_turn = True
board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1],player_side)
board_states = [board.get_board_state()]


font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 86)

background_image = pygame.image.load("res/images/background.png")
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

def draw_start_menu():
    screen.blit(background_image, (0, 0))

    title_text = title_font.render('Chess', True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WINDOW_SIZE[0] // 2, 125))
    screen.blit(title_text, title_rect)

    # Vẽ nút "2 player"
    player_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 125, 250, 250, 50)
    pygame.draw.rect(screen, (200, 200, 200), player_button)
    player_text = font.render('Player vs Player', True, (0, 0, 0))
    player_text_rect = player_text.get_rect(center=player_button.center)
    screen.blit(player_text, player_text_rect)

    # Vẽ nút "1 player"
    ai_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 125, 350, 250, 50)
    pygame.draw.rect(screen, (200, 200, 200), ai_button)
    ai_text = font.render('Player vs Computer', True, (0, 0, 0))
    ai_text_rect = ai_text.get_rect(center=ai_button.center)
    screen.blit(ai_text, ai_text_rect)

    # Vẽ nút "Quit"
    exit_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 125, 450, 250, 50)
    pygame.draw.rect(screen, (200, 200, 200), exit_button)
    exit_text = font.render('Quit', True, (0, 0, 0))
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_text_rect)


def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()

def choose_man_side():
    global board
    global player_turn
    global machine_side
    global player_side
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
                        player_side = "black"
                        machine_side = "white"
                        player_turn = False
                        choosing_side = False
                    elif white_button.collidepoint((mx, my)):
                        player_turn = True
                        choosing_side = False
        board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1],player_side)


def draw_end_game_whitewin():
    running = True
    while running:
        message = "White wins!"
        text = title_font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
        screen.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

    reset_game()
    main()

def draw_end_game_blackwin():
    running = True
    while running:
        message = "Black wins!"
        text = title_font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
        screen.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

    reset_game()
    main()

def reset_game():
    # Đặt lại các biến cần thiết
    global board
    global board_states
    global player_side
    global machine_side
    global player_turn

    # Các biến cần thiết sẽ được đặt lại về trạng thái ban đầu
    board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1], "white")
    board_states = [board.get_board_state()]
    player_side = "white"
    machine_side = "black"
    player_turn = True

    # Hiển thị menu khởi đầu lại
    draw_start_menu()
    pygame.display.update()
    
def check_win(board):
    if board.is_in_checkmate('black') | board.is_in_checkmate('white') :
        return True
    return False

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
        if check_win(board):
            running = False
        draw(screen)
        if board.get_board_state() != board_states[len(board_states)-1] :
            board_states.append(board.get_board_state())
            for row in board.get_board_state():
                print(row)
            print()

def player_vs_computer():
    global player_turn 
    global player_side
    global machine_side
    running = True
    machine = Machine(machine_side)
    print(machine_side)
    while running:
        mx, my = pygame.mouse.get_pos()  # Get mouse position for potential player move

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player_turn & board.handle_click_pvc(mx, my, player_side):
                    player_turn = not player_turn
            if not player_turn :
                machine_move = machine.make_move(board)  # Get computer's move
                board.update_board(machine_move)
                player_turn = not player_turn
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
                        running = False
                    # Kiểm tra xem người dùng có nhấn vào nút "1 player" không
                    elif 350 <= my <= 400:
                        choose_man_side()
                        player_vs_computer()
                        draw(screen)
                        running = False
                    # Kiểm tra xem người dùng có nhấn vào nút "Quit" không
                    elif 450 <= my <= 500:
                        pygame.quit()  # Dừng vòng lặp và thoát game

    if board.is_in_checkmate('black'): # If black is in checkmate
        draw_end_game_whitewin()
    elif board.is_in_checkmate('white'):
        draw_end_game_blackwin()
    pygame.quit()
    

if __name__ == '__main__':
    main()
    