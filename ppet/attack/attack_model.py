from abc import ABC, abstractmethod
import numpy as np

class Attack(ABC):
    """
    Abstract base class for all attack models.
    """
    @abstractmethod
    def train(self, puf, num_crps):
        """
        Trains the attack model on a given PUF instance.
        
        :param puf: The PUF instance to attack.
        :param num_crps: The number of challenge-response pairs to use for training.
        """
        pass

    @abstractmethod
    def predict(self, challenge):
        """
        Predicts the response of the PUF to a given challenge.
        
        :param challenge: The challenge to predict the response for.
        :return: The predicted response.
        """
        pass

    def evaluate(self, puf, num_test_crps):
        """
        Evaluates the attack model's accuracy.
        
        :param puf: The PUF instance to evaluate against.
        :param num_test_crps: The number of challenge-response pairs to use for testing.
        :return: The prediction accuracy (a float between 0 and 1).
        """
        correct_predictions = 0
        for _ in range(num_test_crps):
            # This needs to be adapted based on the PUF's challenge generation logic
            # For now, we assume a generic way to get a challenge.
            # This part will need to be more sophisticated.
            challenge = puf.generate_challenge() # This method needs to be defined in the PUF base class
            
            true_response = puf.generate_response(challenge)
            predicted_response = self.predict(challenge)
            
            if np.array_equal(true_response, predicted_response):
                correct_predictions += 1
        
        return correct_predictions / num_test_crps

from sklearn.linear_model import LogisticRegression

class LogisticRegressionAttack(Attack):
    """
    A machine learning attack on an Arbiter PUF using Logistic Regression.
    """
    def __init__(self):
        self.model = LogisticRegression()
        self.feature_mapping = self._create_feature_mapping

    @staticmethod
    def _create_feature_mapping(challenge):
        """
        Transforms a challenge into a feature vector suitable for a linear classifier.
        For an Arbiter PUF, this is often the parity of the challenge bits.
        """
        # The feature vector is derived from the challenge.
        # A common approach is to use the "parity" vector.
        # parity[i] = product of challenge[i] to challenge[n-1]
        # where challenge bits are mapped from {0, 1} to {-1, 1}.
        challenge_transformed = np.where(challenge == 0, -1, 1)
        
        # This is a simplified feature mapping. A more advanced one would be needed for XOR PUFs.
        # For a single Arbiter PUF, this is a standard approach.
        return np.cumprod(challenge_transformed[::-1])[::-1]

    def train(self, puf, num_crps):
        """
        Trains the Logistic Regression model on the provided PUF.
        """
        print(f"Training Logistic Regression model with {num_crps} CRPs...")
        challenges = [puf.generate_challenge() for _ in range(num_crps)]
        
        # Generate feature vectors for each challenge
        X_train = np.array([self.feature_mapping(c) for c in challenges])
        
        # Generate responses for each challenge
        y_train = np.array([puf.generate_response(c) for c in challenges])
        
        self.model.fit(X_train, y_train)
        print("Training complete.")

    def predict(self, challenge):
        """
        Predicts the response for a given challenge.
        """
        feature_vector = self.feature_mapping(challenge).reshape(1, -1)
        return self.model.predict(feature_vector)[0]
