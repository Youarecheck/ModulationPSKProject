"""
Module for adding AWGN (Additive White Gaussian Noise) to signals.
Simulates noise in a communication channel.
"""

import numpy as np


def add_awgn_noise(symbols, eb_n0_db):
    """
    Add AWGN (Additive White Gaussian Noise) to modulated symbols.

    This function simulates the effect of noise in a communication channel.
    The noise level is controlled by Eb/N0 (Energy per bit to Noise ratio).

    Parameters
    ----------
    symbols : numpy.ndarray (complex)
        Modulated symbols from any modulation scheme
        (BPSK, QPSK, 8-PSK, QAM, etc.)
    eb_n0_db : float
        Energy per bit to noise power spectral density ratio in dB
        Higher values = less noise = better signal quality
        Typical range: -5 dB to 15 dB

    Returns
    -------
    numpy.ndarray (complex)
        Symbols with added AWGN noise

    Notes
    -----
    Technical details:
    - Assumes normalized energy per bit: Eb = 1.0
    - Generates complex Gaussian noise with independent I and Q components
    - Noise power is calculated as: N0 = Eb / (10^(Eb_N0_db/10))
    - Standard deviation: sigma = sqrt(N0/2) for each component

    The noise is complex: noise = noise_I + j*noise_Q
    Both components are independent Gaussian random variables.

    Examples
    --------
    >>> symbols = np.array([1.0, -1.0, 1.0], dtype=complex)
    >>> noisy = add_awgn_noise(symbols, eb_n0_db=10.0)
    >>> # Result will have added Gaussian noise
    >>> # Higher Eb/N0 = less noise = symbols closer to original
    """
    # Step 1: Convert Eb/N0 from dB to linear scale
    # dB formula: dB = 10 * log10(linear)
    # Inverse: linear = 10^(dB/10)
    eb_n0 = 10 ** (eb_n0_db / 10.0)

    # Step 2: Calculate noise power spectral density
    # Normalized energy per bit
    eb = 1.0
    # Noise power spectral density
    n0 = eb / eb_n0

    # Step 3: Calculate standard deviation for noise
    # For complex noise, divide N0 by 2 (half for I, half for Q)
    sigma = np.sqrt(n0 / 2)

    # Step 4: Get number of symbols
    n_symbols = symbols.shape[0]

    # Step 5: Generate independent Gaussian noise for I and Q components
    # I (In-phase) component
    noise_i = sigma * np.random.normal(0, 1, size=n_symbols)
    # Q (Quadrature) component
    noise_q = sigma * np.random.normal(0, 1, size=n_symbols)

    # Step 6: Create complex AWGN noise
    awgn_noise = noise_i + 1j * noise_q

    # Step 7: Add noise to symbols
    received_symbols = symbols + awgn_noise

    return received_symbols


if __name__ == "__main__":
    # This code runs ONLY when you execute this file directly
    print("=" * 60)
    print("Testing AWGN Noise Addition")
    print("=" * 60)

    # Test 1: BPSK symbols
    print("\nTest 1: Adding noise to BPSK symbols")
    test_symbols = np.array([1.0, -1.0, 1.0, -1.0, 1.0], dtype=complex)
    print(f"Original symbols:\n{test_symbols}")

    # Test with different noise levels
    for eb_n0_db in [0, 5, 10, 15]:
        noisy_symbols = add_awgn_noise(test_symbols, eb_n0_db)
        print(f"\nEb/N0 = {eb_n0_db} dB:")
        print(f"Noisy symbols: {noisy_symbols}")

        # Calculate actual noise added
        noise = noisy_symbols - test_symbols
        noise_power = np.mean(np.abs(noise) ** 2)
        print(f"Noise power: {noise_power:.6f}")

    # Test 2: Visual comparison
    print("\n" + "=" * 60)
    print("Test 2: High noise vs Low noise")
    print("=" * 60)

    clean_symbol = np.array([1.0 + 0.0j])

    print(f"\nOriginal symbol: {clean_symbol[0]}")

    # High noise (low Eb/N0)
    high_noise = add_awgn_noise(clean_symbol, eb_n0_db=0)
    print(f"With high noise (0 dB): {high_noise[0]}")

    # Low noise (high Eb/N0)
    low_noise = add_awgn_noise(clean_symbol, eb_n0_db=15)
    print(f"With low noise (15 dB): {low_noise[0]}")

    print("\nNote: Higher Eb/N0 = less noise = closer to original")