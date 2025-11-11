import numpy as np
from scipy.signal.windows import cosine
from scipy.special import pbdn_seq

from GetBytes import *
import main
### constant variables - start
#Amplitude = 64

#angular_velocity = 20 # anguar in  rad

### constant variables - end

def test():
    print(qpsk_modulation(gen_bites(10)))

def bpsk_modulation(bits):
    symbols = 1-2 * bits # [1-2 * bits for bits in bites_]

    ### bits:            [1 , 1, 0, 1 ...] W
    ### bpsk_modulation: [-1,  -1, 1, ...] W


    return symbols.astype(complex)
    #s1 = Amplitude * cosine(angular_velocity * time)
    #s2 = -s1

    #return
def qpsk_modulation(bits):
    if len(bits)%2 != 0:
        raise ValueError("Number of bits must be even")


    bits_pair= bits.reshape(-1,2)
  #  print(bits_pair)

    norm = 1 / np.sqrt(2)

    qpsk_map ={
        (0,0): norm * (1+1j),
        (0,1): norm * (-1+1j),
        (1,1): norm * (-1-1j),
        (1,0): norm * (1-1j),
    }

    symbols = np.array([qpsk_map[tuple(pair)] for pair in bits_pair], dtype=complex)



    return symbols


if __name__ == "__main__":
    test()


