############################################################
# CIS 521: Homework 4
############################################################

############################################################
# Imports
############################################################
import collections
import itertools
import queue
import random

# Include your imports here, if any are used.
import collections
import copy
import itertools
import random
import math
import numpy as np

############################################################

student_name = "Theophilos Constantinidis"


############################################################
# Section 1: Dominoes Game
############################################################


def create_dominoes_game(rows, cols):
    empty_dominoes = np.zeros((rows, cols), dtype=bool).tolist()
    return DominoesGame(empty_dominoes)


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rows, self.cols = np.array(board).shape
        # ccordinates in solution of all tiles in order 0..(n-1)
        self.coords = [(x, y) for x in range(self.rows)
                       for y in range(self.cols)]

    def get_board(self):
        return self.board

    def reset(self):
        self.board = np.zeros((self.rows, self.cols),
                              dtype=bool).tolist()

    def is_legal_move(self, row, col, vertical):
        # If the vertical parameter is True, then the current player
        # intends to place a domino on squares (row, col) and (row + 1, col).
        # If the vertical parameter is False, then the current player intends
        # to place a domino on squares (row, col) and (row, col + 1).
        if vertical and row + 1 < self.rows:
            return not self.board[row][col] and not self.board[row + 1][col]
        if not vertical and col + 1 < self.cols:
            return not self.board[row][col] and not self.board[row][col + 1]
        return False

    def legal_moves(self, vertical):
        legal_moves_ = []
        for r, c in self.coords:
            if self.is_legal_move(r, c, vertical):
                legal_moves_.append((r, c))
        return legal_moves_

    def perform_move(self, row, col, vertical):
        if vertical:
            self.board[row][col] = True
            self.board[row + 1][col] = True
        else:
            self.board[row][col] = True
            self.board[row][col + 1] = True

    def game_over(self, vertical):
        for r, c in self.coords:
            if self.is_legal_move(r, c, vertical):
                return False
        return True

    def copy(self):
        return DominoesGame(copy.deepcopy(self.board))

    def successors(self, vertical):
        for legal_move in self.legal_moves(vertical):
            new_game = self.copy()
            new_game.perform_move(legal_move[0], legal_move[1], vertical)
            yield legal_move, new_game

    def get_random_move(self, vertical):
        return random.choice(self.legal_moves(vertical))

    def evaluate(self, vrt):
        return (len(self.legal_moves(vrt)) -
                len(self.legal_moves(not vrt)))

    def evaluate(self, vrt):
        return (len(self.legal_moves(vrt)) -
                len(self.legal_moves(not vrt)))



    def get_best_move(self, vertical, limit):

        # Start with the current position as a MAX node.
        # Apply the evaluation function to the leaf positions.
        if limit == 0:
            return None, self.evaluate(vertical), 1

        # Expand the game tree a fixed number of ply (limit) using recursion
        max_util = -math.inf
        max_move = None
        sum_leaves = 0
        if limit > 0:
            for move, game in self.successors(vertical):
                move_coords, util_score, num_leaves = game.get_best_move(
                    not vertical, limit - 1)
                if -util_score > max_util:
                    max_util = -util_score
                    max_move = move
                sum_leaves += num_leaves
                print(limit, limit*"  ", "move: ", move, "by ", vertical, "score: ", util_score, "max_score: ",
                      max_util, "max_move: ", max_move, "sum_leaves: ", sum_leaves)

        return max_move, max_util, sum_leaves


b = [[False] * 3 for i in range(3)]
g = DominoesGame(b)
print(g.get_best_move(True, 1))
# ((0, 1), 2, 6)
print(g.get_best_move(True, 4))
# ((0, 1), 3, 10)

############################################################
# Section 2: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
2 hours
"""

feedback_question_2 = """
This assignment was straight forward with no particular challenges
"""

feedback_question_3 = """
I liked the alpha beta algorithm.  Would not change anything.
"""
