from GetBytes import gen_bites
import os
from pathlib import Path
import matplotlib.pyplot as plt
from Modulator import *
from Demodulator import *
from AddAWGNNoise import *
import matplotlib.pyplot as plt
from TransmissionChannel import *



def get_results_path():
    script_dir = Path(__file__).parent.resolve()
    if script_dir.name == 'src':
        results_dir = script_dir.parent / 'results'
    else:
        results_dir = script_dir / 'results'

    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir


def calculate_ber(original_bits, decoded_bits):
    """Calculate Bit Error Rate."""
    errors = np.sum(original_bits != decoded_bits)
    ber = errors / len(original_bits)
    return ber


def simulate_bpsk(eb_n0_range, n_bits=100000):
    ber_Values = []

    print("Simulating BPSK...")
    print("-" * 60)

    for eb_n0_db in eb_n0_range:
       # bits =gen_bites(n_bits) ORGINAL VERSION FOR RANDOM BITES
        bits = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0])


        symbols = bpsk_modulation(bits)
        received_symbols = transmission_channel(symbols, eb_n0_db)
        decoded_bits = bpsk_demodulation(received_symbols)
        ber = calculate_ber(bits, decoded_bits)
        ber_Values.append(ber)
        print(f"Eb/N0 = {eb_n0_db:2d} dB  =>  BER = {ber:.6f}")
    return ber_Values


def simulate_qpsk(eb_n0_range, n_bits=10000):
    """Simulate QPSK transmission."""
    ber_values = []

    # Ensure even number of bits
    if n_bits % 2 != 0:
        n_bits += 1

    print("QPSK Simulation:")
    print("-" * 60)

    for eb_n0_db in eb_n0_range:
        #bits = gen_bites(n_bits) ORGINAL VERSION FOR RANDOM BITES
        bits = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0])
        symbols = qpsk_modulation(bits)
        received_symbols = transmission_channel(symbols, eb_n0_db)
        decoded_bits = qpsk_demodulation(received_symbols)
        ber = calculate_ber(bits, decoded_bits)
        ber_values.append(ber)
        print(f"Eb/N0 = {eb_n0_db:2d} dB  =>  BER = {ber:.6f}")

    return ber_values

def main():

    ## bits = gen_bites(10)
    ##print("orginal Bits: ")
    ##print(bits)
    ##demodulated_bits = bpsk_demodulation(add_awgn_noise(bpsk_modulation(bits),0.5))
    ##print("demodulated Bits: ")
    ##print(demodulated_bits)
    ##print("Bit Error Rate: ")
   # print(bites == demodulated_bites)
    ##print(calculate_ber(bits, demodulated_bits))
    #plt.plot(bites, demodulated_bites)
    #plt.show()


##simulation parameters
    eb_n0_range = range(-2, 16)  # -2 dB to 15 dB
    n_bits = 11

    print("Simulation Parameters:")
    print(f"  - Modulations: BPSK, QPSK")
    print(f"  - Number of bits: {n_bits}")
    print(f"  - Eb/N0 range: {list(eb_n0_range)} dB")
    print()



    # Run simulations
    print("=" * 70)
    print("Running Simulations...")
    print("=" * 70)
    print()

    print("[1/4] BPSK")
    ber_bpsk = simulate_bpsk(eb_n0_range, n_bits)
    print()

    print("[2/4] QPSK")
    ber_qpsk = simulate_qpsk(eb_n0_range, n_bits)
    print()



if __name__ == "__main__":
    main()