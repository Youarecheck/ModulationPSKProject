import numpy as np
import matplotlib.pyplot as plt


def gen_bites(N_bits):
    return np.random.randint(0, 2, size=(N_bits))

def make_disturbance(N_bits):
    pass

print(gen_bites(2))
