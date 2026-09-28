#!/usr/bin/env python3
"""
test_telemetry_analysis.py - Unit test suite for MR Damper Lab analysis toolkit
"""

import os
import unittest
import numpy as np
import pandas as pd
import tempfile

from scripts.analyze_telemetry import compute_metrics
from scripts.generate_sample_data import simulate_spencer_mbw

class TestMRDamperTelemetry(unittest.TestCase):

    def setUp(self):
        # Generate a short synthetic simulation for testing
        self.df = simulate_spencer_mbw(duration=1.0, freq=2.0, amp=0.010, voltage=1.0)

    def test_simulation_columns(self):
        expected_cols = [
            "time_s", "displacement_m", "velocity_mps", "filteredVelocity_mps",
            "commandVoltage_V", "effectiveVoltage_V", "totalForce_N",
            "forceHysteresis_N", "forceViscous_N", "forceAccumulator_N",
            "forceDashpot1_N", "hystereticState_z_m", "internalState_y_m"
        ]
        for col in expected_cols:
            self.assertIn(col, self.df.columns)

    def test_positive_energy_dissipation(self):
        metrics = compute_metrics(self.df)
        self.assertGreater(metrics['energy_dissipated_J'], 0.0, "Energy dissipation must be strictly positive")
        self.assertGreater(metrics['equivalent_damping_Ns_m'], 0.0, "Equivalent damping must be positive")
        self.assertGreater(metrics['f_peak_N'], 0.0, "Peak force must be positive")

    def test_voltage_scaling(self):
        # Increasing voltage from 0.0V to 2.0V should increase dissipated work
        df_low = simulate_spencer_mbw(duration=1.0, freq=2.0, amp=0.010, voltage=0.0)
        df_high = simulate_spencer_mbw(duration=1.0, freq=2.0, amp=0.010, voltage=2.0)

        m_low = compute_metrics(df_low)
        m_high = compute_metrics(df_high)

        self.assertGreater(
            m_high['energy_dissipated_J'],
            m_low['energy_dissipated_J'],
            "High voltage must dissipate more energy than low voltage"
        )
        self.assertGreater(
            m_high['f_peak_N'],
            m_low['f_peak_N'],
            "High voltage peak force must exceed low voltage peak force"
        )

if __name__ == '__main__':
    unittest.main()
