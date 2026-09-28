#!/usr/bin/env python3
"""
generate_sample_data.py - Synthetic Telemetry Data Generator for MR Damper Lab

Generates CSV telemetry datasets matching the exact schema and numerical output
of the MR Damper Lab web application (Spencer Modified Bouc-Wen Model).
"""

import numpy as np
import pandas as pd
import os

def simulate_spencer_mbw(
    duration=3.0,
    dt=0.0002,
    freq=1.5,
    amp=0.015,
    voltage=1.0,
    waveform='sine',
    # Model parameters (Spencer 1997 / Lord RD-1005-3)
    k0=4690.0,
    k1=500.0,
    x0=0.0,
    alpha_a=14000.0,
    alpha_b=69500.0,
    c0_a=2100.0,
    c0_b=350.0,
    c1_a=28300.0,
    c1_b=295.0,
    A=58.0,
    beta=3.63e6,
    gamma=3.63e6,
    n=2.0,
    eta=190.0
):
    omega = 2.0 * np.pi * freq
    t_steps = int(duration / dt)
    time = np.linspace(0, duration, t_steps)

    # Voltage dependencies
    alpha = alpha_a + alpha_b * voltage
    c0 = c0_a + c0_b * voltage
    c1 = c1_a + c1_b * voltage

    # State variables
    y = 0.0
    z = 0.0
    u = 0.0
    v_f = 0.0

    records = []
    decimation = 25 # Match web app decimation (5 ms interval)

    for i, t in enumerate(time):
        # Kinematic excitation
        if waveform == 'sine':
            x = amp * np.sin(omega * t)
            v = amp * omega * np.cos(omega * t)
        elif waveform == 'triangle':
            period = 1.0 / freq
            rel_t = t % period
            quarter = period / 4.0
            if rel_t < quarter:
                x = (amp / quarter) * rel_t
                v = amp / quarter
            elif rel_t < 3.0 * quarter:
                x = amp - (amp / quarter) * (rel_t - quarter)
                v = -amp / quarter
            else:
                x = -amp + (amp / quarter) * (rel_t - 3.0 * quarter)
                v = amp / quarter
        else: # step
            x = amp if (t % 2.0) > 0.1 else 0.0
            v = 0.0

        # RK4 ODE step
        def eval_derivs(curr_y, curr_z, curr_u, curr_vf):
            omega_c = 2.0 * np.pi * 100.0
            dvf = omega_c * (v - curr_vf)
            v_eff = curr_vf
            du = -eta * (curr_u - voltage)
            
            al_u = alpha_a + alpha_b * curr_u
            c0_u = c0_a + c0_b * curr_u
            c1_u = c1_a + c1_b * curr_u

            dy = (1.0 / (c0_u + c1_u)) * (al_u * curr_z + k0 * (x - curr_y) + c0_u * v_eff)
            v_rel = v_eff - dy
            abs_z = abs(curr_z) + 1e-12
            dz = A * v_rel - beta * abs(v_rel) * curr_z * (abs_z**(n - 1.0)) - gamma * v_rel * (abs_z**n)
            return dy, dz, du, dvf, al_u, c0_u, c1_u, v_eff

        k1_y, k1_z, k1_u, k1_vf, _, _, _, _ = eval_derivs(y, z, u, v_f)
        k2_y, k2_z, k2_u, k2_vf, _, _, _, _ = eval_derivs(y + 0.5*dt*k1_y, z + 0.5*dt*k1_z, u + 0.5*dt*k1_u, v_f + 0.5*dt*k1_vf)
        k3_y, k3_z, k3_u, k3_vf, _, _, _, _ = eval_derivs(y + 0.5*dt*k2_y, z + 0.5*dt*k2_z, u + 0.5*dt*k2_u, v_f + 0.5*dt*k2_vf)
        k4_y, k4_z, k4_u, k4_vf, _, _, _, _ = eval_derivs(y + dt*k3_y, z + dt*k3_z, u + dt*k3_u, v_f + dt*k3_vf)

        y += (dt / 6.0) * (k1_y + 2*k2_y + 2*k3_y + k4_y)
        z += (dt / 6.0) * (k1_z + 2*k2_z + 2*k3_z + k4_z)
        u += (dt / 6.0) * (k1_u + 2*k2_u + 2*k3_u + k4_u)
        v_f += (dt / 6.0) * (k1_vf + 2*k2_vf + 2*k3_vf + k4_vf)

        if i % decimation == 0:
            dy_end, _, _, _, al_curr, c0_curr, c1_curr, v_eff_curr = eval_derivs(y, z, u, v_f)
            f_hyst = al_curr * z
            f_visc = c0_curr * (v_eff_curr - dy_end)
            f_accum = k1 * (x - x0)
            f_dashpot1 = c1_curr * dy_end
            f_total = f_dashpot1 + f_accum

            records.append({
                "time_s": round(t, 5),
                "displacement_m": round(x, 6),
                "velocity_mps": round(v, 6),
                "filteredVelocity_mps": round(v_eff_curr, 6),
                "commandVoltage_V": round(voltage, 2),
                "effectiveVoltage_V": round(u, 4),
                "totalForce_N": round(f_total, 2),
                "forceHysteresis_N": round(f_hyst, 2),
                "forceViscous_N": round(f_visc, 2),
                "forceAccumulator_N": round(f_accum, 2),
                "forceDashpot1_N": round(f_dashpot1, 2),
                "hystereticState_z_m": round(z, 7),
                "internalState_y_m": round(y, 7)
            })

    return pd.DataFrame(records)

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)

    print("Generating sample harmonic sweep (1.5 Hz, 15 mm, 1.0 V)...")
    df_sine = simulate_spencer_mbw(waveform='sine', voltage=1.0)
    df_sine.to_csv(os.path.join(out_dir, "sample_harmonic_sweep.csv"), index=False)
    print(f"  -> Saved {len(df_sine)} data points to data/sample_harmonic_sweep.csv")

    print("Generating sample triangle sweep (1.5 Hz, 15 mm, 1.5 V)...")
    df_tri = simulate_spencer_mbw(waveform='triangle', voltage=1.5)
    df_tri.to_csv(os.path.join(out_dir, "sample_triangle_wave.csv"), index=False)
    print(f"  -> Saved {len(df_tri)} data points to data/sample_triangle_wave.csv")
