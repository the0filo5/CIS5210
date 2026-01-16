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
    return math.comb(n ** 2, n)


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


def n_queens_valid_last(board):
    # assumes the board configuration is a list of numbers between
    # where the r-th number designates the column of the queen in row r
    # board[r] = c, check conflicts involving the last queen only
    r2 = len(board) - 1
    c2 = board[r2]
    for r1 in range(r2):
        c1 = board[r1]
        if c1 == c2:  # same column
            return False
        if abs(c2 - c1) == abs(r2 - r1):  # same diagonal
            return False
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
            if n_queens_valid_last(board):
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
        self.board[row][col] = not self.board[row][col]
        for row_off, col_off in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            ro = row + row_off
            co = col + col_off
            if ro >= 0 and ro < self.rows and co >= 0 and co < self.cols:
                self.board[ro][co] = not self.board[ro][co]

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
    return LightsOutPuzzle(np.zeros((rows, cols), dtype=bool).tolist())


############################################################
# Section 3: Linear Disk Movement
############################################################


class LinearDisks(object):

    def __init__(self, length, n, direct=False):
        if direct:
            self.board = np.arange(1, length + 1)
        else:
            self.board = np.ones(length, dtype=int)
        self.board[n:length] = 0
        self.length = length
        self.n = n
        self.direct = direct

    def get_board(self):
        return self.board

    def perform_move(self, pos1, pos2):
        if self.board[pos2] == 0:
            self.board[pos2] = self.board[pos1]
            self.board[pos1] = 0
        else:
            print(f"Error: Disk from {pos1} to non-zero position {pos2} !")
            print(self.board)

    def is_solved(self):
        for pos in range(self.length):
            if pos < self.length - self.n:
                if self.board[pos] != 0:
                    return False
            else:
                if self.direct:
                    if self.board[pos] != self.length - pos:
                        return False
                else:
                    if self.board[pos] != 1:
                        return False
        return True

    def copy(self):
        new_copy = LinearDisks(self.length, self.n, self.direct)
        new_copy.board = copy.deepcopy(self.board)
        return new_copy

    def successors(self):
        for pos in range(self.length):
            # if not last cell in board
            if pos < self.length - 1:
                # if pos has a disk and pos+1 no disk
                if self.board[pos] > 0 and self.board[pos + 1] == 0:
                    new_puzzle = self.copy()
                    new_puzzle.perform_move(pos, pos + 1)
                    yield (pos, pos + 1), new_puzzle
            # if not penultimate cell in board with disk in last position
            if pos < self.length - 2:
                if (self.board[pos] > 0 and self.board[pos + 1] > 0 and
                        self.board[pos + 2] == 0):
                    new_puzzle = self.copy()
                    new_puzzle.perform_move(pos, pos + 2)
                    yield (pos, pos + 2), new_puzzle
            if self.direct:
                # if second+ pos on the board
                if pos > 0:
                    # if pos has a disk and pos-1 no disk
                    if self.board[pos] > 0 and self.board[pos - 1] == 0:
                        new_puzzle = self.copy()
                        new_puzzle.perform_move(pos, pos - 1)
                        yield (pos, pos - 1), new_puzzle
                # if third+ position
                if pos > 1:
                    # if pos has a disk and pos-1 has a disk but pos-2 no disk
                    if (self.board[pos] > 0 and self.board[pos - 1] > 0 and
                            self.board[pos - 2] == 0):
                        new_puzzle = self.copy()
                        new_puzzle.perform_move(pos, pos - 2)
                        yield (pos, pos - 2), new_puzzle

    def find_solution(self):
        visited = set()
        frontier = deque()
        if self.is_solved():
            return []
        visited.add(tuple(self.get_board().ravel()))

        for move, puz in self.successors():
            key = tuple(puz.get_board().ravel())
            if key not in visited:
                visited.add(key)
                frontier.append(([move], puz))

        while frontier:
            moves, puz = frontier.popleft()
            if puz.is_solved():
                return moves

            for move_, puz_ in puz.successors():
                key = tuple(puz_.get_board().ravel())
                if key not in visited:
                    visited.add(key)
                    frontier.append((moves + [move_], puz_))
        return None


def solve_identical_disks(length, n):
    linear_disks = LinearDisks(length, n, direct=False)
    return linear_disks.find_solution()


def solve_distinct_disks(length, n):
    linear_disks = LinearDisks(length, n, direct=True)
    return linear_disks.find_solution()


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
It took me about 10 hours.
"""

feedback_question_2 = """
The most challenging aspect of the assignment was figuring out what
the row and cols where in the queen placement when recursion algorithm
was used.
"""

feedback_question_3 = """
I liked the lights out part.   I would not change anything
"""
