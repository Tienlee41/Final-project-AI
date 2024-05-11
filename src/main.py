import pygame
from pygame.locals import *
from Board import Board

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Chess game')

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1], 'white')

font = pygame.font.Font(None, 36)

background_image = pygame.image.load("res/images/background.png")
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)

def draw_start_menu():
    screen.blit(background_image, (0, 0))

    title_text = font.render('Chess', True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(WINDOW_SIZE[0] // 2, 100))
    screen.blit(title_text, title_rect)

    # Vẽ nút "2 player"
    human_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 100, 250, 200, 50)
    pygame.draw.rect(screen, (200, 200, 200), human_button)
    human_text = font.render('2 player', True, (0, 0, 0))
    human_text_rect = human_text.get_rect(center=human_button.center)
    screen.blit(human_text, human_text_rect)

    # Vẽ nút "1 player"
    ai_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 100, 350, 200, 50)
    pygame.draw.rect(screen, (200, 200, 200), ai_button)
    ai_text = font.render('1 player', True, (0, 0, 0))
    ai_text_rect = ai_text.get_rect(center=ai_button.center)
    screen.blit(ai_text, ai_text_rect)

    # Vẽ nút "Quit"
    exit_button = pygame.Rect((WINDOW_SIZE[0] // 2) - 100, 450, 200, 50)
    pygame.draw.rect(screen, (200, 200, 200), exit_button)
    exit_text = font.render('Quit', True, (0, 0, 0))
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_text_rect)


def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()

# code chơi với người
def play_with_human():
    running_game = True
    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Nút trái chuột
                    mx, my = pygame.mouse.get_pos()
                    square_clicked = check_square_clicked(mx, my)
        draw(screen)

# code chơi với máy
def play_with_computer():
    running_game = True
    while running_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Nút trái chuột
                    mx, my = pygame.mouse.get_pos()
                    square_clicked = check_square_clicked(mx, my)
        draw(screen)

def main():
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
                        play_with_human()
                        draw(screen)
                    # Kiểm tra xem người dùng có nhấn vào nút "1 player" không
                    elif 350 <= my <= 400:
                        play_with_computer()
                        draw(screen)
                    # Kiểm tra xem người dùng có nhấn vào nút "Quit" không
                    elif 450 <= my <= 500:
                        running = False  # Dừng vòng lặp và thoát game

    pygame.quit()

if __name__ == '__main__':
    main()
