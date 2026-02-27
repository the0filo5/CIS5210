# Include your imports here, if any are used.
import numpy as np

from gridworld import Gridworld

student_name = "Type your full name here."


# 1. Value Iteration
class ValueIterationAgent:
    """Implement Value Iteration Agent using Bellman Equations."""

    def __init__(self, game, discount):
        """Store game object and discount value into the agent object,
        initialize values if needed.
        """
        self.values = {}
        for state in game.states:
            self.values[state] = 0.0
        self.game = game
        self.discount = discount
        self.policy = {}
        for s in self.game.states:
            self.policy[s] = self.get_best_policy(s)
            # actions = sorted(self.game.get_actions(s), key=str)
            # self.policy[s] = actions[0] if actions else None
        # All states except terminal, start, and
        print(game.states)

        print("\n".join(
            [f"{s}: {game.get_actions(s)}" for s in game.states]
        ))
        for s in game.states:
            print(s, ":", end="")
            for a in list(game.get_actions(s)):
                print(str(a), " > ", game.get_transitions(s, a), end=", ")
            print()
        for s in game.states:
            print(s, ":")
            for a in list(game.get_actions(s)):
                s_ = game._do_action(s, a)
                if s == s_:
                    print(str(s), str(a), str(s_))
                else:
                    print(str(s),str(a),str(s_), " > ",
                          game.get_reward(s, a, s_))

    def get_value(self, state):
        """Return value V*(s) correspond to state.
        State values should be stored directly for quick retrieval.
        """
        # terminal reward comes from grid value
        # terminal states aren't in game.states so add 0.0 to get_value
        return self.values.get(state, 0.0)

    def get_q_value(self, state, action):
        """Return Q*(s,a) correspond to state and action.
        Q-state values should be computed using Bellman equation:
        Q*(s,a) = Σ_s' T(s,a,s') [R(s,a,s') + γ V*(s')]
        """
        q_total = 0.0
        for s_, prob in self.game.get_transitions(state, action).items():
            q_total += prob * (self.game.get_reward(state, action, s_) +
                        self.discount * self.get_value(s_))
        return q_total

    def get_best_policy(self, state):
        """Return policy π*(s) correspond to state.
        Policy should be extracted from Q-state values using policy extraction:
        π*(s) = argmax_a Q*(s,a)
        """
        actions = sorted(self.game.get_actions(state), key=str)
        if not actions:
            return None
        policies = [self.get_q_value(state, a) for a in actions]
        return actions[int(np.argmax(policies))]

    def iterate(self):
        """Run single synchronous value iteration using Bellman equation:
        V_{k+1}(s) = max_a Q*(s,a)
        Then update values: V*(s) = V_{k+1}(s)
        """
        new_values = dict(self.values)  # or {} and fill it

        for s in self.game.states:
            actions = sorted(self.game.get_actions(s), key=str)
            if not actions:
                new_values[s] = 0.0
                continue
            q_values = [self.get_q_value(s, a) for a in actions]
            new_values[s] = max(q_values)

        self.values = new_values


# 2. Policy Iteration
class PolicyIterationAgent(ValueIterationAgent):
    """Implement Policy Iteration Agent.

    The only difference between policy iteration and value iteration is at
    their iteration method. However, if you need to implement helper function
    or override ValueIterationAgent's methods, you can add them as well.
    """
    def max_abs_diff(self, v1, v2):
        return max(abs(v1[s] - v2[s]) for s in self.game.states)

    def iterate(self):
        """Run single policy iteration.
        Fix current policy, iterate state values V(s) until
        |V_{k+1}(s) - V_k(s)| < ε
        """
        epsilon = 1e-6
        prev_values = dict(self.values)

        while True:
            new_values = dict(prev_values)
            for s in self.game.states:
                actions = self.game.get_actions(s)
                if not actions:  # terminal
                    new_values[s] = 0.0
                    continue
                action = self.policy[s]     # fixed π(s)
                total = 0.0
                for s_, prob in self.game.get_transitions(s, action).items():
                    total += prob * (self.game.get_reward(s, action, s_) +
                                self.discount * prev_values.get(s_, 0.0))
                new_values[s] = total
            if self.max_abs_diff(prev_values, new_values) < epsilon:
                self.values = new_values
                for s in self.game.states:
                    self.policy[s] = self.get_best_policy(s)
                return

            prev_values = new_values


# 3. Bridge Crossing Analysis
def question_3():
    discount = ...
    noise = ...
    return discount, noise


# 4. Policies
def question_4a():
    discount = ...
    noise = ...
    living_reward = ...
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4b():
    discount = ...
    noise = ...
    living_reward = ...
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4c():
    discount = ...
    noise = ...
    living_reward = ...
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4d():
    discount = ...
    noise = ...
    living_reward = ...
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4e():
    discount = ...
    noise = ...
    living_reward = ...
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


# 5. Feedback
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
