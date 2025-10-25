"""
RESONANCE FIELD GENERATOR
Copyright (c) 2025 Americo Simoes. All Rights Reserved.

Generates temporal resonance fields at CTT-predicted frequencies.
Core mechanism for quantum state manipulation in temporal domain.
"""

import numpy as np
import math
from typing import List, Tuple, Optional
from ctt_constants import (
    ALPHA, OMEGA_PLUS, OMEGA_MINUS, PRIME_WINDOWS_S,
    TemporalFramework, framework_transition_energy
)

class ResonanceField:
    """
    Temporal resonance field generator.
    Creates standing waves at framework transition boundaries.
    """
    
    def __init__(self, dimension: int = 256):
        """
        Initialize resonance field.
        
        Args:
            dimension: Field dimension (power of 2 for FFT efficiency)
        """
        self.dimension = dimension
        self.field_state = np.zeros(dimension, dtype=complex)
        self.resonance_amplitude = 1.0
        self.phase_coherence = 1.0
        
        # Initialize at ground state with positive resonance
        self._initialize_ground_state()
    
    def _initialize_ground_state(self):
        """Initialize field at ω+ resonance frequency"""
        t = np.linspace(0, 2*np.pi, self.dimension)
        # Ground state: pure ω+ resonance with α-modulation
        self.field_state = np.exp(1j * OMEGA_PLUS * t) * (1 + ALPHA * np.cos(t))
        self._normalize()
    
    def _normalize(self):
        """Normalize field state to unit probability"""
        norm = np.sqrt(np.sum(np.abs(self.field_state)**2))
        if norm > 0:
            self.field_state /= norm
    
    def apply_resonance_pulse(self, frequency: float, duration: float, phase: float = 0.0):
        """
        Apply resonance pulse at specified frequency.
        
        Args:
            frequency: Resonance frequency in Hz
            duration: Pulse duration in seconds
            phase: Initial phase in radians
        """
        t = np.linspace(0, duration, self.dimension)
        
        # Resonance pulse with temporal dispersion modulation
        pulse = np.exp(1j * (2 * np.pi * frequency * t + phase))
        pulse *= (1 + ALPHA * np.sin(2 * np.pi * frequency * t))
        
        # Apply pulse to field state
        self.field_state *= pulse
        self._normalize()
    
    def create_superposition(self, omega1: float, omega2: float, ratio: float = 0.5):
        """
        Create superposition of two resonance frequencies.
        
        Args:
            omega1: First frequency (Hz)
            omega2: Second frequency (Hz)
            ratio: Amplitude ratio (0 to 1)
        """
        t = np.linspace(0, 2*np.pi, self.dimension)
        
        # Superposition with α-dependent coupling
        component1 = np.sqrt(ratio) * np.exp(1j * omega1 * t)
        component2 = np.sqrt(1 - ratio) * np.exp(1j * omega2 * t)
        
        # Add α-mediated cross-term
        cross_coupling = ALPHA * np.exp(1j * (omega1 + omega2) * t / 2)
        
        self.field_state = component1 + component2 + cross_coupling
        self._normalize()
    
    def entangle_with_prime_window(self, prime_index: int):
        """
        Entangle field with specific prime resonance window.
        
        Args:
            prime_index: Index into PRIME_WINDOWS_S array
        """
        if prime_index >= len(PRIME_WINDOWS_S):
            raise ValueError(f"Prime index {prime_index} out of range")
        
        t_prime = PRIME_WINDOWS_S[prime_index]
        
        # Create entanglement through temporal phase lock
        t = np.linspace(0, t_prime, self.dimension)
        phase_lock = np.exp(1j * OMEGA_PLUS * t / t_prime)
        
        # Apply α-dependent entanglement strength
        entanglement_strength = 1 + ALPHA * np.cos(2 * np.pi * t / t_prime)
        
        self.field_state *= phase_lock * entanglement_strength
        self._normalize()
    
    def framework_transition(self, direction: str = "temporal"):
        """
        Cross framework transition boundary.
        
        Args:
            direction: "temporal" (spatial→temporal) or "spatial" (temporal→spatial)
        """
        if direction == "temporal":
            # Spatial to temporal: contract wavelength by α
            self.field_state = np.fft.fft(self.field_state)
            scale = 1 - ALPHA
            self.field_state *= scale
            self.field_state = np.fft.ifft(self.field_state)
        else:
            # Temporal to spatial: expand wavelength by α
            self.field_state = np.fft.fft(self.field_state)
            scale = 1 + ALPHA
            self.field_state *= scale
            self.field_state = np.fft.ifft(self.field_state)
        
        self._normalize()
    
    def measure_resonance_spectrum(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Measure frequency spectrum of current field state.
        
        Returns:
            frequencies: Array of frequencies
            amplitudes: Corresponding amplitudes
        """
        spectrum = np.fft.fft(self.field_state)
        frequencies = np.fft.fftfreq(self.dimension, d=1.0/self.dimension)
        amplitudes = np.abs(spectrum)
        
        return frequencies, amplitudes
    
    def detect_prime_resonances(self) -> List[Tuple[float, float]]:
        """
        Detect resonances at prime microsecond windows.
        
        Returns:
            List of (window_time, resonance_strength) tuples
        """
        frequencies, amplitudes = self.measure_resonance_spectrum()
        
        resonances = []
        for prime_us in PRIME_WINDOWS_S:
            # Find nearest frequency bin
            target_freq = 1.0 / prime_us
            idx = np.argmin(np.abs(frequencies - target_freq))
            strength = amplitudes[idx]
            
            resonances.append((prime_us * 1e6, float(strength)))
        
        return resonances
    
    def calculate_coherence(self) -> float:
        """
        Calculate field coherence (0 to 1).
        1.0 = perfect coherence, 0.0 = completely decoherent
        """
        # Coherence = purity of density matrix
        rho = np.outer(self.field_state, np.conj(self.field_state))
        purity = np.real(np.trace(rho @ rho))
        
        # Normalize to [0, 1] range
        max_purity = 1.0
        min_purity = 1.0 / self.dimension
        
        coherence = (purity - min_purity) / (max_purity - min_purity)
        self.phase_coherence = coherence
        
        return coherence
    
    def apply_temporal_gate(self, gate_type: str, target_freq: Optional[float] = None):
        """
        Apply temporal quantum gate.
        
        Args:
            gate_type: "hadamard", "phase", "pi_rotation", "alpha_shift"
            target_freq: Target frequency for frequency-selective gates
        """
        if gate_type == "hadamard":
            # Temporal Hadamard: superposition of ω+ and ω-
            self.create_superposition(OMEGA_PLUS, OMEGA_MINUS, 0.5)
        
        elif gate_type == "phase":
            # Phase gate: α-dependent phase shift
            phase_shift = ALPHA * np.pi
            self.field_state *= np.exp(1j * phase_shift)
        
        elif gate_type == "pi_rotation":
            # π rotation in temporal domain
            t = np.linspace(0, np.pi / OMEGA_PLUS, self.dimension)
            rotation = np.exp(1j * TemporalFramework.PI * OMEGA_PLUS * t)
            self.field_state *= rotation
            self._normalize()
        
        elif gate_type == "alpha_shift":
            # α-shift: unique to temporal framework
            self.framework_transition("temporal")
            self.apply_resonance_pulse(OMEGA_PLUS, ALPHA / OMEGA_PLUS)
            self.framework_transition("spatial")
        
        else:
            raise ValueError(f"Unknown gate type: {gate_type}")
    
    def couple_to_field(self, other: 'ResonanceField', coupling_strength: float = ALPHA):
        """
        Couple this field to another resonance field.
        
        Args:
            other: Another ResonanceField instance
            coupling_strength: Coupling strength (default: α)
        """
        if other.dimension != self.dimension:
            raise ValueError("Fields must have same dimension for coupling")
        
        # Create entangled state through temporal coupling
        coupled_state = (self.field_state + coupling_strength * other.field_state) / np.sqrt(1 + coupling_strength**2)
        
        self.field_state = coupled_state
        self._normalize()
    
    def get_state_vector(self) -> np.ndarray:
        """Return current field state vector"""
        return self.field_state.copy()
    
    def set_state_vector(self, state: np.ndarray):
        """Set field state vector"""
        if len(state) != self.dimension:
            raise ValueError(f"State vector must have dimension {self.dimension}")
        
        self.field_state = state.copy()
        self._normalize()
    
    def calculate_framework_overlap(self) -> float:
        """
        Calculate overlap with pure framework transition state.
        Returns measure of how close field is to transition boundary.
        """
        # Pure transition state: equal superposition at ω+ and ω-
        pure_transition = np.zeros(self.dimension, dtype=complex)
        t = np.linspace(0, 2*np.pi, self.dimension)
        
        pure_transition = (np.exp(1j * OMEGA_PLUS * t) + np.exp(1j * OMEGA_MINUS * t)) / np.sqrt(2)
        pure_transition /= np.sqrt(np.sum(np.abs(pure_transition)**2))
        
        # Calculate overlap
        overlap = np.abs(np.vdot(pure_transition, self.field_state))**2
        
        return overlap
    
    def __repr__(self):
        coherence = self.calculate_coherence()
        overlap = self.calculate_framework_overlap()
        
        return (f"ResonanceField(dim={self.dimension}, "
                f"coherence={coherence:.4f}, "
                f"framework_overlap={overlap:.4f})")


if __name__ == "__main__":
    print("=" * 70)
    print("RESONANCE FIELD GENERATOR - TEST")
    print("=" * 70)
    
    # Create resonance field
    field = ResonanceField(dimension=512)
    print(f"\nInitialized: {field}")
    
    # Test Hadamard gate
    print("\nApplying temporal Hadamard gate...")
    field.apply_temporal_gate("hadamard")
    print(f"After Hadamard: {field}")
    
    # Test prime window entanglement
    print("\nEntangling with prime window 0 (10007 μs)...")
    field.entangle_with_prime_window(0)
    print(f"After entanglement: {field}")
    
    # Detect prime resonances
    print("\nDetecting prime resonances:")
    resonances = field.detect_prime_resonances()
    for prime_us, strength in resonances[:4]:
        print(f"  {prime_us:.0f} μs: strength = {strength:.6f}")
    
    # Test framework transition
    print("\nCrossing framework boundary to temporal domain...")
    field.framework_transition("temporal")
    print(f"In temporal domain: {field}")
    
    print("\n" + "=" * 70)
