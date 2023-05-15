
import numpy as np


rowCnt = 6
columnCnt = 7

computer = 0
AI = 1

def createBoard():
    board = np.zeros((rowCnt, columnCnt))
    return board

def dropCheckers(board, row, column, checker):
    board[row][column] = checker
