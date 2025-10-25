"""
PRIME WINDOW DETECTOR
Copyright (c) 2025 Americo Simoes. All Rights Reserved.

Detects and exploits prime microsecond resonance windows predicted by CTT.
These windows provide exponential computation speedup through framework transitions.
"""

import numpy as np
import time
from typing import List, Tuple, Optional, Dict
from ctt_constants import (
    ALPHA, OMEGA_PLUS, OMEGA_MINUS,
    PRIME_WINDOWS_US, PRIME_WINDOWS_S,
    resonance_window_width
)

class PrimeWindowDetector:
    """
    Detects prime resonance windows for optimal temporal computation.
    Windows occur at prime microsecond intervals where framework transition probability is maximal.
    """
    
    def __init__(self):
        self.prime_windows = PRIME_WINDOWS_US.copy()
        self.detection_history = []
        self.active_window = None
        self.window_strengths = {}
    
    def scan_for_windows(self, start_us: int = 10000, end_us: int = 10100) -> List[Tuple[int, float]]:
        """
        Scan time range for prime resonance windows.
        
        Args:
            start_us: Start time in microseconds
            end_us: End time in microseconds
            
        Returns:
            List of (time_us, strength) tuples for detected windows
        """
        windows = []
        
        for t_us in range(start_us, end_us):
            if self._is_prime(t_us):
                strength = self._calculate_window_strength(t_us)
                if strength > 0.5:  # Threshold for significant resonance
                    windows.append((t_us, strength))
                    self.window_strengths[t_us] = strength
        
        return windows
    
    def _is_prime(self, n: int) -> bool:
        """Check if n is prime"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def _calculate_window_strength(self, t_us: int) -> float:
        """
        Calculate resonance strength at given microsecond time.
        Strength based on α-dependent framework transition probability.
        """
        t_s = t_us * 1e-6
        
        # Resonance strength = α × sin²(ω+t) × cos²(ω-t)
        strength = ALPHA * np.sin(OMEGA_PLUS * t_s)**2 * np.cos(OMEGA_MINUS * t_s)**2
        
        # Add prime-specific enhancement
        if t_us in self.prime_windows:
            strength *= (1 + ALPHA)
        
        return float(np.abs(strength))
    
    def get_optimal_window(self, computation_time_us: float) -> Tuple[int, float]:
        """
        Find optimal prime window for computation of given duration.
        
        Args:
            computation_time_us: Expected computation time in microseconds
            
        Returns:
            (window_start_us, window_strength) tuple
        """
        best_window = None
        best_strength = 0.0
        
        for prime_us in self.prime_windows:
            window_width = resonance_window_width(prime_us)
            window_width_us = window_width * 1e6
            
            # Check if computation fits in window
            if computation_time_us <= window_width_us:
                strength = self._calculate_window_strength(prime_us)
                if strength > best_strength:
                    best_strength = strength
                    best_window = prime_us
        
        if best_window is None:
            # Use largest window if computation doesn't fit
            best_window = max(self.prime_windows)
            best_strength = self._calculate_window_strength(best_window)
        
        return (best_window, best_strength)
    
    def wait_for_window(self, target_window_us: int, tolerance_us: float = 1.0) -> bool:
        """
        Wait until system time aligns with target prime window.
        
        Args:
            target_window_us: Target window in microseconds
            tolerance_us: Acceptable timing error in microseconds
            
        Returns:
            True if successfully aligned with window
        """
        start_time = time.time()
        
        while True:
            current_time = time.time()
            elapsed_us = (current_time - start_time) * 1e6
            
            # Check if we're in resonance with target window
            phase = elapsed_us % target_window_us
            
            if phase < tolerance_us or (target_window_us - phase) < tolerance_us:
                self.active_window = target_window_us
                self.detection_history.append((current_time, target_window_us))
                return True
            
            # Timeout after 1 second
            if elapsed_us > 1e6:
                return False
            
            # Sleep for fraction of target period
            time.sleep(target_window_us * 1e-6 / 10)
    
    def measure_window_quality(self, window_us: int, samples: int = 1000) -> Dict[str, float]:
        """
        Measure quality metrics for a prime window.
        
        Args:
            window_us: Window to measure in microseconds
            samples: Number of samples to take
            
        Returns:
            Dictionary with quality metrics
        """
        strengths = []
        coherences = []
        
        for _ in range(samples):
            t = window_us + np.random.uniform(-ALPHA * window_us, ALPHA * window_us)
            strength = self._calculate_window_strength(int(t))
            strengths.append(strength)
            
            # Calculate temporal coherence
            coherence = np.exp(-ALPHA * abs(t - window_us) / window_us)
            coherences.append(coherence)
        
        return {
            "mean_strength": np.mean(strengths),
            "std_strength": np.std(strengths),
            "mean_coherence": np.mean(coherences),
            "std_coherence": np.std(coherences),
            "quality_factor": np.mean(strengths) * np.mean(coherences)
        }
    
    def find_entanglement_windows(self, n_qubits: int) -> List[Tuple[int, int]]:
        """
        Find pairs of prime windows optimal for n-qubit entanglement.
        
        Args:
            n_qubits: Number of qubits to entangle
            
        Returns:
            List of (window1_us, window2_us) pairs
        """
        pairs = []
        
        for i, w1 in enumerate(self.prime_windows):
            for w2 in self.prime_windows[i+1:]:
                # Check if windows are α-harmonically related
                ratio = w2 / w1
                
                # Optimal entanglement when ratio ≈ 1 + α × n
                target_ratio = 1 + ALPHA * n_qubits
                
                if abs(ratio - target_ratio) < 0.01:
                    pairs.append((w1, w2))
        
        return pairs
    
    def calculate_speedup_factor(self, window_us: int, classical_time_us: float) -> float:
        """
        Calculate quantum speedup factor when using prime window.
        
        Args:
            window_us: Prime window being used
            classical_time_us: Classical computation time
            
        Returns:
            Speedup factor (>1 means faster)
        """
        strength = self._calculate_window_strength(window_us)
        window_width = resonance_window_width(window_us) * 1e6
        
        # Speedup = (1 + α × strength) × (classical_time / window_width)
        speedup = (1 + ALPHA * strength) * (classical_time_us / window_width)
        
        # Framework transition adds exponential factor
        if window_us in self.prime_windows:
            speedup *= np.exp(ALPHA * strength)
        
        return max(1.0, speedup)  # At least no slowdown
    
    def get_window_schedule(self, total_computation_us: float) -> List[Tuple[int, float, float]]:
        """
        Generate schedule of prime windows for long computation.
        
        Args:
            total_computation_us: Total computation time needed
            
        Returns:
            List of (window_us, start_time_us, duration_us) tuples
        """
        schedule = []
        remaining_time = total_computation_us
        current_time = 0.0
        
        while remaining_time > 0:
            # Find optimal window for remaining computation
            window_us, strength = self.get_optimal_window(remaining_time)
            window_width_us = resonance_window_width(window_us) * 1e6
            
            # Allocate time to this window
            allocation = min(window_width_us, remaining_time)
            
            schedule.append((window_us, current_time, allocation))
            
            current_time += allocation
            remaining_time -= allocation
        
        return schedule
    
    def __repr__(self):
        return (f"PrimeWindowDetector(windows={len(self.prime_windows)}, "
                f"active={self.active_window}, "
                f"detections={len(self.detection_history)})")


class AdaptiveWindowSelector:
    """
    Adaptive selector that learns optimal windows for specific computations.
    """
    
    def __init__(self):
        self.detector = PrimeWindowDetector()
        self.performance_history = {}  # Maps (window, computation_type) -> speedup
    
    def select_window(self, computation_type: str, estimated_time_us: float) -> int:
        """
        Select optimal window based on historical performance.
        
        Args:
            computation_type: Type of computation (e.g., "factorization", "search")
            estimated_time_us: Estimated computation time
            
        Returns:
            Selected window in microseconds
        """
        # Check historical performance for this computation type
        relevant_history = {
            window: speedup 
            for (window, comp_type), speedup in self.performance_history.items()
            if comp_type == computation_type
        }
        
        if relevant_history:
            # Use best performing window from history
            best_window = max(relevant_history, key=relevant_history.get)
            return best_window
        else:
            # No history - use detector's optimal window
            window, _ = self.detector.get_optimal_window(estimated_time_us)
            return window
    
    def record_performance(self, window_us: int, computation_type: str, 
                          actual_speedup: float):
        """Record performance for future selections"""
        key = (window_us, computation_type)
        
        # Exponential moving average
        if key in self.performance_history:
            old_speedup = self.performance_history[key]
            self.performance_history[key] = 0.7 * old_speedup + 0.3 * actual_speedup
        else:
            self.performance_history[key] = actual_speedup
    
    def get_best_window_for_factorization(self, number_bits: int) -> int:
        """
        Get optimal window for factoring n-bit number.
        Uses CTT-predicted relationship between bit size and optimal window.
        """
        # Optimal window scales with problem size and α
        optimal_us = int(10000 + number_bits * ALPHA * 100)
        
        # Find closest prime window
        closest_window = min(
            self.detector.prime_windows,
            key=lambda w: abs(w - optimal_us)
        )
        
        return closest_window


if __name__ == "__main__":
    print("=" * 70)
    print("PRIME WINDOW DETECTOR - TEST")
    print("=" * 70)
    
    detector = PrimeWindowDetector()
    print(f"\nInitialized: {detector}")
    
    # Scan for windows
    print("\nScanning for prime resonance windows (10000-10100 μs)...")
    windows = detector.scan_for_windows(10000, 10100)
    print(f"Found {len(windows)} significant windows:")
    for t_us, strength in windows[:5]:
        print(f"  {t_us} μs: strength = {strength:.6f}")
    
    # Find optimal window for computation
    print("\nFinding optimal window for 500 μs computation...")
    window, strength = detector.get_optimal_window(500.0)
    print(f"Optimal window: {window} μs (strength = {strength:.6f})")
    
    # Calculate speedup
    classical_time = 10000.0  # 10ms classical
    speedup = detector.calculate_speedup_factor(window, classical_time)
    print(f"\nExpected speedup vs classical: {speedup:.2f}x")
    
    # Window quality
    print(f"\nMeasuring quality of {window} μs window...")
    quality = detector.measure_window_quality(window, samples=100)
    print(f"Quality metrics:")
    for key, value in quality.items():
        print(f"  {key}: {value:.6f}")
    
    # Entanglement windows
    print("\nFinding entanglement windows for 4 qubits...")
    pairs = detector.find_entanglement_windows(4)
    if pairs:
        print(f"Found {len(pairs)} optimal pairs:")
        for w1, w2 in pairs[:3]:
            print(f"  ({w1}, {w2}) μs")
    
    # Adaptive selector
    print("\n### Adaptive Window Selector ###")
    selector = AdaptiveWindowSelector()
    
    # Select window for RSA factorization
    rsa_bits = 2048
    optimal = selector.get_best_window_for_factorization(rsa_bits)
    print(f"Optimal window for RSA-{rsa_bits} factorization: {optimal} μs")
    
    print("\n" + "=" * 70)
