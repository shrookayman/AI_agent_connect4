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
red=(200, 0, 0)
blue=(0, 0, 155)
yellow=(237, 241, 0)
rowCnt = 6
columnCnt = 7
computer = 0
AI = 1
EMPTY = 0
computer_PIECE = 1
AI_PIECE = 2
windowLen = 4
screenSize = 100
screenWidth=750


font = "Montserrat-Bold.ttf"
def minimax(board, depth, maximizingPlayer):
    valid_locations = getValidLocation(board)
    # is_terminal = terminalNode(board)
    if depth == 0 or terminalNode(board):
        if terminalNode(board):
            if moveWin(board, AI_PIECE):
                return (None, 100000000000000)
            elif moveWin(board, computer_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, scorePosition(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = nextRow(board, col)
            b_copy = board.copy()
            dropChecker(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = nextRow(board, col)
            b_copy = board.copy()
            dropChecker(b_copy, row, col, computer_PIECE)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value
def alphaBeta(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = getValidLocation(board)
	if depth == 0 or terminalNode(board):
		if terminalNode(board):
			if moveWin(board, AI_PIECE):
				return (None, 100000000000000)
			elif moveWin(board, computer_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else:
			return (None, scorePosition(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = nextRow(board, col)
			b_copy = board.copy()
			dropChecker(b_copy, row, col, AI_PIECE)
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
			row = nextRow(board, col)
			b_copy = board.copy()
			dropChecker(b_copy, row, col, computer_PIECE)
			new_score = alphaBeta(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value
def createBoard():
    board = np.zeros((rowCnt, columnCnt))
    return board
def dropChecker(board, row, col, piece):
    board[row][col] = piece
def locationValid(board, col):
    return board[rowCnt - 1][col] == 0
def nextRow(board, col):
    for r in range(rowCnt):
        if board[r][col] == 0:
            return r
def evaluateWindow(window, piece):
    score = 0
    opp_piece = computer_PIECE
    if piece == computer_PIECE:
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
def scorePosition(board, piece):
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
            score += evaluateWindow(window, piece)

    ## Score Vertical
    for c in range(columnCnt):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rowCnt - 3):
            window = col_array[r:r + windowLen]
            score += evaluateWindow(window, piece)

    ## Score posiive sloped diagonal
    for r in range(rowCnt - 3):
        for c in range(columnCnt - 3):
            window = [board[r + i][c + i] for i in range(windowLen)]
            score += evaluateWindow(window, piece)

    for r in range(rowCnt - 3):
        for c in range(columnCnt - 3):
            window = [board[r + 3 - i][c + i] for i in range(windowLen)]
            score += evaluateWindow(window, piece)

    return score
def terminalNode(board):
    return moveWin(board, computer_PIECE) or moveWin(board, AI_PIECE) or len(getValidLocation(board)) == 0
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

    # Check positively sloped diagonals
    for c in range(columnCnt - 3):
        for r in range(rowCnt - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(columnCnt - 3):
        for r in range(3, rowCnt):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True
def getValidLocation(board):
    valid_locations = []
    for col in range(columnCnt):
        if locationValid(board, col):
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
            if board[r][c] == computer_PIECE:
                pygame.draw.circle(screen, red, (
                int(c * screenSize + screenSize / 2), height - int(r * screenSize + screenSize / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, blue, (
                int(c * screenSize + screenSize / 2), height - int(r * screenSize + screenSize / 2)), RADIUS)
    pygame.display.update()

def chooseMinimax(depth):
        global event
        game_over = False
        turn = AI  # 1
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                pygame.display.update()
            if turn == computer:  # 0
                col, minimax_score = minimax(board, depth, True)
                if locationValid(board, col):
                    row = nextRow(board, col)
                    dropChecker(board, row, col, computer_PIECE)
                    if moveWin(board, computer_PIECE):
                        label = myFont.render("computer wins", True, red)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn = AI
                    printBoard(board)
                    draw_board(board)
            if turn == AI and not game_over:
                col, minimax_score = minimax(board, depth, True)
                if locationValid(board, col):
                    # pygame.time.wait(500)
                    row = nextRow(board, col)
                    dropChecker(board, row, col, AI_PIECE)
                    if moveWin(board, AI_PIECE):
                        label = myFont.render(" Agent Wins!!", True, blue)
                        screen.blit(label, (40, 10))
                        game_over = True
                    printBoard(board)
                    draw_board(board)
                    turn = computer
            if game_over:
                pygame.time.wait(6000)
def chooseAlphabeta(depth):
        game_over = False
        turn = AI
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                pygame.display.update()
            if turn == computer:
                col, alphaBeta_score = alphaBeta(board, depth, -math.inf, math.inf, True)
                if locationValid(board, col):
                    row = nextRow(board, col)
                    dropChecker(board, row, col, computer_PIECE)
                    if moveWin(board, computer_PIECE):
                        label = myFont.render("computer wins!!", True, red)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn = AI
                    printBoard(board)
                    draw_board(board)
            if turn == AI and not game_over:
                col, alphaBeta_score = alphaBeta(board, depth, -math.inf, math.inf, True)
                if locationValid(board, col):
                    row = nextRow(board, col)
                    dropChecker(board, row, col, AI_PIECE)
                    if moveWin(board, AI_PIECE):
                        label = myFont.render("Agent Wins", True, blue)
                        screen.blit(label, (40, 10))
                        game_over = True
                    printBoard(board)
                    draw_board(board)
                    turn = computer
            if game_over:
                pygame.time.wait(6000)


board = createBoard()
printBoard(board)
pygame.init()
width = columnCnt * screenSize
height = (rowCnt + 1) * screenSize
size = (width, height)
RADIUS = int(screenSize / 2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myFont = pygame.font.SysFont("connect 4", 75)
# os.environ['SDL_VIDEO_CENTERED']= '1'

clock = pygame.time.Clock()

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, False, textColor)
    return newText

setAlgorithm = "MINIMAX"
def connect4(setAlgorithm):
    pygame.init()

    class Option:
        hovered = True
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
    minimaxi=text_format("MINIMAX", font, 75, white)
    alphabetaa = text_format("ALPHA-BETA", font, 75, white)
    text_quit=text_format("Exit", font, 75, white)

    minRect=minimaxi.get_rect()
    alphabetaRect = alphabetaa.get_rect()
    exitRect=text_quit.get_rect()

    level1 = text_format("Easy", font, 75, white)
    level2 = text_format("Medium", font, 75, white)
    level3 = text_format("Hard", font, 75, white)

    level1Rect = level1.get_rect()
    level2Rect = level2.get_rect()
    level3Rect = level3.get_rect()

    options = [
        Option("MINIMAX", (screenWidth/4 - (minRect[2]/4), 330)),
        Option("ALPHA-BETA", (screenWidth / 4 - (alphabetaRect[2] / 4), 400)),
        Option("Exit", (screenWidth/4 - (exitRect[2]/4), 470)),
        Option("Easy", (3 * screenWidth / 4 - (level1Rect[2] / 4), 330)),
        Option("Medium", (3 * screenWidth / 4 - (level2Rect[2] / 4), 400)),
        Option("Hard", (3 * screenWidth / 4 - (level3Rect[2] / 4), 470))
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

                    if event.type == pygame.MOUSEBUTTONDOWN and option.text == "Easy" and setAlgorithm =="ALPHA BETA":
                        chooseAlphabeta(2)
                        # print(option.text)
                        connect4(setAlgorithm)
                    elif event.type == pygame.MOUSEBUTTONDOWN and option.text == "Easy" and setAlgorithm =="MINIMAX":
                        chooseMinimax(2)
                        connect4(setAlgorithm)
                    if event.type == pygame.MOUSEBUTTONDOWN and option.text == "Medium" and setAlgorithm =="ALPHA BETA":
                        chooseAlphabeta(4)
                        connect4(setAlgorithm)
                    elif event.type == pygame.MOUSEBUTTONDOWN and option.text == "Medium" and setAlgorithm == "MINIMAX":
                        chooseMinimax(4)
                        connect4(setAlgorithm)
                    if event.type == pygame.MOUSEBUTTONDOWN and option.text == "Hard" and setAlgorithm =="ALPHA BETA":
                        chooseAlphabeta(6)
                        connect4(setAlgorithm)
                    elif event.type == pygame.MOUSEBUTTONDOWN and option.text == "Hard" and setAlgorithm == "MINIMAX":
                        chooseMinimax(6)
                        connect4(setAlgorithm)
                    if event.type == pygame.MOUSEBUTTONDOWN and option.text == "Exit":
                        pygame.quit()
                        quit()


            else:
                option.hovered = False
            option.draw()

        title=text_format("CONNECT 4 AI vs AI ", font, 65, black)
        title_rect=title.get_rect()
        screen.blit(title, (screenWidth/2 - (title_rect[2]/2), 80))
        pygame.display.update()


connect4(setAlgorithm)
pygame.quit()
QUIT()