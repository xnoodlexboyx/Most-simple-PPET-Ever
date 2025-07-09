import numpy as np

class ArbiterPUF:
    """
    A simple Arbiter PUF model.
    """
    def __init__(self, stages):
        self.stages = stages
        # Each stage has two paths, with a slight delay difference
        # Represented as a random delay for each path
        self.delays = np.random.rand(stages, 2) * 2 - 1 # Delays between -1 and 1

    def generate_response(self, challenge):
        """
        Generates a response for a given challenge.
        Challenge is a binary array of length 'stages'.
        """
        if len(challenge) != self.stages:
            raise ValueError(f"Challenge length must match the number of stages ({self.stages})")

        # Simulate the path delays
        # For a simple Arbiter PUF, the response is determined by the cumulative delay difference
        # between the two paths.
        
        # Initialize cumulative delays for both paths
        path_0_delay = 0
        path_1_delay = 0

        for i in range(self.stages):
            if challenge[i] == 0: # Straight path
                path_0_delay += self.delays[i, 0]
                path_1_delay += self.delays[i, 1]
            else: # Crossover path
                path_0_delay += self.delays[i, 1]
                path_1_delay += self.delays[i, 0]
        
        # The response bit is 0 if path 0 is faster, 1 if path 1 is faster
        response_bit = 0 if path_0_delay < path_1_delay else 1
        return response_bit

class XORArbiterPUF:
    """
    A simple XOR Arbiter PUF model, composed of multiple Arbiter PUFs.
    """
    def __init__(self, num_arbiters, stages_per_arbiter):
        self.num_arbiters = num_arbiters
        self.stages_per_arbiter = stages_per_arbiter
        self.arbiters = [ArbiterPUF(stages_per_arbiter) for _ in range(num_arbiters)]

    def generate_response(self, challenge):
        """
        Generates a response for a given challenge by XORing responses from multiple Arbiter PUFs.
        """
        if len(challenge) != self.stages_per_arbiter:
            raise ValueError(f"Challenge length must match the number of stages per arbiter ({self.stages_per_arbiter})")
        
        # Generate responses from each individual arbiter PUF
        arbiter_responses = [arbiter.generate_response(challenge) for arbiter in self.arbiters]
        
        # XOR all responses
        xor_response = 0
        for res in arbiter_responses:
            xor_response ^= res
            
        return xor_response