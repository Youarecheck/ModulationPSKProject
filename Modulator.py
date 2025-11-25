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


def psk8_modulation(bits):

    # Check if number of bits is multiple of 3
    if len(bits) % 3 != 0:
        raise ValueError("Number of bits must be multiple of 3 for 8-PSK")

    # Reshape bits into triplets
    bit_triplets = bits.reshape(-1, 3)

    # 8-PSK constellation (Gray coding)
    # Angles: 0, 45, 90, 135, 180, 225, 270, 315 degrees
    angles = np.array([0, 1, 3, 2, 6, 7, 5, 4]) * np.pi / 4

    # Create constellation points
    constellation = np.exp(1j * angles)

    # Map each triplet to symbol index (binary to decimal)
    symbol_indices = bit_triplets[:, 0] * 4 + bit_triplets[:, 1] * 2 + bit_triplets[:, 2]

    # Get corresponding symbols
    symbols = constellation[symbol_indices]

    return symbols


def qam16_modulation(bits):

    # Check if number of bits is multiple of 4
    if len(bits) % 4 != 0:
        raise ValueError("Number of bits must be multiple of 4 for 16-QAM")

    # Reshape bits into groups of 4
    bit_groups = bits.reshape(-1, 4)

    # Split into I and Q bits
    i_bits = bit_groups[:, 0:2]  # First 2 bits for I
    q_bits = bit_groups[:, 2:4]  # Last 2 bits for Q

    # Mapping for 2 bits to PAM-4 levels: {-3, -1, +1, +3}
    pam4_map = {
        (0, 0): -3,
        (0, 1): -1,
        (1, 1): +1,
        (1, 0): +3
    }

    # Map I and Q components
    i_components = np.array([pam4_map[tuple(pair)] for pair in i_bits])
    q_components = np.array([pam4_map[tuple(pair)] for pair in q_bits])

    # Create complex symbols
    symbols = i_components + 1j * q_components

    # Normalize to unit average energy
    # Average energy of unnormalized 16-QAM: E[|s|^2] = 10
    # Normalization factor: 1/sqrt(10)
    norm = 1 / np.sqrt(10)
    symbols = symbols * norm

    return symbols


if __name__ == "__main__":
    print("=" * 60)
    print("Testing All Modulation Schemes")
    print("=" * 60)

    # Test 1: BPSK
    print("\n1. BPSK Modulation")
    print("-" * 60)
    bpsk_bits = np.array([0, 1, 0, 1])
    bpsk_symbols = bpsk_modulation(bpsk_bits)
    print(f"Bits (4):    {bpsk_bits}")
    print(f"Symbols (4): {bpsk_symbols}")
    print(f"Energy: {np.mean(np.abs(bpsk_symbols) ** 2):.6f} (should be ~1.0)")

    # Test 2: QPSK
    print("\n2. QPSK Modulation")
    print("-" * 60)
    qpsk_bits = np.array([0, 0, 0, 1, 1, 1, 1, 0])
    qpsk_symbols = qpsk_modulation(qpsk_bits)
    print(f"Bits (8):    {qpsk_bits}")
    print(f"Symbols (4): {qpsk_symbols}")
    print(f"Energy: {np.mean(np.abs(qpsk_symbols) ** 2):.6f} (should be ~1.0)")

    # Test 3: 8-PSK
    print("\n3. 8-PSK Modulation")
    print("-" * 60)
    psk8_bits = np.array([0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1])
    psk8_symbols = psk8_modulation(psk8_bits)
    print(f"Bits (12):   {psk8_bits}")
    print(f"Symbols (4): {psk8_symbols}")
    print(f"Energy: {np.mean(np.abs(psk8_symbols) ** 2):.6f} (should be ~1.0)")

    #
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"BPSK:   1 bit/symbol  - 4 bits -> 4 symbols")
    print(f"QPSK:   2 bits/symbol - 8 bits -> 4 symbols")
    print(f"8-PSK:  3 bits/symbol - 12 bits -> 4 symbols")