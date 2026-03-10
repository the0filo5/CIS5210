import random

student_name = "Type your full name here."


# 1. Q-Learning
class QLearningAgent:
    """Implement Q Reinforcement Learning Agent using Q-table."""

    def __init__(self, game, discount, learning_rate, explore_prob):
        """Store any needed parameters into the agent object.
        Initialize Q-table.
        """
        self.game = game
        self.discount = discount
        self.learning_rate = learning_rate
        self.explore_prob = explore_prob
        self.q_table = dict()

    def get_q_value(self, state, action):
        """Retrieve Q-value from Q-table.
        For an never seen (s,a) pair, the Q-value is by default 0.
        """
        return self.q_table.get((state, action), 0.0)

    def get_value(self, state):
        """Compute state value from Q-values using Bellman Equation.
        V(s) = max_a Q(s,a)
        """
        actions = sorted(self.game.get_actions(state), key=str)
        if not actions:
            return 0.0
        return max(self.get_q_value(state, a) for a in actions)

    def get_best_policy(self, state):
        """Compute the best action to take in the state using Policy
        Extraction.
        π(s) = argmax_a Q(s,a)

        If there are ties, return a random one for better performance.
        Hint: use random.choice().
        """
        actions = sorted(self.game.get_actions(state), key=str)
        if not actions:
            return None
        max_qs = max(self.get_q_value(state, a) for a in actions)
        best_actions = [a for a in actions if self.get_q_value(state, a
                                                               ) == max_qs]
        return random.choice(best_actions)

    def update(self, state, action, next_state, reward):
        """Update Q-values using running average.
        Q(s,a) = (1 - α) Q(s,a) + α (R + γ V(s'))
        Where α is the learning rate, and γ is the discount.

        Note: You should not call this function in your code.
        """
        sample = reward + self.discount * self.get_value(next_state)
        old_q = self.get_q_value(state, action)
        self.q_table[(state, action)] = (
                (1 - self.learning_rate) * old_q
                + self.learning_rate * sample
        )

    # 2. Epsilon Greedy
    def get_action(self, state):
        """Compute the action to take for the agent, incorporating exploration.
        That is, with probability ε, act randomly.
        Otherwise, act according to the best policy.

        Hint: use random.random() < ε to check if exploration is needed.
        """
        actions = list(self.game.get_actions(state))
        if not actions:
            return None

        if random.random() < self.explore_prob:
            return random.choice(actions)
        return self.get_best_policy(state)


# 3. Bridge Crossing Revisited
def question3():
    epsilon = 0.05
    learning_rate = 0.2
    return 'NOT POSSIBLE'  # epsilon, learning_rate
    # If not possible, return 'NOT POSSIBLE'


# 5. Approximate Q-Learning
class ApproximateQAgent(QLearningAgent):
    """Implement Approximate Q Learning Agent using weights."""

    def __init__(self, *args, extractor):
        """Initialize parameters and store the feature extractor.
        Initialize weights table."""

        super().__init__(*args)
        self.extractor = extractor
        self.weights = dict()

    def get_weight(self, feature):
        """Get weight of a feature.
        Never seen feature should have a weight of 0.
        """
        if feature not in self.weights:
            self.weights[feature] = 0.0
        return self.weights[feature]

    def get_q_value(self, state, action):
        """Compute Q value based on the dot product of feature
        components and weights.
        Q(s,a) = w_1 * f_1(s,a) + w_2 * f_2(s,a) + ... + w_n * f_n(s,a)
        """
        return sum(self.get_weight(f) * v for f, v in
                   self.extractor(state, action).items())

    def update(self, state, action, next_state, reward):
        """Update weights using least-squares approximation.
        Δ = R + γ V(s') - Q(s,a)
        Then update weights: w_i = w_i + α * Δ * f_i(s, a)
        """
        delta = (reward + self.discount * self.get_value(next_state)
                 - self.get_q_value(state, action)
                 )
        for (f, v) in self.extractor(state, action).items():
            self.weights[f] = self.get_weight(
                f) + self.learning_rate * delta * v


# 6. Feedback
# Just an approximation is fine.
feedback_question_1 = """
I spent about 4 hours
"""

feedback_question_2 = """
The PAC man.   No real stumbling blocks
"""

feedback_question_3 = """
The learning nature and simplicity of the agent.  Would not change anything.
"""
