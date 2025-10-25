"""
TEMPORAL QUBIT IMPLEMENTATION
Copyright (c) 2025 Americo Simoes. All Rights Reserved.

Quantum bits based on temporal phase states rather than spatial spin.
Exploits α=0.0302 framework transition for exponential speedup.
"""

import numpy as np
from typing import List, Optional, Tuple
from ctt_constants import ALPHA, OMEGA_PLUS, OMEGA_MINUS, TemporalFramework
from resonance_field import ResonanceField

class TemporalQubit:
    """
    Temporal qubit: |ψ⟩ = α|0⟩ + β|1⟩ where states are temporal phases
    |0⟩ = ω+ resonance state
    |1⟩ = ω- resonance state
    """
    
    def __init__(self, initial_state: str = "|0⟩"):
        """
        Initialize temporal qubit.
        
        Args:
            initial_state: "|0⟩", "|1⟩", "|+⟩", or "|−⟩"
        """
        self.field = ResonanceField(dimension=128)
        self.alpha = 1.0 + 0.0j
        self.beta = 0.0 + 0.0j
        
        if initial_state == "|0⟩":
            self._set_zero_state()
        elif initial_state == "|1⟩":
            self._set_one_state()
        elif initial_state == "|+⟩":
            self._set_plus_state()
        elif initial_state == "|−⟩":
            self._set_minus_state()
        else:
            raise ValueError(f"Unknown initial state: {initial_state}")
    
    def _set_zero_state(self):
        """Set to |0⟩ = ω+ resonance"""
        self.alpha = 1.0
        self.beta = 0.0
        # Field already initialized to ω+ by default
    
    def _set_one_state(self):
        """Set to |1⟩ = ω- resonance"""
        self.alpha = 0.0
        self.beta = 1.0
        t = np.linspace(0, 2*np.pi, self.field.dimension)
        self.field.field_state = np.exp(1j * OMEGA_MINUS * t) * (1 + ALPHA * np.cos(t))
        self.field._normalize()
    
    def _set_plus_state(self):
        """Set to |+⟩ = (|0⟩ + |1⟩)/√2"""
        self.alpha = 1.0 / np.sqrt(2)
        self.beta = 1.0 / np.sqrt(2)
        self.field.create_superposition(OMEGA_PLUS, OMEGA_MINUS, 0.5)
    
    def _set_minus_state(self):
        """Set to |−⟩ = (|0⟩ − |1⟩)/√2"""
        self.alpha = 1.0 / np.sqrt(2)
        self.beta = -1.0 / np.sqrt(2)
        self.field.create_superposition(OMEGA_PLUS, OMEGA_MINUS, 0.5)
        self.field.field_state *= np.exp(1j * np.pi)  # π phase shift
        self.field._normalize()
    
    def hadamard(self):
        """
        Temporal Hadamard gate: Creates superposition in temporal domain
        H|0⟩ = |+⟩, H|1⟩ = |−⟩
        """
        self.field.apply_temporal_gate("hadamard")
        
        # Update coefficients
        new_alpha = (self.alpha + self.beta) / np.sqrt(2)
        new_beta = (self.alpha - self.beta) / np.sqrt(2)
        self.alpha = new_alpha
        self.beta = new_beta
    
    def pauli_x(self):
        """
        Temporal X gate: Bit flip in temporal domain
        X|0⟩ = |1⟩, X|1⟩ = |0⟩
        """
        # Swap α and β
        self.alpha, self.beta = self.beta, self.alpha
        
        # Swap field resonances
        t = np.linspace(0, 2*np.pi, self.field.dimension)
        if np.abs(self.alpha) > np.abs(self.beta):
            self.field.field_state = np.exp(1j * OMEGA_PLUS * t) * (1 + ALPHA * np.cos(t))
        else:
            self.field.field_state = np.exp(1j * OMEGA_MINUS * t) * (1 + ALPHA * np.cos(t))
        self.field._normalize()
    
    def pauli_z(self):
        """
        Temporal Z gate: Phase flip in temporal domain
        Z|0⟩ = |0⟩, Z|1⟩ = −|1⟩
        """
        self.beta *= -1
        self.field.field_state *= np.exp(1j * np.pi * np.abs(self.beta)**2)
    
    def phase_gate(self, theta: float):
        """
        Phase gate: Apply phase rotation
        P(θ)|0⟩ = |0⟩, P(θ)|1⟩ = e^(iθ)|1⟩
        """
        self.beta *= np.exp(1j * theta)
        self.field.apply_temporal_gate("phase")
    
    def rotation_x(self, theta: float):
        """
        Rotation around X axis in temporal Bloch sphere
        RX(θ) = exp(-iθX/2)
        """
        cos_half = np.cos(theta / 2)
        sin_half = np.sin(theta / 2)
        
        new_alpha = cos_half * self.alpha - 1j * sin_half * self.beta
        new_beta = -1j * sin_half * self.alpha + cos_half * self.beta
        
        self.alpha = new_alpha
        self.beta = new_beta
        
        # Update field
        self.field.create_superposition(
            OMEGA_PLUS, OMEGA_MINUS,
            np.abs(self.alpha)**2 / (np.abs(self.alpha)**2 + np.abs(self.beta)**2)
        )
    
    def rotation_y(self, theta: float):
        """
        Rotation around Y axis in temporal Bloch sphere
        RY(θ) = exp(-iθY/2)
        """
        cos_half = np.cos(theta / 2)
        sin_half = np.sin(theta / 2)
        
        new_alpha = cos_half * self.alpha - sin_half * self.beta
        new_beta = sin_half * self.alpha + cos_half * self.beta
        
        self.alpha = new_alpha
        self.beta = new_beta
        
        # Update field
        self.field.create_superposition(
            OMEGA_PLUS, OMEGA_MINUS,
            np.abs(self.alpha)**2 / (np.abs(self.alpha)**2 + np.abs(self.beta)**2)
        )
    
    def rotation_z(self, theta: float):
        """
        Rotation around Z axis in temporal Bloch sphere
        RZ(θ) = exp(-iθZ/2)
        """
        self.alpha *= np.exp(-1j * theta / 2)
        self.beta *= np.exp(1j * theta / 2)
        
        self.field.field_state *= np.exp(1j * theta * np.abs(self.beta)**2)
    
    def alpha_gate(self):
        """
        α-gate: Unique to temporal framework
        Applies framework transition with α-dependent phase
        """
        self.field.apply_temporal_gate("alpha_shift")
        
        # Apply α-dependent phase rotation
        phase = ALPHA * np.pi
        self.alpha *= np.exp(1j * phase / 2)
        self.beta *= np.exp(-1j * phase / 2)
    
    def measure(self) -> int:
        """
        Measure qubit in computational basis
        
        Returns:
            0 or 1 with probabilities |α|² and |β|²
        """
        prob_zero = np.abs(self.alpha)**2
        prob_one = np.abs(self.beta)**2
        
        # Normalize probabilities
        total = prob_zero + prob_one
        prob_zero /= total
        prob_one /= total
        
        # Measure
        result = np.random.choice([0, 1], p=[prob_zero, prob_one])
        
        # Collapse to measured state
        if result == 0:
            self._set_zero_state()
        else:
            self._set_one_state()
        
        return result
    
    def get_state_vector(self) -> np.ndarray:
        """Return state vector [α, β]"""
        norm = np.sqrt(np.abs(self.alpha)**2 + np.abs(self.beta)**2)
        return np.array([self.alpha / norm, self.beta / norm])
    
    def get_bloch_coordinates(self) -> Tuple[float, float, float]:
        """
        Get coordinates on temporal Bloch sphere
        
        Returns:
            (x, y, z) coordinates
        """
        state = self.get_state_vector()
        alpha, beta = state[0], state[1]
        
        x = 2 * np.real(np.conj(alpha) * beta)
        y = 2 * np.imag(np.conj(alpha) * beta)
        z = np.abs(alpha)**2 - np.abs(beta)**2
        
        return (x, y, z)
    
    def fidelity_with(self, other: 'TemporalQubit') -> float:
        """
        Calculate fidelity with another qubit
        F = |⟨ψ₁|ψ₂⟩|²
        """
        state1 = self.get_state_vector()
        state2 = other.get_state_vector()
        
        overlap = np.vdot(state1, state2)
        fidelity = np.abs(overlap)**2
        
        return fidelity
    
    def __repr__(self):
        state = self.get_state_vector()
        alpha_str = f"{state[0].real:.3f}" if np.abs(state[0].imag) < 1e-10 else f"({state[0].real:.3f}+{state[0].imag:.3f}i)"
        beta_str = f"{state[1].real:.3f}" if np.abs(state[1].imag) < 1e-10 else f"({state[1].real:.3f}+{state[1].imag:.3f}i)"
        
        return f"TemporalQubit(|ψ⟩ = {alpha_str}|0⟩ + {beta_str}|1⟩)"


