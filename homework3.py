############################################################
# CIS 521: Homework 3
############################################################
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
                yield from puz.iddfs_helper(limit-1, moves)
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
        sum = 0
        puzzle = np.array(self.board)
        # exclude 0 tile from manhattan distance calculation
        for i in range(1, self.rows*self.cols):
            x, y = np.where(puzzle == i)
            x, y = int(x[0]), int(y[0])
            sum += (abs(x - self.sol_coords[i][0])
                    + abs(y - self.sol_coords[i][1]))
        return sum

    # Required
    def find_solution_a_star(self):
        visited = set()
        frontier = PriorityQueue()
        if self.is_solved():
            return []
        visited.add(tuple(np.array(self.get_board()).ravel()))

        for rc, puz in self.successors():
            key = tuple(np.array(puz.get_board()).ravel())
            if key not in visited:
                visited.add(key)
                frontier.put((puz.distance() + 1, [rc], puz))

        while not frontier.empty():
            _, moves, puz = frontier.get()
            if puz.is_solved():
                return moves

            for rc_, puz_ in puz.successors():
                key = tuple(np.array(puz_.get_board()).ravel())
                if key not in visited:
                    visited.add(key)
                    frontier.put((puz_.distance() + len(moves), moves
                                  + [rc_], puz_))
        return None


b = [[1,2,3], [4,0,5], [6,7,8]]
p = TilePuzzle(b)
solutions = p.find_solutions_iddfs()
print(list(solutions))


b = [[1,2,3], [4,0,5], [6,7,8]]
p = TilePuzzle(b)
solution = p.find_solution_a_star()
print(solution)

############################################################
# Section 2: Grid Navigation
############################################################


def find_path(start, goal, scene):
    pass


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################


def solve_distinct_disks(length, n):
    pass


############################################################
# Section 4: Feedback
############################################################


# Just an approximation is fine.
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
