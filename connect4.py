from pygame.locals import *
import os
import numpy as np
import random
import pygame
import sys
import math
sky= (191, 193, 244)
white=(250, 250, 250)
black=(0, 0, 0)
gray=(75, 75, 75)
red=(200, 0, 0)
blue=(0, 0, 155)
yellow=(237, 241, 0)
rowCnt = 6
columnCnt = 7
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
windowLen = 4
screenSize = 100
screen_width=700
screen_height=700
global event
font = "Montserrat-Bold.ttf"
def alphaBeta(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = terminalNode(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if moveWin(board, AI_PIECE):
				return (None, 100000000000000)
			elif moveWin(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = alphaBeta(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = alphaBeta(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value
def create_board():
    board = np.zeros((rowCnt, columnCnt))
    return board
def drop_piece(board, row, col, piece):
    board[row][col] = piece
def is_valid_location(board, col):
    return board[rowCnt - 1][col] == 0
def get_next_open_row(board, col):
    for r in range(rowCnt):
        if board[r][col] == 0:
            return r
def printBoard(board):
    print(np.flip(board, 0))
def moveWin(board, piece):
    # Check horizontal locations for win
    for c in range(columnCnt - 3):
        for r in range(rowCnt):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(columnCnt):
        for r in range(rowCnt - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(columnCnt - 3):
        for r in range(rowCnt - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(columnCnt - 3):
        for r in range(3, rowCnt):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score
def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, columnCnt // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(rowCnt):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(columnCnt - 3):
            window = row_array[c:c + windowLen]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(columnCnt):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rowCnt - 3):
            window = col_array[r:r + windowLen]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(rowCnt - 3):
        for c in range(columnCnt - 3):
            window = [board[r + i][c + i] for i in range(windowLen)]
            score += evaluate_window(window, piece)

    for r in range(rowCnt - 3):
        for c in range(columnCnt - 3):
            window = [board[r + 3 - i][c + i] for i in range(windowLen)]
            score += evaluate_window(window, piece)

    return score
def terminalNode(board):
    return moveWin(board, PLAYER_PIECE) or moveWin(board, AI_PIECE) or len(get_valid_locations(board)) == 0
def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = terminalNode(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if moveWin(board, AI_PIECE):
                return (None, 100000000000000)
            elif moveWin(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value
def get_valid_locations(board):
    valid_locations = []
    for col in range(columnCnt):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations
def draw_board(board):
    for c in range(columnCnt):
        for r in range(rowCnt):
            pygame.draw.rect(screen, yellow, (c * screenSize, r * screenSize + screenSize, screenSize, screenSize))
            pygame.draw.circle(screen, white, (
            int(c * screenSize + screenSize / 2), int(r * screenSize + screenSize + screenSize / 2)), RADIUS)

    for c in range(columnCnt):
        for r in range(rowCnt):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, red, (
                int(c * screenSize + screenSize / 2), height - int(r * screenSize + screenSize / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, blue, (
                int(c * screenSize + screenSize / 2), height - int(r * screenSize + screenSize / 2)), RADIUS)
    pygame.display.update()
board = create_board()
printBoard(board)
pygame.init()
width = columnCnt * screenSize
height = (rowCnt + 1) * screenSize
size = (width, height)
RADIUS = int(screenSize / 2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("connect 4", 75)


def choosemini(depth):
    game_over = False
    turn = AI //1
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            pygame.display.update()
        if turn == PLAYER: #0
            col, minimax_score = minimax(board, depth, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                if moveWin(board, PLAYER_PIECE):
                    label = myfont.render("computer wins", True, red)
                    screen.blit(label, (40, 10))
                    game_over = True
                turn = AI
                printBoard(board)
                draw_board(board)
        if turn == AI and not game_over:
            col, minimax_score = minimax(board, depth, True)
            if is_valid_location(board, col):
                # pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                if moveWin(board, AI_PIECE):
                    label = myfont.render(" Agent Wins!!", True, blue)
                    screen.blit(label, (40, 10))
                    game_over = True
                printBoard(board)
                draw_board(board)
                turn = PLAYER
        if game_over:
            pygame.time.wait(6000)
def choosealpha(depth):
    game_over = False
    turn = AI
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            pygame.display.update()
        if turn == PLAYER:
            col, alphaBeta_score = alphaBeta(board, depth, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                if moveWin(board, PLAYER_PIECE):
                    label = myfont.render("Player wins!!", True, red)
                    screen.blit(label, (40, 10))
                    game_over = True
                turn = AI
                printBoard(board)
                draw_board(board)
        if turn == AI and not game_over:
            col, alphaBeta_score = alphaBeta(board, depth, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                if moveWin(board, AI_PIECE):
                    label = myfont.render("Agent Wins", True, blue)
                    screen.blit(label, (40, 10))
                    game_over = True
                printBoard(board)
                draw_board(board)
                turn = PLAYER
        if game_over:
            pygame.time.wait(6000)

os.environ['SDL_VIDEO_CENTERED'] = '1'

clock = pygame.time.Clock()

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, False, textColor)
    return newText

setAlgorithm = "MINIMAX"
def connect4(setAlgorithm):
    pygame.init()

    class Option:
        hovered = False
        def __init__(self, text, pos):
            self.text = text
            self.pos = pos
            self.set_rect()
            self.draw()

        def draw(self):
            self.set_rend()
            screen.blit(self.rend, self.rect)
        def set_rend(self):
            self.rend = menu_font.render(self.text, True, self.get_color())
        def get_color(self):
            if self.hovered:
                return red
            else:
                return blue
        def set_rect(self):
            self.set_rend()
            self.rect = self.rend.get_rect()
            self.rect.topleft = self.pos

    menu_font = pygame.font.Font(font, 40)
    text_settingmin=text_format("MINIMAX", font, 75, white)
    text_settingalpha = text_format("ALPHA-BETA", font, 75, white)
    text_quit=text_format("Exit", font, 75, white)

    setting_rectmin=text_settingmin.get_rect()
    setting_rectalpha = text_settingalpha.get_rect()
    quit_rect=text_quit.get_rect()

    text_setting1 = text_format("easy", font, 75, white)
    text_setting2 = text_format("medium", font, 75, white)
    text_setting3 = text_format("hard", font, 75, white)

    setting_rect1 = text_setting1.get_rect()
    setting_rect2 = text_setting2.get_rect()
    setting_rect3 = text_setting3.get_rect()

    options = [
        Option("MINIMAX", (screen_width/4 - (setting_rectmin[2]/4), 330)),
        Option("ALPHA-BETA", (screen_width / 4 - (setting_rectalpha[2] / 4), 400)),
        Option("Exit", (screen_width/4 - (quit_rect[2]/4), 470)),
        Option("easy", (3 * screen_width / 4 - (setting_rect1[2] / 4), 330)),
        Option("medium", (3 * screen_width / 4 - (setting_rect2[2] / 4), 400)),
        Option("hard", (3 * screen_width / 4 - (setting_rect3[2] / 4), 470))
    ]

    pygame.display.update()
    pygame.display.set_caption("Connect 4")

    while True:
        pygame.event.pump()
        screen.fill(white)
        for option in options :
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and option.text == "ALPHA-BETA":
                         setAlgorithm = "ALPHA BETA"
                         print(setAlgorithm)

                    if event.type == pygame.MOUSEBUTTONDOWN and option.text == "MINIMAX":
                        setAlgorithm = "MINIMAX"
                        print(setAlgorithm)

                    if event.type == pygame.MOUSEBUTTONDOWN and option.text == "easy" and setAlgorithm =="ALPHA BETA":
                        choosealpha(2)
                        # print(option.text)
                        connect4(setAlgorithm)
                    elif event.type == pygame.MOUSEBUTTONDOWN and option.text == "easy" and setAlgorithm =="MINIMAX":
                        choosemini(2)
                        connect4(setAlgorithm)
                    if event.type == pygame.MOUSEBUTTONDOWN and option.text == "medium" and setAlgorithm =="ALPHA BETA":
                        choosealpha(4)
                        connect4(setAlgorithm)
                    elif event.type == pygame.MOUSEBUTTONDOWN and option.text == "medium" and setAlgorithm == "MINIMAX":
                        choosemini(4)
                        connect4(setAlgorithm)
                    if event.type == pygame.MOUSEBUTTONDOWN and option.text == "hard" and setAlgorithm =="ALPHA BETA":
                        choosealpha(6)
                        connect4(setAlgorithm)
                    elif event.type == pygame.MOUSEBUTTONDOWN and option.text == "hard" and setAlgorithm == "MINIMAX":
                        choosemini(6)
                        connect4(setAlgorithm)
                    if event.type == pygame.MOUSEBUTTONDOWN and option.text == "Exit":
                        pygame.quit()
                        quit()


            else:
                option.hovered = False
            option.draw()

        title=text_format("CONNECT 4 AI vs AI ", font, 65, black)
        title_rect=title.get_rect()
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        pygame.display.update()


connect4(setAlgorithm)
pygame.quit()
QUIT()