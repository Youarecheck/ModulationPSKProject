from AddAWGNNoise import *
import numpy as np
def bpsk_demodulation(recived_symbols):
    decoded_bits = (recived_symbols.real <0).astype(int)


    return decoded_bits




def qpsk_demodulation(recived_symbols):
    n_symbols = len(recived_symbols)
    bits =np.zeros(n_symbols*2, dtype=int)

    i_component = recived_symbols.real
    q_component = recived_symbols.imag

    for idx, (i,q) in enumerate(zip(i_component, q_component)):
        if i >= 0 and q >= 0:
            bits[2*idx:2*idx+2] = [0, 0]
        elif i<0 and q >= 0:
            bits[2*idx:2*idx+2] = [0, 1]
        elif i<0 and q<0:
            bits[2*idx:2*idx+2] = [1, 1]
        else:
            bits[2*idx:2*idx+2] = [1, 0]

        return bits