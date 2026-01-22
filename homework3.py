############################################################
# CIS 521: Homework 3
############################################################
import math
from collections import deque
from copy import deepcopy
from queue import PriorityQueue

############################################################
# Imports
############################################################

import numpy as np
import random
import copy

############################################################

student_name = "Theophilos Constantinidis"


############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    solution_range = np.arange(1, rows * cols + 1)
    solution_range[-1] = 0
    board = solution_range.reshape(rows, cols).tolist()
    return TilePuzzle(board)


class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rows, self.cols = np.array(board).shape
        solution_range = list(range(1, self.rows * self.cols + 1))
        solution_range[-1] = 0
        self.solution = solution_range
        # find the 0 coordinates
        coords = np.where(np.array(self.board) == 0)
        self.x, self.y = int(coords[0][0]), int(coords[1][0])
        # ccordinates in solution of all tiles in order 0..(n-1)
        self.sol_coords = [(x, y) for x in range(self.rows)
                           for y in range(self.cols)]

    def get_board(self):
        return self.board

    def is_move_valid(self, direction):
        move_offset = {'up': (-1, 0),
                       'down': (1, 0),
                       'left': (0, -1),
                       'right': (0, 1)}
        # get move offset
        x_offset, y_offset = move_offset[direction]
        # calculate the coordinates of tile to be moved
        x_m, y_m = self.x + x_offset, self.y + y_offset
        # if coordinates tile off the board dimensions return False
        if x_m < 0 or y_m < 0 or x_m >= self.rows or y_m >= self.cols:
            return False, self.x, self.y
        return True, x_m, y_m

    def perform_move(self, direction):
        valid_move, x_m, y_m = self.is_move_valid(direction)
        if valid_move:
            # Move the tile to zero coordinates
            self.board[self.x][self.y] = self.board[x_m][y_m]
            # zero out the previous tile coordinates
            self.board[x_m][y_m] = 0
            # update the zero coordinates
            self.x, self.y = x_m, y_m
            return True
        return False

    def scramble(self, num_moves):
        for r in range(num_moves):
            move = random.choice(['up', 'down', 'left', 'right'])
            self.perform_move(move)

    def is_solved(self):
        return sum(~(np.array(self.board).ravel() == self.solution)) == 0

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        for move in ['up', 'down', 'left', 'right']:
            valid_move, x_m, y_m = self.is_move_valid(move)
            if valid_move:
                new_puzzle = self.copy()
                new_puzzle.perform_move(move)
                yield move, new_puzzle

    # Helper function for recursion
    def iddfs_helper(self, limit, moves):
        if self.is_solved():
            yield list(moves)
            return

        if limit > 0:
            # calculate next level of next moves
            for move, puz in self.successors():
                moves.append(move)
                yield from puz.iddfs_helper(limit - 1, moves)
                moves.pop()

        return

    # Required
    def find_solutions_iddfs2(self):
        max_depth = 1000000
        for depth in range(max_depth + 1):
            # if no solutions then generator will return empty
            solutions = self.iddfs_helper(depth, [])
            if solutions and len(list(solutions)) > 0:
                yield solutions
        return

    def find_solutions_iddfs(self):
        max_depth = 10000000
        for depth in range(max_depth + 1):
            found = False
            for sol in self.iddfs_helper(depth, []):
                found = True
                yield sol
            if found:
                return

    # Manhattan Distance
    def distance(self):
        total = 0
        puzzle = np.array(self.board)
        # exclude 0 tile from manhattan distance calculation
        for i in range(1, self.rows * self.cols):
            x, y = np.where(puzzle == i)
            x, y = int(x[0]), int(y[0])
            total += (abs(x - self.sol_coords[i][0])
                      + abs(y - self.sol_coords[i][1]))
        return total

    # Required
    def find_solution_a_star(self):
        visited = set()
        frontier = PriorityQueue()
        g_score = dict()
        if self.is_solved():
            return []
        key = tuple(np.array(self.get_board()).ravel())
        visited.add(key)
        g_score[key] = 0

        for rc, puz in self.successors():
            key = tuple(np.array(puz.get_board()).ravel())
            if key not in visited or g_score[key] > 1:
                visited.add(key)
                g_score[key] = 1
                frontier.put((puz.distance() + g_score[key], [rc], puz))

        while not frontier.empty():
            _, moves, puz = frontier.get()
            if puz.is_solved():
                return moves

            for rc_, puz_ in puz.successors():
                key = tuple(np.array(puz_.get_board()).ravel())
                if key not in visited or g_score[key] > len(moves) + 1:
                    visited.add(key)
                    g_score[key] = len(moves) + 1
                    frontier.put((puz_.distance() + g_score[key], moves
                                  + [rc_], puz_))
        return None


b = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
p = TilePuzzle(b)
print(p.find_solution_a_star())


############################################################
# Section 2: Grid Navigation
############################################################


def find_path(start, goal, scene):
    pass


############################################################
# Section 3: Linear Disk Movement, Revisited
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
        # ccordinates in solution of all tiles in order 0..(n-1)
        self.sol_coords = [self.length - x for x in range(0, self.length)]

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

    # Manhattan Distance
    def distance(self):
        """
        Manhattan distance works for grid puzzles because each move changes
        distance by 1. In Linear Disk Movement, a single move can advance a
        disk by 2 (a hop), so summing absolute index differences for all
        disks can overshoot the true remaining number of moves.
        So we need to redesign h(n) via a relaxed version of the disk problem.
        Ignore blocking and assume each disk can always move toward its goal #
        by up to 2 cells per move. For each disk, compute how far it still
        needs to travel to its target index and convert that to a minimal
        number of moves under this relaxation (think “distance divided by 2,
        rounded up”). Sum over all disks.
        """
        total = 0
        # exclude 0 tile from manhattan distance calculation
        for i in range(self.n, 0, -1):
            x = np.where(self.board == i)
            x = int(x[0][0])
            total += math.ceil(abs(x - self.sol_coords[i]) / 2.0)
        return total

    def find_solution(self):
        visited = set()
        frontier = PriorityQueue()
        g_score = dict()
        if self.is_solved():
            return []
        key = tuple(self.get_board().ravel())
        visited.add(key)
        g_score[key] = 0

        for move, puz in self.successors():
            key = tuple(puz.get_board().ravel())
            if key not in visited or g_score[key] > 1:
                visited.add(key)
                g_score[key] = 1
                frontier.put((puz.distance() + g_score[key], [move], puz))

        while not frontier.empty():
            _, moves, puz = frontier.get()
            if puz.is_solved():
                return moves

            for move_, puz_ in puz.successors():
                key = tuple(puz_.get_board().ravel())
                if key not in visited or g_score[key] > len(moves) + 1:
                    visited.add(key)
                    g_score[key] = len(moves) + 1
                    frontier.put((puz_.distance() + g_score[key], moves
                                  + [move_], puz_))


def solve_distinct_disks(length, n):
    linear_disks = LinearDisks(length, n, direct=True)
    return linear_disks.find_solution()

############################################################
# Section 4: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
It took me about 10 hours.
"""

feedback_question_2 = """
The most challenging aspect of the assignment was figuring out how to create
the generator in the find_solutions_iddfs function.
"""

feedback_question_3 = """
I liked the find_solution_a_star implementation challenge.   
I would not change anything
"""
