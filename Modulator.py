import numpy as np
from scipy.signal.windows import cosine

from GetBytes import *
import main
### constant variables - start
#Amplitude = 64

#angular_velocity = 20 # anguar in  rad

### constant variables - end

def bpsk_modulation(bits):
    symbols = 1-2 * bits # [1-2 * bits for bits in bites_]

    ### bits:            [1 , 1, 0, 1 ...] W
    ### bpsk_modulation: [-1,  -1, 1, ...] W
    return symbols.astype(complex)
    #s1 = Amplitude * cosine(angular_velocity * time)
    #s2 = -s1

    #return

x = gen_bites(10)
print(x)
print(bpsk_modulation(x))
