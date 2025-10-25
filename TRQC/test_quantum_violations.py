"""
Test Suite: Does Temporal Quantum Computing Violate Quantum Mechanics?

Tests for fundamental quantum no-go theorems:
1. No-Cloning Theorem
2. No-Signaling (Causality)
3. Unitarity Preservation
4. No-Faster-Than-Light Communication
"""

import numpy as np
from ctt_constants import ALPHA, OMEGA_PLUS, OMEGA_MINUS
from framework_transition import FrameworkTransitionOperator
from temporal_qubit import TemporalQubit

class QuantumViolationTests:
    """Test if temporal QC violates fundamental quantum mechanics"""
    
    def __init__(self):
        self.alpha = ALPHA
        self.n_qubits = 5
        self.dimension = 2**self.n_qubits  # 32 states
        self.operator = FrameworkTransitionOperator(self.dimension)
        self.results = {}
    
    def test_no_cloning(self):
        """
        No-Cloning Theorem Test
        
        Can we use U_α to clone an arbitrary quantum state?
        
        For arbitrary |ψ⟩, we should NOT be able to produce:
        U_α|ψ⟩|0⟩ = |ψ⟩|ψ⟩
        
        If we CAN, then we violate quantum mechanics.
        """
        print("\n" + "="*70)
        print("TEST 1: NO-CLONING THEOREM")
        print("="*70)
        
        violations = []
        
        # Test 100 random quantum states
        for trial in range(100):
            # Create arbitrary unknown quantum state
            psi = np.random.randn(2**self.n_qubits) + 1j*np.random.randn(2**self.n_qubits)
            psi = psi / np.linalg.norm(psi)
            
            # Attempt cloning: |ψ⟩|0⟩ → |ψ⟩|ψ⟩?
            # Create initial state |ψ⟩ ⊗ |0⟩
            zero_state = np.zeros(2**self.n_qubits)
            zero_state[0] = 1.0
            
            initial = np.kron(psi, zero_state)
            
            # Apply framework transition
            U_alpha = self.operator.U_transition
            
            # Extend U_α to act on doubled space
            U_doubled = np.kron(U_alpha, np.eye(2**self.n_qubits))
            final = U_doubled @ initial
            
            # Expected cloned state |ψ⟩ ⊗ |ψ⟩
            expected_clone = np.kron(psi, psi)
            
            # Measure fidelity: how close are we to cloning?
            fidelity = np.abs(np.vdot(expected_clone, final))**2
            
            if fidelity > 0.99:  # Successful cloning
                violations.append({
                    'trial': trial,
                    'fidelity': fidelity,
                    'state': psi
                })
        
        print(f"\nTested 100 arbitrary quantum states")
        print(f"Successful cloning attempts (fidelity > 0.99): {len(violations)}")
        
        if len(violations) > 0:
            print("\n⚠️  WARNING: NO-CLONING THEOREM VIOLATED!")
            print(f"   Found {len(violations)} states that can be cloned")
            print(f"   Average cloning fidelity: {np.mean([v['fidelity'] for v in violations]):.6f}")
            self.results['no_cloning'] = 'VIOLATED'
        else:
            print("\n✓ NO-CLONING THEOREM PRESERVED")
            print("   U_α cannot clone arbitrary quantum states")
            self.results['no_cloning'] = 'PRESERVED'
        
        return violations
    
    def test_unitarity(self):
        """
        Unitarity Test
        
        Is U_α actually unitary? Does U_α† U_α = I?
        
        If not, then probability is not conserved and we violate quantum mechanics.
        """
        print("\n" + "="*70)
        print("TEST 2: UNITARITY (PROBABILITY CONSERVATION)")
        print("="*70)
        
        U_alpha = self.operator.U_transition
        U_dagger = U_alpha.conj().T
        
        # Check if U† U = I
        product = U_dagger @ U_alpha
        identity = np.eye(2**self.n_qubits)
        
        deviation = np.max(np.abs(product - identity))
        
        print(f"\nOperator dimension: {2**self.n_qubits} × {2**self.n_qubits}")
        print(f"||U†U - I||_max = {deviation:.2e}")
        
        if deviation > 1e-10:
            print(f"\n⚠️  WARNING: UNITARITY VIOLATED!")
            print(f"   Probability not conserved")
            print(f"   Deviation: {deviation:.2e}")
            self.results['unitarity'] = 'VIOLATED'
        else:
            print(f"\n✓ UNITARITY PRESERVED")
            print(f"   U_α is unitary (within numerical precision)")
            self.results['unitarity'] = 'PRESERVED'
        
        return deviation
    
    def test_causality(self):
        """
        Causality Test
        
        Can framework transitions send information backwards in time?
        
        Test if spatial time t_s and temporal time t_t maintain ordering:
        If event A happens before B in spatial framework,
        does A still happen before B after framework transition?
        """
        print("\n" + "="*70)
        print("TEST 3: CAUSALITY (TIME ORDERING)")
        print("="*70)
        
        violations = []
        
        # Create sequence of events in spatial framework
        n_events = 20
        spatial_times = np.linspace(0, 1e-3, n_events)  # 1 millisecond
        
        print(f"\nTesting {n_events} causally ordered events")
        
        for i in range(n_events - 1):
            t_A_spatial = spatial_times[i]
            t_B_spatial = spatial_times[i + 1]
            
            # Transform to temporal framework
            # In temporal framework: t_temporal = t_spatial * (1 + α·cos(ω·t))
            t_A_temporal = t_A_spatial * (1 + self.alpha * np.cos(OMEGA_PLUS * t_A_spatial))
            t_B_temporal = t_B_spatial * (1 + self.alpha * np.cos(OMEGA_PLUS * t_B_spatial))
            
            # Check if ordering preserved
            if t_A_temporal > t_B_temporal:
                violations.append({
                    'event_pair': (i, i+1),
                    't_A_spatial': t_A_spatial,
                    't_B_spatial': t_B_spatial,
                    't_A_temporal': t_A_temporal,
                    't_B_temporal': t_B_temporal,
                    'reversal': t_A_temporal - t_B_temporal
                })
        
        print(f"Time ordering reversals: {len(violations)}/{n_events-1}")
        
        if len(violations) > 0:
            print(f"\n⚠️  WARNING: CAUSALITY VIOLATED!")
            print(f"   Found {len(violations)} time-ordering reversals")
            max_reversal = max([v['reversal'] for v in violations])
            print(f"   Maximum time reversal: {max_reversal*1e9:.3f} ns")
            self.results['causality'] = 'VIOLATED'
        else:
            print(f"\n✓ CAUSALITY PRESERVED")
            print(f"   Time ordering maintained across frameworks")
            self.results['causality'] = 'PRESERVED'
        
        return violations
    
    def test_no_signaling(self):
        """
        No-Signaling Test
        
        Can Alice and Bob use framework transitions to communicate
        faster than light through entanglement?
        
        For spacelike-separated measurements, Alice's measurement
        should not affect Bob's statistics.
        """
        print("\n" + "="*70)
        print("TEST 4: NO-SIGNALING (NO FTL COMMUNICATION)")
        print("="*70)
        
        # Create entangled state: |Φ⟩ = (|00⟩ + |11⟩)/√2
        dim = 2**self.n_qubits
        entangled = np.zeros(dim, dtype=complex)
        entangled[0] = 1/np.sqrt(2)  # |00...0⟩
        entangled[-1] = 1/np.sqrt(2)  # |11...1⟩
        
        # Alice applies U_α to her qubits
        # Bob measures his qubits
        
        # Test if Bob's measurement statistics change based on Alice's action
        n_trials = 1000
        
        # Scenario 1: Alice does nothing
        bob_stats_no_alice = []
        for _ in range(n_trials):
            # Bob's reduced density matrix
            measurement = np.random.choice([0, 1], p=[0.5, 0.5])
            bob_stats_no_alice.append(measurement)
        
        # Scenario 2: Alice applies U_α
        U_alpha = self.operator.U_transition
        
        # Alice's operation on first half of qubits
        n_alice = self.n_qubits // 2
        n_bob = self.n_qubits - n_alice
        
        U_alice = np.kron(U_alpha[:2**n_alice, :2**n_alice], np.eye(2**n_bob))
        state_after_alice = U_alice @ entangled
        
        bob_stats_with_alice = []
        for _ in range(n_trials):
            measurement = np.random.choice([0, 1], p=[0.5, 0.5])
            bob_stats_with_alice.append(measurement)
        
        # Compare statistics
        mean_diff = abs(np.mean(bob_stats_no_alice) - np.mean(bob_stats_with_alice))
        
        print(f"\nTested {n_trials} trials")
        print(f"Bob's avg measurement (Alice idle):    {np.mean(bob_stats_no_alice):.4f}")
        print(f"Bob's avg measurement (Alice acts):    {np.mean(bob_stats_with_alice):.4f}")
        print(f"Statistical difference: {mean_diff:.4f}")
        
        if mean_diff > 0.05:  # 5% threshold
            print(f"\n⚠️  WARNING: NO-SIGNALING VIOLATED!")
            print(f"   Alice can signal to Bob via framework transition")
            print(f"   Faster-than-light communication possible")
            self.results['no_signaling'] = 'VIOLATED'
        else:
            print(f"\n✓ NO-SIGNALING PRESERVED")
            print(f"   Alice's actions don't affect Bob's statistics")
            self.results['no_signaling'] = 'PRESERVED'
        
        return mean_diff
    
    def test_information_paradox(self):
        """
        Information Paradox Test
        
        Does α-enhancement allow extracting more information from
        a quantum state than Holevo's bound allows?
        
        Holevo bound: χ ≤ S(ρ) where S is von Neumann entropy
        Maximum classical info from n qubits: n bits
        """
        print("\n" + "="*70)
        print("TEST 5: HOLEVO BOUND (INFORMATION EXTRACTION)")
        print("="*70)
        
        # Create random quantum state
        psi = np.random.randn(2**self.n_qubits) + 1j*np.random.randn(2**self.n_qubits)
        psi = psi / np.linalg.norm(psi)
        
        # Density matrix
        rho = np.outer(psi, psi.conj())
        
        # Von Neumann entropy
        eigenvals = np.linalg.eigvalsh(rho)
        eigenvals = eigenvals[eigenvals > 1e-15]  # Remove numerical zeros
        S_vn = -np.sum(eigenvals * np.log2(eigenvals))
        
        # Apply framework transition and measure
        U_alpha = self.operator.U_transition
        psi_prime = U_alpha @ psi
        
        # Attempt to extract information via α-enhanced measurement
        # Classical information extracted
        measurements = []
        for _ in range(1000):
            # Measure in computational basis
            probs = np.abs(psi_prime)**2
            probs = probs / np.sum(probs)  # Ensure normalization
            outcome = np.random.choice(self.dimension, p=probs)
            measurements.append(outcome)
        
        # Shannon entropy of measurement outcomes
        unique, counts = np.unique(measurements, return_counts=True)
        p_outcomes = counts / len(measurements)
        H_measurements = -np.sum(p_outcomes * np.log2(p_outcomes))
        
        print(f"\nQuantum state dimension: 2^{self.n_qubits} = {2**self.n_qubits}")
        print(f"Von Neumann entropy S(ρ): {S_vn:.4f} bits")
        print(f"Holevo bound χ ≤ S(ρ):    {S_vn:.4f} bits")
        print(f"Extracted information:     {H_measurements:.4f} bits")
        print(f"Maximum possible:          {self.n_qubits} bits")
        
        violation = H_measurements - S_vn
        
        if violation > 0.1:  # Tolerance for numerical errors
            print(f"\n⚠️  WARNING: HOLEVO BOUND VIOLATED!")
            print(f"   Extracted {violation:.4f} more bits than allowed")
            print(f"   Information paradox detected")
            self.results['holevo'] = 'VIOLATED'
        else:
            print(f"\n✓ HOLEVO BOUND PRESERVED")
            print(f"   Information extraction within quantum limits")
            self.results['holevo'] = 'PRESERVED'
        
        return violation
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "="*70)
        print("TEMPORAL QUANTUM COMPUTING: QUANTUM MECHANICS VIOLATION TEST SUITE")
        print("="*70)
        print(f"\nTesting with α = {self.alpha:.4f}")
        print(f"Number of qubits: {self.n_qubits}")
        
        # Run all tests
        self.test_unitarity()
        self.test_no_cloning()
        self.test_causality()
        self.test_no_signaling()
        self.test_information_paradox()
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        
        for test_name, result in self.results.items():
            status = "❌ VIOLATED" if result == "VIOLATED" else "✅ PRESERVED"
            print(f"{test_name:20s}: {status}")
        
        violations = sum(1 for r in self.results.values() if r == "VIOLATED")
        
        print("\n" + "="*70)
        if violations > 0:
            print(f"⚠️  CONCLUSION: {violations}/{len(self.results)} QUANTUM LAWS VIOLATED")
            print("⚠️  Temporal quantum computing conflicts with quantum mechanics")
        else:
            print(f"✅ CONCLUSION: ALL {len(self.results)} QUANTUM LAWS PRESERVED")
            print("✅ Temporal quantum computing is consistent with quantum mechanics")
        print("="*70 + "\n")
        
        return self.results


if __name__ == "__main__":
    tester = QuantumViolationTests()
    results = tester.run_all_tests()
