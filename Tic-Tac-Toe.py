# pygame → pip install pygame
# numpy → pip install numpy
# python --version
# pip --version

import sys
import pygame
import numpy as np
import time

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)
HOVER = (80, 80, 80)

# Sizes
WIDTH, HEIGHT = 600, 650
SQUARE_SIZE = WIDTH // 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')

font = pygame.font.SysFont(None, 35)

board = np.zeros((3, 3))

HUMAN = 1
AI = 2

game_over = False
ai_thinking = False

# Scores
human_score = 0
ai_score = 0

# Restart Button
button_rect = pygame.Rect(200, 605, 200, 40)

# ---------------- DRAW ---------------- #
def draw_lines():
    screen.fill(BLACK)
    for i in range(1, 3):
        pygame.draw.line(screen, WHITE, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), 8)
        pygame.draw.line(screen, WHITE, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, WIDTH), 8)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == HUMAN:
                pygame.draw.circle(screen, WHITE,
                    (col * 200 + 100, row * 200 + 100), 50, 8)
            elif board[row][col] == AI:
                pygame.draw.line(screen, WHITE,
                    (col * 200 + 50, row * 200 + 50),
                    (col * 200 + 150, row * 200 + 150), 8)
                pygame.draw.line(screen, WHITE,
                    (col * 200 + 50, row * 200 + 150),
                    (col * 200 + 150, row * 200 + 50), 8)

def draw_winning_line(player):
    for row in range(3):
        if all(board[row][col] == player for col in range(3)):
            pygame.draw.line(screen, RED, (0, row*200+100), (600, row*200+100), 10)

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            pygame.draw.line(screen, RED, (col*200+100, 0), (col*200+100, 600), 10)

def draw_status(text):
    pygame.draw.rect(screen, BLACK, (0, 600, WIDTH, 50))

    label = font.render(text, True, WHITE)
    screen.blit(label, (10, 610))

    score = font.render(f"Human: {human_score}  AI: {ai_score}", True, WHITE)
    screen.blit(score, (280, 610))

def draw_button():
    mouse_pos = pygame.mouse.get_pos()

    # Hover effect
    if button_rect.collidepoint(mouse_pos):
        color = HOVER
    else:
        color = GRAY

    pygame.draw.rect(screen, color, button_rect, border_radius=8)

    text = font.render("Restart Game", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

# ---------------- LOGIC ---------------- #
def check_win(b, player):
    for row in range(3):
        if all(b[row][col] == player for col in range(3)):
            return True
    for col in range(3):
        if all(b[row][col] == player for row in range(3)):
            return True
    if all(b[i][i] == player for i in range(3)):
        return True
    if all(b[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(b):
    return not np.any(b == 0)

# ---------------- MINIMAX ---------------- #
def minimax(b, is_max):
    if check_win(b, AI):
        return 1
    if check_win(b, HUMAN):
        return -1
    if is_full(b):
        return 0

    if is_max:
        best = -np.inf
        for i in range(3):
            for j in range(3):
                if b[i][j] == 0:
                    b[i][j] = AI
                    score = minimax(b, False)
                    b[i][j] = 0
                    best = max(score, best)
        return best
    else:
        best = np.inf
        for i in range(3):
            for j in range(3):
                if b[i][j] == 0:
                    b[i][j] = HUMAN
                    score = minimax(b, True)
                    b[i][j] = 0
                    best = min(score, best)
        return best

def best_move():
    global ai_thinking
    ai_thinking = True
    draw_status("AI Thinking...")
    pygame.display.update()

    time.sleep(0.4)

    best_score = -np.inf
    move = (0, 0)

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = AI
                score = minimax(board, False)
                board[i][j] = 0
                if score > best_score:
                    best_score = score
                    move = (i, j)

    board[move[0]][move[1]] = AI
    ai_thinking = False

def restart():
    global game_over, ai_thinking, human_score, ai_score
    board.fill(0)
    game_over = False
    ai_thinking = False

    # Reset scores (remove if you want to keep score)
    human_score = 0
    ai_score = 0

    draw_lines()

# ---------------- MAIN LOOP ---------------- #
draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Restart button FIRST
            if button_rect.collidepoint(event.pos):
                restart()
                continue

            if not game_over:
                x, y = event.pos

                if y < 600:
                    row = y // 200
                    col = x // 200

                    if board[row][col] == 0:
                        board[row][col] = HUMAN

                        if check_win(board, HUMAN):
                            game_over = True
                            draw_winning_line(HUMAN)
                            human_score += 1

                        elif is_full(board):
                            game_over = True

                        else:
                            best_move()

                            if check_win(board, AI):
                                game_over = True
                                draw_winning_line(AI)
                                ai_score += 1

                            elif is_full(board):
                                game_over = True

    draw_figures()
    draw_button()

    # -------- STATUS -------- #
    if ai_thinking:
        draw_status("AI Thinking...")
    elif game_over:
        if check_win(board, HUMAN):
            draw_status("Human Wins!")
        elif check_win(board, AI):
            draw_status("AI Wins!")
        else:
            draw_status("Draw!")
    else:
        draw_status("Your Turn")

    pygame.display.update()