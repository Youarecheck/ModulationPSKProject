from AddAWGNNoise import *
import numpy as np
def bpsk_demodulation(recived_symbols):
    decoded_bits = (recived_symbols.real <0).astype(int)
  #  print("demodulated bits:", decoded_bits)


    return decoded_bits


def qpsk_demodulation(received_symbols):


    n_symbols = len(received_symbols)
    bits = np.zeros(n_symbols * 2, dtype=int)

    # Extract I and Q components
    i_component = received_symbols.real
    q_component = received_symbols.imag

    # Decision regions (Gray coding)
    for idx, (i, q) in enumerate(zip(i_component, q_component)):
        if i >= 0 and q >= 0:  # Quadrant I
            bits[2 * idx:2 * idx + 2] = [0, 0]
        elif i < 0 and q >= 0:  # Quadrant II
            bits[2 * idx:2 * idx + 2] = [0, 1]
        elif i < 0 and q < 0:  # Quadrant III
            bits[2 * idx:2 * idx + 2] = [1, 1]
        else:  # Quadrant IV (i >= 0, q < 0)
            bits[2 * idx:2 * idx + 2] = [1, 0]

    return bits


def psk8_demodulation(received_symbols):

    # 8-PSK constellation with Gray coding
    angles = np.array([0, 1, 3, 2, 6, 7, 5, 4]) * np.pi / 4
    constellation = np.exp(1j * angles)

    n_symbols = len(received_symbols)
    bits = np.zeros(n_symbols * 3, dtype=int)

    # For each received symbol, find closest constellation point
    for idx, symbol in enumerate(received_symbols):
        # Calculate distances to all constellation points
        distances = np.abs(symbol - constellation)

        # Find index of closest point
        closest_idx = np.argmin(distances)

        # Convert index to 3 bits
        bit0 = (closest_idx >> 2) & 1
        bit1 = (closest_idx >> 1) & 1
        bit2 = closest_idx & 1

        bits[3 * idx:3 * idx + 3] = [bit0, bit1, bit2]

    return bits


def qam16_demodulation(received_symbols):

    # Denormalize symbols (reverse the 1/sqrt(10) normalization)
    norm = np.sqrt(10)
    denorm_symbols = received_symbols * norm

    n_symbols = len(received_symbols)
    bits = np.zeros(n_symbols * 4, dtype=int)

    # PAM-4 demodulation mapping (Gray coded)
    def pam4_demod(value):
        if value < -2:
            return [0, 0]  # -3
        elif value < 0:
            return [0, 1]  # -1
        elif value < 2:
            return [1, 1]  # +1
        else:
            return [1, 0]  # +3

    # Demodulate each symbol
    for idx, symbol in enumerate(denorm_symbols):
        i_bits = pam4_demod(symbol.real)
        q_bits = pam4_demod(symbol.imag)
        bits[4 * idx:4 * idx + 4] = i_bits + q_bits

    return bits


if __name__ =="__main__":
      # Test all demodulators
    from Modulator import bpsk_modulation, qpsk_modulation
    from TransmissionChannel import transmission_channel

    print("=" * 60)
    print("Testing All Demodulation Schemes")
    print("=" * 60)

    # Test parameters
    eb_n0_db = 5

    # Test 1: BPSK
    print("\n1. BPSK Demodulation")
    print("-" * 60)
    bpsk_bits = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0])
    bpsk_symbols = bpsk_modulation(bpsk_bits)
    bpsk_received = transmission_channel(bpsk_symbols, eb_n0_db)
    bpsk_decoded = bpsk_demodulation(bpsk_received)
    bpsk_errors = np.sum(bpsk_bits != bpsk_decoded)
    print(f"Transmitted bits: {bpsk_bits}")
    print(f"Decoded bits:     {bpsk_decoded}")
    print(f"Errors: {bpsk_errors}/{len(bpsk_bits)} - BER: {bpsk_errors / len(bpsk_bits):.4f}")
    # Test 2: QPSK
    print("\n2. QPSK Demodulation")
    print("-" * 60)
    qpsk_bits = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0])
    qpsk_symbols = qpsk_modulation(qpsk_bits)
    qpsk_received = transmission_channel(qpsk_symbols, eb_n0_db)
    qpsk_decoded = qpsk_demodulation(qpsk_received)
    qpsk_errors = np.sum(qpsk_bits != qpsk_decoded)
    print(f"Transmitted bits: {qpsk_bits}")
    print(f"Decoded bits:     {qpsk_decoded}")
    print(f"Errors: {qpsk_errors}/{len(qpsk_bits)} - BER: {qpsk_errors / len(qpsk_bits):.4f}")
