import numpy as np


def add_awgn_noise(bpskSymbols, Eb_No_db):
    Eb_no = 10**(Eb_No_db/ 10.0) # Convertion from dB to float number

    Eb= 1.0 # Energy of bit
    N0 = Eb/Eb_no

    sigma = np.sqrt(N0/2) # standard deviation
    NSymbols = bpskSymbols.shape[0] # Number of symbols

    noise_I =sigma * np.random.normal(0, 1, size=NSymbols)
    noise_Q =sigma * np.random.normal(0, 1, size=NSymbols)

    awgnNoise = noise_I + 1j * noise_Q


    recivedSymbols = bpskSymbols + awgnNoise
    return recivedSymbols