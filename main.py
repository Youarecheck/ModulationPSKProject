from GetBytes import *
import matplotlib.pyplot as plt
from Modulator import *
from Demodulator import *
from AddAWGNNoise import *
import matplotlib.pyplot as plt
from TransmissionChannel import *



def make_disturbance(N_bits):
    pass # NULL

def calculate_ber(original_bits, decoded_bits):
    """Calculate Bit Error Rate."""
    errors = np.sum(original_bits != decoded_bits)
    ber = errors / len(original_bits)
    return ber


def main():

    bites = gen_bites(10)
    print("orginal Bites: ")
    print(bites)
    demodulated_bites = bpsk_demodulation(add_awgn_noise(bpsk_modulation(bites),0.5))
    print("demodulated Bites: ")
    print(demodulated_bites)
    print("Bit Error Rate: ")
   # print(bites == demodulated_bites)
    print(calculate_ber(bites, demodulated_bites))
    #plt.plot(bites, demodulated_bites)
    #plt.show()





if __name__ == "__main__":
    main()