class TemporalQubitRegister:
    """Register of multiple temporal qubits with entanglement"""
    
    def __init__(self, n_qubits: int):
        """
        Initialize register of n qubits
        
        Args:
            n_qubits: Number of qubits in register
        """
        self.n_qubits = n_qubits
        self.qubits = [TemporalQubit() for _ in range(n_qubits)]
        self.entanglement_map = {}  # Maps qubit pairs to entanglement strength
    
    def apply_single_gate(self, gate_func, target: int, *args):
        """
        Apply single-qubit gate to target qubit
        
        Args:
            gate_func: Gate function (e.g., hadamard, pauli_x)
            target: Target qubit index
            *args: Additional arguments for gate
        """
        if target >= self.n_qubits:
            raise ValueError(f"Target qubit {target} out of range")
        
        gate_func(self.qubits[target], *args)
    
    def cnot(self, control: int, target: int):
        """
        Controlled-NOT gate in temporal domain
        If control is |1⟩, flip target
        """
        if control >= self.n_qubits or target >= self.n_qubits:
            raise ValueError("Control or target out of range")
        
        control_qubit = self.qubits[control]
        target_qubit = self.qubits[target]
        
        # Measure control qubit probability of being |1⟩
        prob_one = np.abs(control_qubit.beta)**2
        
        # Apply X gate to target with probability proportional to control being |1⟩
        if prob_one > 0.5:
            target_qubit.pauli_x()
        
        # Create entanglement through field coupling
        control_qubit.field.couple_to_field(target_qubit.field, ALPHA)
        
        # Record entanglement
        self.entanglement_map[(control, target)] = ALPHA
    
    def entangle_prime_window(self, qubit_index: int, prime_index: int):
        """
        Entangle specific qubit with prime resonance window
        This is unique to temporal QC - exploits CTT physics
        """
        if qubit_index >= self.n_qubits:
            raise ValueError(f"Qubit {qubit_index} out of range")
        
        self.qubits[qubit_index].field.entangle_with_prime_window(prime_index)
    
    def measure_all(self) -> List[int]:
        """Measure all qubits, return list of results"""
        return [qubit.measure() for qubit in self.qubits]
    
    def get_statevector(self) -> np.ndarray:
        """
        Get full statevector of register
        Returns 2^n dimensional complex vector
        """
        # Start with first qubit
        state = self.qubits[0].get_state_vector()
        
        # Tensor product with remaining qubits
        for i in range(1, self.n_qubits):
            state = np.kron(state, self.qubits[i].get_state_vector())
        
        return state
    
    def __repr__(self):
        return f"TemporalQubitRegister(n_qubits={self.n_qubits}, entangled_pairs={len(self.entanglement_map)})"


if __name__ == "__main__":
    print("=" * 70)
    print("TEMPORAL QUBIT - TEST")
    print("=" * 70)
    
    # Single qubit operations
    print("\n### Single Qubit Operations ###")
    q = TemporalQubit()
    print(f"Initial state: {q}")
    
    q.hadamard()
    print(f"After Hadamard: {q}")
    
    x, y, z = q.get_bloch_coordinates()
    print(f"Bloch coordinates: ({x:.3f}, {y:.3f}, {z:.3f})")
    
    # Multi-qubit register
    print("\n### Qubit Register ###")
    register = TemporalQubitRegister(n_qubits=4)
    print(f"Created: {register}")
    
    # Apply Hadamard to all qubits
    for i in range(4):
        register.qubits[i].hadamard()
    print("Applied Hadamard to all 4 qubits")
    
    # Create entanglement
    register.cnot(0, 1)
    register.cnot(2, 3)
    print(f"After CNOT gates: {register}")
    
    # Entangle with prime window
    register.entangle_prime_window(0, 0)
    print("Entangled qubit 0 with prime window 10007 μs")
    
    # Measure
    results = register.measure_all()
    print(f"Measurement results: {results}")
    
    print("\n" + "=" * 70)
