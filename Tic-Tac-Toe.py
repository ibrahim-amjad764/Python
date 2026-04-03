# pygame → pip install pygame
# numpy → pip install numpy
# python --version
# pip --version
import sys
import pygame
import numpy as np

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Sizes
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK)

# BOARD
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Players
HUMAN = 1  # X
AI = 2     # O

# 🔹 Draw grid
def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, WHITE, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, WHITE, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

# 🔹 Draw X and O
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == HUMAN:
                pygame.draw.circle(screen, WHITE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == AI:
                pygame.draw.line(screen, WHITE,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, WHITE,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 CROSS_WIDTH)

# 🔹 Highlight winning line
def draw_winning_line(player):
    # Check rows
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            pygame.draw.line(screen, RED,
                             (15, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                             (WIDTH - 15, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                             15)
            return
    # Check columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            pygame.draw.line(screen, RED,
                             (col * SQUARE_SIZE + SQUARE_SIZE // 2, 15),
                             (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 15),
                             15)
            return
    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        pygame.draw.line(screen, RED,
                         (15, 15),
                         (WIDTH - 15, HEIGHT - 15),
                         15)
        return
    if all(board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)):
        pygame.draw.line(screen, RED,
                         (WIDTH - 15, 15),
                         (15, HEIGHT - 15),
                         15)
        return

# 🔹 Mark square
def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    return not np.any(board == 0)

def check_win(player):
    # Return True if player wins
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return True
    if all(board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)):
        return True
    return False

# 🔹 Minimax AI
def minimax(minimax_board, depth, is_maximizing):
    if check_win(AI):
        return 1
    elif check_win(HUMAN):
        return -1
    elif not np.any(minimax_board == 0):
        return 0

    if is_maximizing:
        best_score = -np.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = AI
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = np.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = HUMAN
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

# 🔹 AI best move
def best_move():
    best_score = -np.inf
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = AI
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], AI)

# 🔹 Restart game
def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

draw_lines()
player_turn = HUMAN
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            row = mouseY // SQUARE_SIZE
            col = mouseX // SQUARE_SIZE
            if available_square(row, col):
                mark_square(row, col, HUMAN)

                if check_win(HUMAN):
                    print(" Human wins!")
                    draw_winning_line(HUMAN)
                    game_over = True
                elif is_board_full():
                    print(" Draw!")
                    game_over = True
                else:
                    best_move()
                    if check_win(AI):
                        print(" AI wins!")
                        draw_winning_line(AI)
                        game_over = True
                    elif is_board_full():
                        print(" Draw!")
                        game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                player_turn = HUMAN
                game_over = False

    draw_figures()
    pygame.display.update()