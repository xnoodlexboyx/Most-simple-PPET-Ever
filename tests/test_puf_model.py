import pytest
import numpy as np
from ppet.puf.puf_model import ArbiterPUF, XORArbiterPUF, SRAMPUF, RingOscillatorPUF

def test_arbiter_puf_instantiation():
    """
    Tests that an ArbiterPUF can be instantiated with the correct number of stages.
    """
    puf = ArbiterPUF(stages=64)
    assert puf.stages == 64
    assert puf.delays.shape == (64, 2)

def test_xor_arbiter_puf_instantiation():
    """
    Tests that an XORArbiterPUF can be instantiated correctly.
    """
    puf = XORArbiterPUF(num_arbiters=4, stages_per_arbiter=64)
    assert puf.num_arbiters == 4
    assert len(puf.arbiters) == 4
    assert all(isinstance(arb, ArbiterPUF) for arb in puf.arbiters)

def test_sram_puf_instantiation():
    """
    Tests that an SRAMPUF can be instantiated correctly.
    """
    puf = SRAMPUF(rows=128, cols=128)
    assert puf.rows == 128
    assert puf.cols == 128
    assert puf.sram_array.shape == (128, 128)

def test_ro_puf_instantiation():
    """
    Tests that a RingOscillatorPUF can be instantiated correctly.
    """
    puf = RingOscillatorPUF(num_oscillators=256)
    assert puf.num_oscillators == 256
    assert puf.frequencies.shape == (256,)