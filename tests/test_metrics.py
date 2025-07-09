import pytest
import numpy as np
from ppet.puf.puf_model import XORArbiterPUF
from ppet.analysis.metrics import calculate_uniqueness, calculate_reliability, calculate_bit_aliasing

@pytest.fixture
def puf_instances():
    """
    Provides a fixed set of PUF instances for testing.
    """
    np.random.seed(42)
    return [XORArbiterPUF(num_arbiters=4, stages_per_arbiter=64) for _ in range(10)]

def test_calculate_uniqueness(puf_instances):
    """
    Tests the uniqueness calculation.
    The result should be close to 0.5 for a good PUF.
    """
    np.random.seed(42)
    uniqueness = calculate_uniqueness(puf_instances, num_challenges=100, challenge_length=64)
    assert 0.4 < uniqueness < 0.6

def test_calculate_reliability(puf_instances):
    """
    Tests the reliability calculation.
    With no noise, reliability should be 1.0.
    """
    np.random.seed(42)
    puf = puf_instances[0]
    challenge = puf.generate_challenge()
    reliability = calculate_reliability(puf, challenge, num_readings=100, temperature=25.0, voltage=1.0)
    assert reliability == 1.0

def test_calculate_reliability_with_noise(puf_instances):
    """
    Tests that reliability decreases with environmental stress.
    """
    np.random.seed(42)
    puf = puf_instances[0]
    challenge = puf.generate_challenge()
    # High temperature should introduce errors
    reliability = calculate_reliability(puf, challenge, num_readings=100, temperature=85.0, voltage=1.0)
    assert reliability < 1.0

def test_calculate_bit_aliasing(puf_instances):
    """
    Tests the bit aliasing calculation.
    The result should be close to 0.5 for an unbiased PUF.
    """
    np.random.seed(42)
    bit_aliasing = calculate_bit_aliasing(puf_instances, num_challenges=100, challenge_length=64)
    # The aliasing of the single output bit
    assert 0.4 < bit_aliasing[0] < 0.7