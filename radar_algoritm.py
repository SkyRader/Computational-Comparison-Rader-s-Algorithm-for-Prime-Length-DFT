import numpy as np

def is_prime(n):
    """Simple check to ensure N is prime."""
    if n < 2: return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def get_primitive_root(p):
    """Finds a primitive root modulo p (needed for Rader's index mapping)."""
    if p == 2: return 1
    phi = p - 1
    
    # Find all prime factors of phi
    factors = set()
    n = phi
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1: factors.add(n)
    
    # Test for a primitive root (g)
    for g in range(2, p):
        is_primitive = True
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                is_primitive = False
                break
        if is_primitive:
            return g
    return None # Should not happen for a prime p

def rader_fft(x):
    """
    Implements Rader's Algorithm for prime-length N DFT.
    Converts a prime-length N DFT into a circular convolution,
    which is then solved efficiently using two standard FFTs.
    """
    N = len(x)
    if not is_prime(N):
        raise ValueError("Rader's Algorithm only works for prime N.")

    # 0. Handle the trivial DC term X[0] and scaling of X[k]
    X0 = sum(x)
    
    if N == 1:
        return np.array([X0])
    
    # 1. Setup based on Number Theory
    p = N
    g = get_primitive_root(p)
    if g is None:
        raise RuntimeError("Could not find primitive root.")

    # Indices mapping: Generate powers and their inverses for the circular shift
    # Indices are mapped from [1, p-1]
    
    # y[i] is the signal x[g^i mod p]
    y = np.zeros(p - 1, dtype=complex)
    
    # h[i] is the DFT kernel e^(-j * 2pi * g^(-i) / p)
    h = np.zeros(p - 1, dtype=complex)
    
    # h_conv[i] is the DFT kernel for the convolution step, arranged
    h_conv = np.zeros(p - 1, dtype=complex) 

    # Generate the mapped sequences y and h_conv
    for i in range(p - 1):
        # Index k = g^i mod p
        k = pow(g, i, p)
        
        # y[i] = x[k]
        y[i] = x[k]
        
        # h_conv[i] = e^(-j * 2pi * k / p) -> This is the core kernel
        angle = -2 * np.pi * k / p
        h_conv[i] = np.exp(1j * angle)
    
    # Reverse h_conv to get the h sequence for circular convolution
    h = np.concatenate(([h_conv[0]], h_conv[1:][::-1]))
    
    # 2. Perform Circular Convolution using FFT/IFFT
    # Length for FFT is M = p-1. Since M is composite, we use standard FFT.
    
    # FFT of inputs
    FY = np.fft.fft(y)
    FH = np.fft.fft(h)
    
    # Convolution in frequency domain is multiplication
    FZ = FY * FH
    
    # IFFT back to get the convolution result z
    z = np.fft.ifft(FZ)
    
    # 3. Reconstruct the Final DFT Result X[k]
    
    X = np.zeros(p, dtype=complex)
    
    # X[0] is the DC term (calculated in step 0)
    X[0] = X0 
    
    # X[k] for k != 0 is found by adding the x[0] term to the convolution result z
    # The convolution result z is mapped back according to g^i mod p
    x0_offset = x[0] - x[0] # The x[0] is usually subtracted then added, but simplified here
    
    for i in range(p - 1):
        # Index k = g^i mod p
        k = pow(g, i, p)
        
        # X[k] = z[i] + x[0] - x[0]
        # X[k] = z[i] - x[0] + x[0]
        X[k] = z[i] + x[0] - z[0] # Simplified Rader's step
        
        
    return X

# --- Example Usage (Run this section to test the code) ---

if __name__ == '__main__':
    N_prime = 7
    fs = 100 
    freq = 5 
    
    # Generate the time-domain signal
    t = np.arange(N_prime) / fs
    x_time = np.sin(2 * np.pi * freq * t) + 1j * np.zeros(N_prime) # Real signal
    
    # 1. Brute-Force DFT (Accuracy Benchmark)
    X_brute = np.fft.fft(x_time) # NumPy's FFT is highly optimized and works as brute force for small N
    
    # 2. Rader's Algorithm 
    X_rader = rader_fft(x_time)
    
    print(f"--- N={N_prime} Signal Analysis ---")
    print(f"Max Difference between NumPy and Rader's: {np.max(np.abs(X_brute - X_rader)):.10f}")
    
    # Show the first few magnitude values
    print("\nMagnitude Comparison (First 4 Bins):")
    for k in range(4):
        print(f"  Bin {k}: Brute={np.abs(X_brute[k]):.6f} | Rader's={np.abs(X_rader[k]):.6f}")
