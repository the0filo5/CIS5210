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
    return [f(x) for x in lst if p(x)]


def concatenate(seqs):
    return [element for sequence in seqs for element in sequence]


def transpose(matrix):
    return [[row[j] for row in matrix] for j in range(len(matrix[0]))]


############################################################
# Section 3: Sequence Slicing
############################################################


def copy(seq):
    return seq


def all_but_last(seq):
    return seq[:-1]


def every_other(seq):
    return [seq[i] for i in range(0, len(seq), 2)]


############################################################
# Section 4: Combinatorial Algorithms
############################################################


def prefixes(seq):
    return [seq[0:i] for i in range(0, len(seq) + 1)]


def suffixes(seq):
    return [seq[i:] for i in range(0, len(seq) + 1)]


def slices(seq):
    return [seq[j:j + i + 1] for j in range(0, len(seq)) for i in
            range(0, len(seq) - j)]


############################################################
# Section 5: Text Processing
############################################################


def normalize(text):
    # Set to lowercase
    # Isolate words between white spaces and join them with ' ' in between
    return " ".join(text.lower().split())


def no_vowels(text):
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    return "".join(x for x in text if x not in vowels)

def digits_to_words(text):
    numbers = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
               '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
    return " ".join(numbers[x] for x in text if x in numbers)

def to_mixed_case(name):
    # Obtain words from variable name separated by _
    words = name.replace('_', ' ')
    words = words.strip().split()
    # If no words found return empty string
    if not words:
        return ""
    # First word lower character
    first_word = words[0].lower()
    # If more than 1 word join the rest capitalised
    if len(words) > 1:
        return first_word + "".join(w.capitalize() for w in words[1:])
    return first_word


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
