import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')

############################################################
# CIS 521: Homework 1
############################################################

student_name = "Theophilos Constantinidis"
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
    The keys of a dictionary have to be immutable types,
    so when they are hashed the hash does not change, suh as strings,
    numbers, and tuples.
    So a solution would be to convert the lists to tuples and use them as keys

    points_to_names = {(0, 0): "home", (1, 2): "school", (-1, 1): "market"}
"""

python_concepts_question_3 = """
    concatenate2 would be faster as it has been implemented in C (CPython) and
    not in pure python as in the case of the concatenate1 loop.  In python
    using += , the string is recreated in every rotation copying and
    reallocating memory each time the string grows.
    In CPython the implementation first calculates how much memor
    it needs and allocates it from the beginning.
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
    return seq[:]


def all_but_last(seq):
    return seq[:-1]


def every_other(seq):
    return seq[::2]


############################################################
# Section 4: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(0, len(seq) + 1):
        yield seq[0:i]


def suffixes(seq):
    for i in range(0, len(seq) + 1):
        yield seq[i:]


def slices(seq):
    for j in range(0, len(seq)):
        for i in range(0, len(seq) - j):
            yield seq[j:j + i + 1]


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
               '5': 'five', '6': 'six', '7': 'seven', '8': 'eight',
               '9': 'nine'}
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
        self.coefficients = tuple(polynomial)

    def get_polynomial(self):
        return self.coefficients

    def __neg__(self):
        return Polynomial([(-coef, p) for coef, p in self.coefficients])

    def __add__(self, other):
        combined_list = list(self.coefficients)
        combined_list.extend(other.get_polynomial())
        return Polynomial(combined_list)  # or return combined_list

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        multiplied_coefficients = []
        for coef1, pow1 in self.coefficients:
            for coef2, pow2 in other.coefficients:
                multiplied_coefficients.append((coef1 * coef2, pow1 + pow2))
        return Polynomial(multiplied_coefficients)

    def __call__(self, x):
        if x == 0 and any(power < 0 for _, power in self.coefficients):
            return ZeroDivisionError("Cannot apply polynomial to 0 division")
        return sum(coef * (x ** power) for coef, power in self.coefficients)

    # sort and return a polynomial in descending power of polynomial element
    def sort(self):
        return Polynomial(
            sorted(self.coefficients, key=lambda term: term[1], reverse=True))

    def simplify(self):
        # Create a dictionary by power
        group_by_power = {}
        # Create unique list of powers in descending order
        for coef, power in self.coefficients:
            group_by_power[power] = group_by_power.get(power, 0) + coef
        # iterate through all dict terms and keep ones with non-zero coefs
        no_zero_terms = [(round(coef), p) for p, coef in group_by_power.items()
                         if coef != 0]
        # Update (0, 0) if no non-zero terms
        if not no_zero_terms:
            self.coefficients = (0, 0)
        else:
            # Update with simplified polynomial is descending power order
            no_zero_terms.sort(key=lambda t: t[1], reverse=True)
            self.coefficients = tuple(no_zero_terms)

    def __str__(self):
        # no leading space for sign of first coef
        lead_space = ''
        sequence = ''
        # starts with no operator for first positive coef
        operator = ''
        var = 'x'
        for i, (coef, power) in enumerate(self.coefficients):
            # if coef negative use - sign
            if coef < 0:
                operator = '-'
            # if power zero then no 'x'
            if power == 0:
                var = ''
            coeff = f"{abs(coef)}"
            # if coeff = 1 and power not 0, then no 1
            if abs(coef) == 1 and power != 0:
                coeff = ""
            # if power 1 or 0 then no ^ sign and power number
            if power == 1 or power == 0:
                sequence += operator + lead_space + f"{coeff}{var} "
            else:
                sequence += operator + lead_space + f"{coeff}{var}^{power} "
            # reset parameters for next loop
            lead_space = ' '
            operator = '+'
            var = 'x'
        # return sequence without last trailing space
        return sequence[:-1]


############################################################
# Section 7: Python Packages
############################################################

def sort_array(list_of_matrices):
    return np.array(sorted([int(elem) for matrix in list_of_matrices
                            for elem in matrix.flatten()],
                           reverse=True)
                    )


def POS_tag(sentence):
    list_tokens = nltk.word_tokenize(sentence)
    list_words = [w.lower() for w in list_tokens if
                  w.lower() not in stopwords.words('english')
                  and w not in "!""#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"]
    return nltk.pos_tag(list_words)


############################################################
# Section 8: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
5 hours
"""

feedback_question_2 = """
The most challenging without being necessarily difficult was converting
loops into single list comprehensions and generators.
"""

feedback_question_3 = """
Single list comprehensions.
No would not change anything.
"""
