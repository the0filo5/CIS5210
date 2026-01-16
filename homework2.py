############################################################
# CIS 521: Homework 2
############################################################
import math
from collections import deque

import numpy as np
import random
import copy

student_name = "Theophilos Constantinidis"


############################################################
# Imports
############################################################

# Include your imports here, if any are used.


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    # out of n^2 board positions pick n and place indistinguishable queens
    return math.comb(n ** n, n)


def num_placements_one_per_row(n):
    # for each of n rows place one queen to any of n columns
    return n ** n


def n_queens_valid(board):
    # assumes the board configuration is a list of numbers between
    # where the r-th number designates the column of the queen in row r
    n = max(len(board), max(board) + 1)

    conflicts = np.zeros((n, n))
    # for each row r
    for r in range(n):
        if r >= len(board):
            break
        # if (r,board[r]) board position already in conflicts
        if conflicts[r][board[r]] > 0:
            return False
        conflicts[r, :] = 1  # conflict all columns in row r
        conflicts[:, board[r]] = 1  # conflict all rows of column board[r]

        rows = np.arange(n)
        c1 = rows - (r - board[r])  # "\" cols
        m1 = (c1 >= 0) & (c1 < n)  # mask out the negatives
        conflicts[rows[m1], c1[m1]] = 1

        c2 = (r + board[r]) - rows  # "/" cols
        m2 = (c2 >= 0) & (c2 < n)  # mask out the negatives
        conflicts[rows[m2], c2[m2]] = 1

    return True


def n_queens_helper(n, board):
    # when all rows are full we have a valid solution
    # after recursive function has taken n step one for each row
    if len(board) == n:
        yield board.copy()
        return

    # place queen in next row
    for c in range(n):
        # place queen in column c in of row = len(board)
        if c not in board:
            board.append(c)
            if n_queens_valid(board):
                yield from n_queens_helper(n, board)
            board.pop()


def n_queens_solutions(n):
    return list(n_queens_helper(n, []))


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows, self.cols = np.array(board).shape

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = ~self.board[row][col]
        for row_off, col_off in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
            ro = row + row_off
            co = col + col_off
            if ro >= 0 and ro < self.rows and co >= 0 and co < self.cols:
                self.board[ro][co] = ~self.board[ro][co]

    def scramble(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if random.random() < 0.5:
                    self.perform_move(r, c)

    def is_solved(self):
        return np.array(self.board).sum() == 0

    def copy(self):
        return LightsOutPuzzle(copy.deepcopy(self.board))

    def successors(self):
        for r in range(self.rows):
            for c in range(self.cols):
                new_puzzle = self.copy()
                new_puzzle.perform_move(r, c)
                yield (r, c), new_puzzle

    def find_solution(self):
        visited = set()
        frontier = deque()
        if self.is_solved():
            return []
        visited.add(tuple(np.array(self.get_board()).ravel()))

        for rc, puz in self.successors():
            key = tuple(np.array(puz.get_board()).ravel())
            if key not in visited:
                visited.add(key)
                frontier.append(([rc], puz))

        while frontier:
            moves, puz = frontier.popleft()
            if puz.is_solved():
                return moves

            for rc_, puz_ in puz.successors():
                key = tuple(np.array(puz_.get_board()).ravel())
                if key not in visited:
                    visited.add(key)
                    frontier.append((moves + [rc_], puz_))
        return None

def create_puzzle(rows, cols):
    return LightsOutPuzzle(np.zeros((rows, cols), dtype=bool))



############################################################
# Section 3: Linear Disk Movement
############################################################

def solve_identical_disks(length, n):
    pass


def solve_distinct_disks(length, n):
    pass


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
