import numpy as np
from abc import ABC, abstractmethod

class PUF(ABC):
    """
    Abstract base class for all PUF models.
    """
    @abstractmethod
    def generate_response(self, challenge, temperature=25.0, voltage=1.0):
        """
        Generates a response for a given challenge.
        """
        pass

    @abstractmethod
    def generate_challenge(self):
        """
        Generates a valid challenge for the PUF.
        """
        pass

class ArbiterPUF(PUF):
    """
    A simple Arbiter PUF model.
    """
    def __init__(self, stages):
        self.stages = stages
        # Each stage has two paths, with a slight delay difference
        # Represented as a random delay for each path
        self.delays = np.random.rand(stages, 2) * 2 - 1 # Delays between -1 and 1

    def generate_response(self, challenge, temperature=25.0, voltage=1.0):
        """
        Generates a response for a given challenge, optionally considering environmental factors.
        Challenge is a binary array of length 'stages'.
        Temperature is in Celsius, Voltage is in Volts.
        """
        if len(challenge) != self.stages:
            raise ValueError(f"Challenge length must match the number of stages ({self.stages})")

        # Simulate the effect of temperature and voltage on delays
        temp_effect = 1 + (temperature - 25.0) * 0.002
        volt_effect = 1 - (voltage - 1.0) * 0.05
        
        effective_delays = self.delays * temp_effect * volt_effect

        # Add a small amount of Gaussian noise to simulate thermal jitter
        # The noise increases with temperature
        noise_magnitude = abs(temperature - 25.0) * 0.01
        noisy_delays = effective_delays + np.random.normal(0, noise_magnitude, effective_delays.shape)

        # Initialize cumulative delays for both paths
        path_0_delay = 0
        path_1_delay = 0

        for i in range(self.stages):
            if challenge[i] == 0: # Straight path
                path_0_delay += noisy_delays[i, 0]
                path_1_delay += noisy_delays[i, 1]
            else: # Crossover path
                path_0_delay += noisy_delays[i, 1]
                path_1_delay += noisy_delays[i, 0]
        
        # The response bit is 0 if path 0 is faster, 1 if path 1 is faster
        response_bit = 0 if path_0_delay < path_1_delay else 1
        return response_bit

    def generate_challenge(self):
        return np.random.randint(0, 2, self.stages)

class XORArbiterPUF(PUF):
    """
    A simple XOR Arbiter PUF model, composed of multiple Arbiter PUFs.
    """
    def __init__(self, num_arbiters, stages_per_arbiter):
        self.num_arbiters = num_arbiters
        self.stages_per_arbiter = stages_per_arbiter
        self.arbiters = [ArbiterPUF(stages_per_arbiter) for _ in range(num_arbiters)]

    def generate_response(self, challenge, temperature=25.0, voltage=1.0):
        """
        Generates a response for a given challenge by XORing responses from multiple Arbiter PUFs,
        optionally considering environmental factors.
        """
        if len(challenge) != self.stages_per_arbiter:
            raise ValueError(f"Challenge length must match the number of stages per arbiter ({self.stages_per_arbiter})")
        
        # Generate responses from each individual arbiter PUF, passing on the stress parameters
        arbiter_responses = [arbiter.generate_response(challenge, temperature=temperature, voltage=voltage) for arbiter in self.arbiters]
        
        # XOR all responses
        xor_response = 0
        for res in arbiter_responses:
            xor_response ^= res
            
        return xor_response

    def generate_challenge(self):
        return np.random.randint(0, 2, self.stages_per_arbiter)

class SRAMPUF(PUF):
    """
    A simple SRAM PUF model.
    The PUF is modeled as a 2D array of random bits.
    A challenge selects a subset of these bits to form the response.
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Initialize SRAM with random startup values (0 or 1)
        self.sram_array = np.random.randint(0, 2, size=(rows, cols))

    def generate_response(self, challenge, temperature=25.0, voltage=1.0):
        """
        Generates a response for a given challenge.
        The challenge is expected to be a list of tuples, where each tuple
        is a (row, col) coordinate of a bit to be included in the response.
        """
        # A simple noise model for SRAM PUF: temperature can cause bit flips.
        # The probability of a flip is proportional to the deviation from nominal temperature.
        flip_probability = abs(temperature - 25.0) * 0.005
        
        response_bits = []
        for r, c in challenge:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                bit = self.sram_array[r, c]
                if np.random.rand() < flip_probability:
                    bit = 1 - bit
                response_bits.append(bit)
            else:
                raise ValueError(f"Invalid address in challenge: ({r}, {c})")
        
        return np.array(response_bits)

    def generate_challenge(self, num_bits=128):
        """
        Generates a random challenge for the SRAM PUF by selecting random cell locations.
        """
        challenge = []
        for _ in range(num_bits):
            r = np.random.randint(0, self.rows)
            c = np.random.randint(0, self.cols)
            challenge.append((r, c))
        return challenge

class RingOscillatorPUF(PUF):
    """
    A simple Ring Oscillator (RO) PUF model.
    The PUF is modeled as a set of ROs, each with a slightly different native frequency.
    A challenge consists of selecting two ROs to compare their frequencies.
    """
    def __init__(self, num_oscillators):
        self.num_oscillators = num_oscillators
        # Assign a random native frequency to each oscillator
        # Frequencies are centered around a mean with some random variation
        self.frequencies = 1e6 + np.random.randn(num_oscillators) * 1e3

    def generate_response(self, challenge, temperature=25.0, voltage=1.0):
        """
        Generates a response for a given challenge, optionally considering environmental factors.
        The challenge is a tuple or list containing the indices of two oscillators to compare.
        """
        if len(challenge) != 2:
            raise ValueError("Challenge for RO PUF must be a pair of oscillator indices.")
        
        ro1_idx, ro2_idx = challenge
        if not (0 <= ro1_idx < self.num_oscillators and 0 <= ro2_idx < self.num_oscillators):
            raise ValueError("Oscillator index out of bounds.")

        # Simulate the effect of temperature and voltage on frequencies
        temp_effect = 1 - (temperature - 25.0) * 0.001
        volt_effect = 1 + (voltage - 1.0) * 0.02
        base_frequencies = self.frequencies * temp_effect * volt_effect
        
        # Add jitter proportional to temperature deviation
        noise_magnitude = abs(temperature - 25.0) * 100.0
        noisy_frequencies = base_frequencies + np.random.normal(0, noise_magnitude, base_frequencies.shape)
        
        if noisy_frequencies[ro1_idx] > noisy_frequencies[ro2_idx]:
            return 1
        else:
            return 0

    def generate_challenge(self):
        """
        Generates a random challenge for the RO PUF by selecting two different oscillators.
        """
        indices = np.random.choice(self.num_oscillators, 2, replace=False)
        return tuple(indices)