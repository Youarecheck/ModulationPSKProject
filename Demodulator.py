from AddAWGNNoise import *
import numpy as np
def bpsk_demodulation(recived_symbols):
    decoded_bits = (recived_symbols.real <0).astype(int)
    return decoded_bits