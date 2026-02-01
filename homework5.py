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

############################################################

student_name = "Theophilos Constantinidis"


############################################################
# Sudoku Solver
############################################################


def sudoku_cells():
    return [(x, y) for x in range(9) for y in range(9)]

def box_coords(cell):
    return cell[0] // 3, cell[1] // 3

def box_dict():
    boxes = {(br, bc): [] for br in range(3) for bc in range(3)}
    for cell in sudoku_cells():
        boxes[box_coords(cell)].append(cell)
    return boxes

def sudoku_arcs():
    arc_list = []
    boxes = box_dict()
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
        for cell in boxes[box_coords((i, j))]:
            if (i, j) != cell:
                arc = ((i, j), cell)
                if arc not in arc_list:
                    arc_list.append(arc)
    return arc_list

def read_board(path):
    puzzle = dict()
    with open(path, "r") as f:
        for i, line in enumerate(f):
            for j, val in enumerate(line[:-1]):
                if val == "*":
                    puzzle[(i, j)] = set(range(1, 10))
                else:
                    puzzle[(i, j)] = set([int(val)],)
    return puzzle


class Sudoku(object):
    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

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


    def infer_improved(self):
        pass

    def infer_with_guessing(self):
        pass

    def __print__(self):
        brd = [['[**********]' for x in range(9)] for y in range(9)]
        for cell, value in self.board.items():
            brd[cell[0]][cell[1]] = list(value)
        for i in range(9):
            print("-"*109)
            print("| ", end= ' ')
            for j in range(9):
                print(f"{''.join([str(x) for x in brd[i][j]]):9}", end=" | ")
            print()
        print("-"*109)


b = read_board("soduku_puzzles\easy.txt")
s = Sudoku(b)
print(s.__print__())
s.infer_ac3()
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
