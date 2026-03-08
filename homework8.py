############################################################
# CIS 521: Homework 8
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import string
import pdb
import re
import random
import math

############################################################

student_name = "Type your full name here."

############################################################
# Section 1: Ngram Models
############################################################


def tokenize(text):
    return re.findall(r"\w+|[^\w\s]", text)


def ngrams(n, tokens):
    padded_tokens = ['<START>'] * (n-1) + tokens + ['<END>']
    context_list = []
    if n < 1:
        return context_list
    for i in range(0, len(padded_tokens) - n + 1):
        context_list.append((tuple(padded_tokens[i: i + n - 1]),
                             padded_tokens[i + n - 1]))
    return context_list


class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.context = dict()
        self.next_token = dict()
        self.tokens = dict()
        self.total_tokens = 0

    def update(self, sentence):
        for (c, e) in ngrams(self.n, tokenize(sentence)):
            self.context[c] = self.context.get(c, 0) + 1
            self.next_token[(c, e)] = self.next_token.get((c, e), 0) + 1
            self.tokens[e] = self.tokens.get(e, 0) + 1
        self.total_tokens = sum(self.tokens.values())

    def prob(self, context, token):
        context_occurences = self.context.get(context, 0)
        if context_occurences == 0:
            return 0
        return self.next_token.get((context, token), 0) / context_occurences

    def random_token(self, context):
        r = random.random()
        # get all tokens generating for a certain context and sort them by
        # token lexicographic order
        lexi_ordered_tokens = sorted([t for (c, t) in self.next_token
                                      if c == context])
        cum_sum = 0.0
        for t in lexi_ordered_tokens:
            cum_sum += self.prob(context, t)
            if cum_sum > r:
                return t

    def random_text(self, token_count):
        new_context = ["<START>" for _ in range(self.n - 1)]
        for i in range(token_count):
            new_token = self.random_token(tuple(new_context[
                                                i: i + self.n - 1]))
            if new_token == "<END>":
                new_context.append("<START>")
            elif new_token is None:
                pass
            else:
                new_context.append(new_token)
        return " ".join(t for t in new_context if t != "<START>")

    def perplexity(self, sentence):
        tokens_ = tokenize(sentence)
        ngrams_ = ngrams(self.n, tokens_)
        prob_sum = 0.0
        for (c, e) in ngrams_:
            prob_sum += math.log(self.prob(c, e))
        return math.exp(-prob_sum / len(ngrams_))


def create_ngram_model(n, path):
    model = NgramModel(n)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line:
                model.update(line)
    return model


############################################################
# Section 2: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
I spent 3 hours on the assignment
"""

feedback_question_2 = """
Calculating perplexity was the most challenging
No significant stumbling blocks
"""

feedback_question_3 = """
I liked the probability calculations
Would not change anything
"""
