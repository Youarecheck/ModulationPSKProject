import numpy as np


def gen_bites(N_bits):
    return np.random.randint(0, 2, size=(N_bits))