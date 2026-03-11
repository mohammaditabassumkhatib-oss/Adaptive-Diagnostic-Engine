import math

class IRTAdaptiveEngine:

    D = 1.7        # IRT scaling constant
    ALPHA = 0.3    # Learning rate
    MIN_THETA = 0.1
    MAX_THETA = 1.0

    def __init__(self, initial_ability: float = 0.5):
        self.theta = initial_ability

    def probability_correct(self, difficulty: float) -> float:
        """
        Probability the student gets this question right,
        given their current ability and the question's difficulty.
        """
        exponent = -self.D * (self.theta - difficulty)
        return 1 / (1 + math.exp(exponent))

    def update_ability(self, difficulty: float, is_correct: bool) -> float:
        """
        Update theta after the student answers a question.
        Returns the new ability score.
        """
        actual = 1 if is_correct else 0
        expected = self.probability_correct(difficulty)

        self.theta = self.theta + self.ALPHA * (actual - expected)

        # Clamp between 0.1 and 1.0
        self.theta = max(self.MIN_THETA, min(self.MAX_THETA, self.theta))

        return round(self.theta, 4)

    def next_difficulty_target(self) -> float:
        """
        The difficulty level the next question should be near.
        """
        return round(self.theta, 2)