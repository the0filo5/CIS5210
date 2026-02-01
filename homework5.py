############################################################
# CIS 521: Homework 5
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import collections
import copy
import itertools
import random
import math
from queue import PriorityQueue

import numpy as np

############################################################

student_name = "Theophilos Constantinidis"


############################################################
# Sudoku Solver
############################################################


def sudoku_cells():
    return [(x, y) for x in range(9) for y in range(9)]


def block_coords(cell):
    return cell[0] // 3, cell[1] // 3


def block_dict():
    block = {(br, bc): [] for br in range(3) for bc in range(3)}
    for cell in sudoku_cells():
        block[block_coords(cell)].append(cell)
    return block


def sudoku_arcs():
    arc_list = []
    boxes = block_dict()
    # for each row
    for i, j in sudoku_cells():
        for k in range(9):
            # for cell (i,j) row put in arcs all cells in same row
            if (i, j) != (i, k):
                arc_list.append(((i, j), (i, k)))
            # for cell (i, j) column put in arcs all cells in same column
            if (i, j) != (k, j):
                arc_list.append(((i, j), (k, j)))
        # add all cells in the same 3x3 box
        for cell in boxes[block_coords((i, j))]:
            if (i, j) != cell:
                arc = ((i, j), cell)
                if arc not in arc_list:
                    arc_list.append(arc)
    return arc_list


# creates a dictionary of all tails that can affect head by row, col, block
def sudoku_arcs_dict(cells, arcs):
    arcs_dict_row = {cell: [] for cell in cells}
    arcs_dict_col = {cell: [] for cell in cells}
    arcs_dict_block = {cell: [] for cell in cells}
    cell_block = {cell: block_coords(cell) for cell in cells}
    for h, t in arcs:
        if h[0] == t[0]:
            arcs_dict_row[h].append(t)
        if h[1] == t[1]:
            arcs_dict_col[h].append(t)
        if cell_block[h] == cell_block[t]:
            arcs_dict_block[h].append(t)
    return arcs_dict_row, arcs_dict_col, arcs_dict_block


def read_board(path):
    puzzle = dict()
    with open(path, "r") as f:
        for i, line in enumerate(f):
            for j, val in enumerate(line[:-1]):
                if val == "*":
                    puzzle[(i, j)] = set(range(1, 10))
                else:
                    puzzle[(i, j)] = set([int(val)], )
    return puzzle


class Sudoku(object):
    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    BLOCKS = block_dict()
    ARCS_DICT_ROW, ARCS_DICT_COL, ARCS_DICT_BLK = sudoku_arcs_dict(CELLS, ARCS)

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def copy(self):
        return Sudoku(copy.deepcopy(self.board))

    def remove_inconsistent_values(self, head, tail):
        if (head, tail) not in self.ARCS:
            return False
        # remove only if cell2 has a single value
        if len(self.board[tail]) == 1:
            # get the only element from the set
            v = next(iter(self.board[tail]))
            if v in self.board[head]:
                self.board[head].remove(v)
                return True
        return False

    def infer_ac3(self):
        arc_queue = collections.deque(self.ARCS)
        while len(arc_queue) > 0:
            head, tail = arc_queue.popleft()
            # if change made then all arc of head need to be reconsidered
            if self.remove_inconsistent_values(head, tail):
                # then add back all neighbors of head to queue to examine
                for h, t in self.ARCS:
                    if t == head and h != tail and (h, head) not in arc_queue:
                        arc_queue.append((h, head))

    def is_solved(self):
        return all(len(self.board[cell]) == 1 for cell in self.CELLS)

    def is_dead_end(self):
        return any(len(self.board[cell]) == 0 for cell in self.CELLS)

    def infer_improved(self):
        self.infer_ac3()
        # check all the cells with more than one choice
        for head in self.CELLS:
            n = len(self.board[head])
            if n <= 1:
                continue

            # occurs = dict()
            found_hidden_single = False
            for v in self.board[head]:
                for LIST in [self.ARCS_DICT_BLK[head],
                             self.ARCS_DICT_ROW[head],
                             self.ARCS_DICT_COL[head]]:
                    found_elsewhere = False
                    for cell in LIST:
                        if v in self.board[cell]:
                            found_elsewhere = True
                            break
                            # occurs[v] = occurs.get(v, 0) + 1
                    # if len(occurs) == 0:
                    # v not found in any cell of at least one of the LISTs
                    if not found_elsewhere:
                        self.board[head] = [v]
                        self.infer_ac3()
                        found_hidden_single = True
                        break  # breaks LIST loop
                if found_hidden_single:
                    break  # breaks v loop

    def guessHelper(self):

        if self.is_solved():
            return True, self.board
        if self.is_dead_end():
            return False, self.board

        sudoku = self.copy()

        # count all the cells with multiple choices to find the ones
        # with the fewer guess options and most occurences in tail cells
        # priority queue will use #choices, 24-#occurences as the priority
        cell_priority = {i: [] for i in range(2, 10)}
        guess_queue = PriorityQueue()
        min_choices = 9
        max_choices = 0
        for head in sudoku.CELLS:
            n = len(sudoku.board[head])
            if n <= 1:
                continue
            if min_choices >= n:
                min_choices = n
            if max_choices >= n:
                max_choices = n
            cell_priority[n].append(head)

        found_elsewhere = False

        for choice_num in range(min_choices, max_choices + 1):
            for head in cell_priority[choice_num]:
                n = len(sudoku.board[head])
                # only cells with multiple choices
                if n <= 1:
                    continue
                neighbors = set(self.ARCS_DICT_BLK[head]) \
                            | set(self.ARCS_DICT_ROW[head]) \
                            | set(self.ARCS_DICT_COL[head])

                for v in sudoku.board[head]:
                    occurs = 0
                    for cell in neighbors:
                        if v in sudoku.board[cell]:
                            occurs = occurs + 1
                    guess_queue.put((n, 24 - occurs, v, head))
                    found_elsewhere = True

            if found_elsewhere:
                n, prio, v, h = guess_queue.get()
                print("guess ", h, " = ", v, n, prio)
                sudoku.board[h] = [v]
                sudoku.infer_improved()
                found, board = sudoku.guessHelper()
                if found:
                    return True, board
                sudoku = self.copy()

        return False, self.board


def infer_with_guessing(self):
    self.infer_improved()
    solved, board = self.guessHelper()
    self.board = board


def __print__(self):
    brd = [['[**********]' for x in range(9)] for y in range(9)]
    for cell, value in self.board.items():
        brd[cell[0]][cell[1]] = list(value)
    for i in range(9):
        print("-" * 109)
        print("| ", end=' ')
        for j in range(9):
            print(f"{''.join([str(x) for x in brd[i][j]]):9}", end=" | ")
        print()
    print("-" * 109)


b = read_board("soduku_puzzles\medium4.txt")
s = Sudoku(b)
print(s.__print__())
s.infer_ac3()
print(s.__print__())
s.infer_improved()
print(s.__print__())
s.infer_with_guessing()
print(s.__print__())
'''
True set([1, 2, 3, 4, 5, 6, 7, 9])
True set([1, 3, 4, 5, 6, 7, 9])
False set([1, 3, 4, 5, 6, 7, 9])
'''
############################################################
# Feedback
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
