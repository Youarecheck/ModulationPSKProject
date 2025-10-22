from GetBytes import *
import matplotlib.pyplot as plt
from Modulator import *
from Demodulator import *
from AddAWGNNoise import *
import matplotlib.pyplot as plt



def make_disturbance(N_bits):
    pass # NULL



def main():

    bites = gen_bites(614)
    #print(bites)
    my_array = bpsk_demodulation(add_awgn_noise(bpsk_modulation(bites),0.5))
    ##print(bites == my_array)
    print(calculate_ber(bites, my_array))
    plt.plot(bites, my_array)
    plt.show()





if __name__ == "__main__":
    main()