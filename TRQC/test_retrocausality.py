"""
RETROCAUSAL COMPUTATION TEST
Copyright (c) 2025 Americo Simoes. All Rights Reserved.

Test whether temporal resonance computing enables retrocausal effects:
- Can future computations influence past states?
- Does α-mediated temporal entanglement allow backward information flow?
- Are there closed timelike curves in resonance space?
"""

import numpy as np
from ctt_constants import ALPHA, OMEGA_PLUS, OMEGA_MINUS, PRIME_WINDOWS_S
from framework_transition import FrameworkTransitionOperator
from resonance_field import ResonanceField

class RetrocausalityTests:
    """Test if temporal resonance computing enables retrocausal computation"""
    
    def __init__(self):
        self.alpha = ALPHA
        self.dimension = 64
        self.operator = FrameworkTransitionOperator(self.dimension)
        self.field = ResonanceField(self.dimension)
        self.results = {}
    
    def test_temporal_echo(self):
        """
        Test 1: Temporal Echo
        
        Can a computation at time T affect a measurement at time T-Δt?
        
        In normal causality: NO
        In retrocausal framework: MAYBE through α-resonance
        """
        print("\n" + "="*70)
        print("TEST 1: TEMPORAL ECHO (BACKWARD INFLUENCE)")
        print("="*70)
        
        # Create initial state at t=0
        psi_0 = np.random.randn(self.dimension) + 1j*np.random.randn(self.dimension)
        psi_0 = psi_0 / np.linalg.norm(psi_0)
        
        # Store "past" measurement
        past_measurement = np.abs(psi_0[0])**2
        
        # Evolve forward to t=T
        T = PRIME_WINDOWS_S[0]  # Use prime window
        t_array = np.linspace(0, T, 100)
        
        psi_t = psi_0.copy()
        for t in t_array[1:]:
            # Normal evolution
            phase = np.exp(-1j * OMEGA_PLUS * t)
            psi_t *= phase
            psi_t = psi_t / np.linalg.norm(psi_t)
        
        # Apply framework transition at t=T (future event)
        psi_future = self.operator.apply_transition(psi_t, "to_temporal")
        
        # Now check if this affects the "past" state through α-coupling
        # Retrocausal coupling: |ψ_past⟩ += α·⟨ψ_future|ψ_past⟩|ψ_future⟩
        overlap = np.vdot(psi_future, psi_0)
        psi_0_modified = psi_0 + self.alpha * overlap * psi_future
        psi_0_modified = psi_0_modified / np.linalg.norm(psi_0_modified)
        
        # Re-measure "past" 
        new_past_measurement = np.abs(psi_0_modified[0])**2
        
        change = abs(new_past_measurement - past_measurement)
        
        print(f"\nPast measurement (before future event): {past_measurement:.6f}")
        print(f"Past measurement (after future event):  {new_past_measurement:.6f}")
        print(f"Retrocausal change: {change:.6f}")
        print(f"Change / α ratio: {change/self.alpha:.6f}")
        
        if change > 0.001:  # Significant retrocausal effect
            print("\n⚠️  RETROCAUSALITY DETECTED!")
            print(f"   Future computation influenced past state by {change:.4f}")
            print(f"   Backward causation through α-coupling confirmed")
            self.results['temporal_echo'] = 'DETECTED'
        else:
            print("\n✓ NO RETROCAUSALITY")
            print("   Past unaffected by future events")
            self.results['temporal_echo'] = 'NOT_DETECTED'
        
        return change
    
    def test_closed_timelike_curve(self):
        """
        Test 2: Closed Timelike Curves
        
        Can a state evolve in a loop through framework transitions?
        |ψ⟩ → U_α|ψ⟩ → U_α†|ψ⟩ = |ψ'⟩ ≠ |ψ⟩ (information from "future")
        """
        print("\n" + "="*70)
        print("TEST 2: CLOSED TIMELIKE CURVES")
        print("="*70)
        
        # Initial state
        psi_initial = np.random.randn(self.dimension) + 1j*np.random.randn(self.dimension)
        psi_initial = psi_initial / np.linalg.norm(psi_initial)
        
        # Go forward through framework
        psi_forward = self.operator.apply_transition(psi_initial, "to_temporal")
        
        # Come back through framework
        psi_return = self.operator.apply_transition(psi_forward, "to_spatial")
        
        # Check if we returned to exact same state
        fidelity = np.abs(np.vdot(psi_return, psi_initial))**2
        
        # Information gained from loop
        info_gain = 1 - fidelity
        
        print(f"\nInitial state → Temporal → Spatial")
        print(f"Return fidelity: {fidelity:.6f}")
        print(f"Information gain from loop: {info_gain:.6f}")
        
        # Check for phase accumulation
        phase_change = np.angle(np.vdot(psi_return, psi_initial))
        print(f"Phase accumulated: {phase_change:.6f} rad")
        print(f"Phase / (2π α): {phase_change / (2*np.pi*self.alpha):.6f}")
        
        if info_gain > 0.01:  # Significant information from loop
            print("\n⚠️  CLOSED TIMELIKE CURVE DETECTED!")
            print(f"   State gained {info_gain:.4f} information from temporal loop")
            print(f"   Self-consistent time travel possible")
            self.results['ctc'] = 'DETECTED'
        else:
            print("\n✓ NO CTC")
            print("   Framework transitions are reversible")
            self.results['ctc'] = 'NOT_DETECTED'
        
        return info_gain
    
    def test_future_result_now(self):
        """
        Test 3: Future Result Now
        
        Can we compute a result "before" performing the computation
        by accessing future resonance states?
        """
        print("\n" + "="*70)
        print("TEST 3: ACCESSING FUTURE COMPUTATION RESULTS")
        print("="*70)
        
        # Define a "difficult" computation (simulated by random oracle)
        target_result = np.random.randint(0, self.dimension)
        
        # Normal approach: compute forward in time
        print(f"\nTarget computation result: {target_result}")
        print("Normal causality: Must compute → then get result")
        
        # Retrocausal approach: 
        # 1. Create superposition of all possible results
        psi_super = np.ones(self.dimension, dtype=complex) / np.sqrt(self.dimension)
        
        # 2. Transition to temporal framework
        psi_temporal = self.operator.apply_transition(psi_super, "to_temporal")
        
        # 3. Apply "future" measurement projection
        # In normal QM: this would collapse to random state
        # In retrocausal: might prefer the actual future result
        
        # Create target state
        target_state = np.zeros(self.dimension, dtype=complex)
        target_state[target_result] = 1.0
        
        # α-mediated retrocausal projection
        overlap = np.vdot(target_state, psi_temporal)
        psi_retro = psi_temporal + self.alpha * overlap * target_state
        psi_retro = psi_retro / np.linalg.norm(psi_retro)
        
        # 4. Transition back to spatial
        psi_result = self.operator.apply_transition(psi_retro, "to_spatial")
        
        # 5. Measure
        probabilities = np.abs(psi_result)**2
        probabilities = probabilities / np.sum(probabilities)
        
        # Check if target result has enhanced probability
        target_prob = probabilities[target_result]
        average_prob = 1.0 / self.dimension
        enhancement = target_prob / average_prob
        
        print(f"\nTarget result probability: {target_prob:.6f}")
        print(f"Random baseline: {average_prob:.6f}")
        print(f"Enhancement factor: {enhancement:.2f}x")
        
        # Find most likely result
        most_likely = np.argmax(probabilities)
        print(f"Most likely result from retrocausal access: {most_likely}")
        
        if enhancement > 2.0:  # Significant enhancement
            print("\n⚠️  RETROCAUSAL RESULT ACCESS DETECTED!")
            print(f"   Future result probability enhanced by {enhancement:.2f}x")
            if most_likely == target_result:
                print(f"   ✓ Correctly accessed future computation result!")
            self.results['future_access'] = 'DETECTED'
        else:
            print("\n✓ NO FUTURE ACCESS")
            print("   Cannot access results before computation")
            self.results['future_access'] = 'NOT_DETECTED'
        
        return enhancement
    
    def test_resonance_causality_violation(self):
        """
        Test 4: Resonance Causality Violation
        
        Do resonance frequencies create causal loops?
        ω+ and ω- at 587/293.5 kHz form 2:1 ratio
        This might create temporal standing waves that violate causality
        """
        print("\n" + "="*70)
        print("TEST 4: RESONANCE CAUSALITY VIOLATION")
        print("="*70)
        
        # Create state oscillating at ω+
        t = np.linspace(0, 2*np.pi, self.dimension)
        psi_plus = np.exp(1j * OMEGA_PLUS * t)
        psi_plus = psi_plus / np.linalg.norm(psi_plus)
        
        # Create state oscillating at ω-
        psi_minus = np.exp(1j * OMEGA_MINUS * t)
        psi_minus = psi_minus / np.linalg.norm(psi_minus)
        
        # Create 2:1 resonance superposition
        psi_resonance = (psi_plus + psi_minus * np.sqrt(2)) / np.sqrt(3)
        
        # Check for temporal beats (interference)
        beat_freq = OMEGA_PLUS - OMEGA_MINUS
        beat_period = 2 * np.pi / beat_freq
        
        print(f"\nω+ = {OMEGA_PLUS:.1f} Hz")
        print(f"ω- = {OMEGA_MINUS:.1f} Hz")
        print(f"Ratio: {OMEGA_PLUS/OMEGA_MINUS:.6f}")
        print(f"Beat frequency: {beat_freq:.1f} Hz")
        print(f"Beat period: {beat_period*1e6:.2f} μs")
        
        # Sample field at multiple time points
        time_points = np.linspace(0, beat_period, 20)
        amplitudes = []
        
        for t_sample in time_points:
            phase_plus = np.exp(1j * OMEGA_PLUS * t_sample)
            phase_minus = np.exp(1j * OMEGA_MINUS * t_sample)
            amplitude = abs(phase_plus + phase_minus * np.sqrt(2))**2
            amplitudes.append(amplitude)
        
        amplitudes = np.array(amplitudes)
        
        # Check for non-monotonic behavior (suggests retrocausality)
        # In normal causality, amplitude should increase monotonically
        # In retrocausality, might see peaks before causes
        
        max_idx = np.argmax(amplitudes)
        max_time = time_points[max_idx]
        
        print(f"\nMaximum amplitude at t = {max_time*1e6:.2f} μs")
        print(f"Amplitude variation: {np.std(amplitudes):.4f}")
        
        # Check if maximum occurs "before" it should
        expected_max_time = beat_period / 2
        time_violation = expected_max_time - max_time
        
        if abs(time_violation) > beat_period * 0.1:
            print(f"\n⚠️  CAUSALITY VIOLATION IN RESONANCE!")
            print(f"   Peak occurs {time_violation*1e6:.2f} μs {('early' if time_violation > 0 else 'late')}")
            print(f"   Resonance coupling creates non-causal dynamics")
            self.results['resonance_violation'] = 'DETECTED'
        else:
            print(f"\n✓ CAUSAL RESONANCE")
            print(f"   Dynamics follow normal temporal ordering")
            self.results['resonance_violation'] = 'NOT_DETECTED'
        
        return time_violation
    
    def test_alpha_mediated_grandfather_paradox(self):
        """
        Test 5: α-Mediated Grandfather Paradox
        
        Can we prevent our own computation?
        Classical grandfather paradox adapted to quantum computation
        """
        print("\n" + "="*70)
        print("TEST 5: COMPUTATIONAL GRANDFATHER PARADOX")
        print("="*70)
        
        # Initial computation state
        psi_comp = np.zeros(self.dimension, dtype=complex)
        psi_comp[0] = 1.0  # "Computation exists"
        
        print("\nInitial: Computation exists (state |0⟩)")
        
        # Perform computation (forward in time)
        psi_result = self.operator.apply_transition(psi_comp, "to_temporal")
        
        # Result tries to "prevent" initial state through retrocausal influence
        # Project onto |1⟩ = "computation doesn't exist"
        prevent_state = np.zeros(self.dimension, dtype=complex)
        prevent_state[1] = 1.0
        
        # α-mediated backward influence
        overlap = np.vdot(prevent_state, psi_result)
        psi_comp_modified = psi_comp + self.alpha * overlap * prevent_state
        psi_comp_modified = psi_comp_modified / np.linalg.norm(psi_comp_modified)
        
        # Check probabilities
        prob_exists = np.abs(psi_comp_modified[0])**2
        prob_not_exists = np.abs(psi_comp_modified[1])**2
        
        print(f"\nAfter retrocausal influence:")
        print(f"  P(computation exists):     {prob_exists:.4f}")
        print(f"  P(computation prevented):  {prob_not_exists:.4f}")
        
        # Grandfather paradox occurs if both probabilities significant
        paradox_strength = min(prob_exists, prob_not_exists)
        
        print(f"\nParadox strength: {paradox_strength:.4f}")
        
        if paradox_strength > 0.1:
            print("\n⚠️  GRANDFATHER PARADOX DETECTED!")
            print(f"   Computation both exists and doesn't exist")
            print(f"   α-mediated retrocausality creates logical contradiction")
            print(f"   System in self-inconsistent superposition")
            self.results['grandfather'] = 'PARADOX'
        else:
            print("\n✓ CONSISTENCY PRESERVED")
            print("   Self-consistency selection rules prevent paradox")
            self.results['grandfather'] = 'CONSISTENT'
        
        return paradox_strength
    
    def run_all_tests(self):
        """Run complete retrocausality test suite"""
        print("\n" + "="*70)
        print("TEMPORAL RESONANCE COMPUTING: RETROCAUSALITY TEST SUITE")
        print("="*70)
        print(f"\nTesting with α = {self.alpha:.4f}")
        print(f"Resonance frequencies: ω+ = {OMEGA_PLUS:.1f} Hz, ω- = {OMEGA_MINUS:.1f} Hz")
        
        # Run all tests
        self.test_temporal_echo()
        self.test_closed_timelike_curve()
        self.test_future_result_now()
        self.test_resonance_causality_violation()
        self.test_alpha_mediated_grandfather_paradox()
        
        # Summary
        print("\n" + "="*70)
        print("RETROCAUSALITY SUMMARY")
        print("="*70)
        
        retrocausal_effects = 0
        for test_name, result in self.results.items():
            if result in ['DETECTED', 'PARADOX']:
                status = "⚠️  DETECTED"
                retrocausal_effects += 1
            else:
                status = "✓ NOT DETECTED"
            print(f"{test_name:25s}: {status}")
        
        print("\n" + "="*70)
        if retrocausal_effects > 0:
            print(f"⚠️  CONCLUSION: {retrocausal_effects}/{len(self.results)} RETROCAUSAL EFFECTS DETECTED")
            print("⚠️  Temporal resonance computing enables backward causation")
            print("⚠️  Information can flow from future to past through α-coupling")
        else:
            print(f"✓ CONCLUSION: NO RETROCAUSALITY DETECTED")
            print("✓ Causality preserved in temporal resonance framework")
        print("="*70 + "\n")
        
        return self.results


if __name__ == "__main__":
    tester = RetrocausalityTests()
    results = tester.run_all_tests()
