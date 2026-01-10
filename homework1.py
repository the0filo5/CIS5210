import numpy
import nltk

############################################################
# CIS 521: Homework 1
############################################################

student_name = "Theophilos Constantinidis"
git
init
# This is where your grade report will be sent.
student_email = "theocon@seas.upenn.edu"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
    Dynamically typed means that variable types are defined during run-time 
    and don't need to be pre-defined.
    Also it means their type can be changed during run-time as well.
    Examples:
    myVar = 9
    myVar = "nine"
    
    Strongly typed means that python wont allow operations between 
    by silently converting incompatible types in most cases."
    Examples:
    myVar1 = 9
    myVar2 = "6"
    # Below gives TypeError: unsupported operand type(s) for +: 'int' and 'str'
    mySum = myVar1 + myVar2
"""

python_concepts_question_2 = """
    The keys of a dictionary have to be immutable types, so when they are hashed
    the hash does not change, suh as strings, numbers, and tuples.  
    So a solution would be to convert the lists to tuples and use them as keys
    
    points_to_names = {(0, 0): "home", (1, 2): "school", (-1, 1): "market"}
"""

python_concepts_question_3 = """
    concatenate2 would be faster as it has been implemented in C (CPython) and
    not in pure python as in the case of the concatenate1 loop.  In python using
    += , the string is recreated in every rotation copying and reallocating 
    memory each time the string grows.  In CPython the implementation first
    calculates how much memor it needs and allocates it from the beginning.
"""

############################################################
# Section 2: Working with Lists
############################################################


def extract_and_apply(lst, p, f):
    pass


def concatenate(seqs):
    pass


def transpose(matrix):
    pass


############################################################
# Section 3: Sequence Slicing
############################################################


def copy(seq):
    pass


def all_but_last(seq):
    pass


def every_other(seq):
    pass


############################################################
# Section 4: Combinatorial Algorithms
############################################################


def prefixes(seq):
    pass


def suffixes(seq):
    pass


def slices(seq):
    pass


############################################################
# Section 5: Text Processing
############################################################


def normalize(text):
    pass


def no_vowels(text):
    pass


def digits_to_words(text):
    pass


def to_mixed_case(name):
    pass


############################################################
# Section 6: Polynomials
############################################################


class Polynomial(object):

    def __init__(self, polynomial):
        pass

    def get_polynomial(self):
        pass

    def __neg__(self):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __call__(self, x):
        pass

    def simplify(self):
        pass

    def __str__(self):
        pass


############################################################
# Section 7: Python Packages
############################################################


def sort_array(list_of_matrices):
    pass


def POS_tag(sentence):
    pass


############################################################
# Section 8: Feedback
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
