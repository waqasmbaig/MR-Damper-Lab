#!/usr/bin/env python3
"""
analyze_telemetry.py - MR Damper Telemetry & Hysteresis Analysis Toolkit

Processes CSV telemetry files exported from the MR Damper Lab web application.
Calculates energy dissipation per cycle (Wd), equivalent viscous damping (C_eq),
peak dynamic forces, and generates high-resolution engineering plots.

Usage:
    python3 scripts/analyze_telemetry.py data/sample_harmonic_sweep.csv --save docs/assets/telemetry_analysis_sample.png
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compute_metrics(df):
    """
    Computes key semi-active vibration and hysteresis metrics in SI units.
    """
    time = df['time_s'].values
    disp = df['displacement_m'].values
    vel = df['velocity_mps'].values
    force = df['totalForce_N'].values

    dt = np.mean(np.diff(time))
    total_time = time[-1] - time[0]

    # Peak forces
    f_max = np.max(force)
    f_min = np.min(force)
    f_peak = max(abs(f_max), abs(f_min))

    # Stroke amplitude and frequency estimation via zero-crossings or peak-to-peak
    x_amp = 0.5 * (np.max(disp) - np.min(disp))
    
    # Estimate frequency
    zero_crossings = np.where(np.diff(np.signbit(disp)))[0]
    if len(zero_crossings) >= 2:
        half_periods = np.diff(time[zero_crossings])
        est_period = 2.0 * np.mean(half_periods)
        est_freq = 1.0 / est_period if est_period > 0 else 1.0
    else:
        est_freq = 1.5

    omega = 2.0 * np.pi * est_freq

    # Energy dissipated per cycle: W_d = \oint F dx
    # Numerical trapezoidal cycle integration over the last full cycle
    cycle_time = 1.0 / est_freq if est_freq > 0 else 1.0
    last_cycle_mask = time >= (time[-1] - cycle_time)

    x_cyc = disp[last_cycle_mask]
    f_cyc = force[last_cycle_mask]
    v_cyc = vel[last_cycle_mask]

    # Trapezoidal integration for loop area
    work_dissipated = np.abs(np.trapezoid(f_cyc, x_cyc))

    # Equivalent viscous damping: C_eq = W_d / (pi * omega * X0^2)
    if x_amp > 1e-6 and omega > 1e-3:
        c_eq = work_dissipated / (np.pi * omega * (x_amp**2))
    else:
        c_eq = 0.0

    # Power metrics
    inst_power = np.abs(force * vel)
    p_peak = np.max(inst_power)
    p_avg = np.mean(inst_power)

    return {
        "f_max_N": f_max,
        "f_min_N": f_min,
        "f_peak_N": f_peak,
        "stroke_amp_mm": x_amp * 1e3,
        "frequency_Hz": est_freq,
        "energy_dissipated_J": work_dissipated,
        "equivalent_damping_Ns_m": c_eq,
        "peak_power_W": p_peak,
        "avg_power_W": p_avg,
        "voltage_V": df['commandVoltage_V'].iloc[-1] if 'commandVoltage_V' in df else 0.0
    }

def plot_telemetry(df, metrics, save_path=None):
    """
    Renders publication-grade 4-panel telemetry and hysteresis characterization.
    """
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), facecolor='#070d18')
    fig.suptitle(
        f"MR Damper Telemetry Characterization • Spencer MBW Model\n"
        f"Voltage: {metrics['voltage_V']:.1f} V | Stroke: ±{metrics['stroke_amp_mm']:.1f} mm @ {metrics['frequency_Hz']:.2f} Hz | "
        f"$W_d$: {metrics['energy_dissipated_J']:.2f} J/cycle | $C_{{eq}}$: {metrics['equivalent_damping_Ns_m']:.0f} N·s/m",
        color='#f8fafc', fontsize=12, fontweight='bold', y=0.98
    )

    t = df['time_s'].values
    x_mm = df['displacement_m'].values * 1e3
    v_mps = df['velocity_mps'].values
    f_N = df['totalForce_N'].values

    # 1. Hysteresis Loop: Force vs. Displacement
    ax1 = axs[0, 0]
    ax1.set_facecolor('#0f172a')
    ax1.grid(True, color='#1e293b', ls='--', lw=0.7)
    ax1.plot(x_mm, f_N, color='#38bdf8', lw=2.2, label='Damper Force $F_d$')
    ax1.fill(x_mm, f_N, color='#0284c7', alpha=0.15, label=f'Enclosed Work $W_d = {metrics["energy_dissipated_J"]:.2f}$ J')
    ax1.axhline(0, color='#334155', lw=0.8, ls=':')
    ax1.axvline(0, color='#334155', lw=0.8, ls=':')
    ax1.set_title("Hysteresis Loop (Force vs. Displacement)", color='#e2e8f0', fontsize=11, fontweight='semibold')
    ax1.set_xlabel("Piston Displacement $x$ (mm)", color='#94a3b8', fontsize=9)
    ax1.set_ylabel("Total Damping Force $F_d$ (N)", color='#94a3b8', fontsize=9)
    ax1.tick_params(colors='#94a3b8', labelsize=8)
    ax1.legend(facecolor='#070d18', edgecolor='#334155', labelcolor='#cbd5e1', fontsize=8, loc='upper left')

    # 2. Damping Curve: Force vs. Velocity
    ax2 = axs[0, 1]
    ax2.set_facecolor('#0f172a')
    ax2.grid(True, color='#1e293b', ls='--', lw=0.7)
    ax2.plot(v_mps, f_N, color='#34d399', lw=2.2, label='Damping Curve $F_d - v$')
    ax2.axhline(0, color='#334155', lw=0.8, ls=':')
    ax2.axvline(0, color='#334155', lw=0.8, ls=':')
    ax2.set_title("Force vs. Velocity Characteristics", color='#e2e8f0', fontsize=11, fontweight='semibold')
    ax2.set_xlabel("Piston Velocity $\\dot{x}$ (m/s)", color='#94a3b8', fontsize=9)
    ax2.set_ylabel("Total Damping Force $F_d$ (N)", color='#94a3b8', fontsize=9)
    ax2.tick_params(colors='#94a3b8', labelsize=8)
    ax2.legend(facecolor='#070d18', edgecolor='#334155', labelcolor='#cbd5e1', fontsize=8, loc='upper left')

    # 3. Synchronized Time Series Signals
    ax3 = axs[1, 0]
    ax3.set_facecolor('#0f172a')
    ax3.grid(True, color='#1e293b', ls='--', lw=0.7)
    ax3.plot(t, x_mm, color='#60a5fa', lw=1.8, label='Displacement $x$ (mm)')
    ax3.plot(t, v_mps * 100.0, color='#fbbf24', lw=1.5, ls='--', label='Velocity $\\dot{x}$ (cm/s)')
    ax3.plot(t, f_N / 10.0, color='#f472b6', lw=1.8, label='Force $F_d$ (daN = 10 N)')
    ax3.set_title("Synchronized Time-Series Telemetry", color='#e2e8f0', fontsize=11, fontweight='semibold')
    ax3.set_xlabel("Simulation Time $t$ (s)", color='#94a3b8', fontsize=9)
    ax3.set_ylabel("Signal Amplitude (Scaled)", color='#94a3b8', fontsize=9)
    ax3.tick_params(colors='#94a3b8', labelsize=8)
    ax3.legend(facecolor='#070d18', edgecolor='#334155', labelcolor='#cbd5e1', fontsize=8, loc='upper right')

    # 4. Internal Force Decomposition
    ax4 = axs[1, 1]
    ax4.set_facecolor('#0f172a')
    ax4.grid(True, color='#1e293b', ls='--', lw=0.7)
    ax4.plot(t, f_N, color='#f8fafc', lw=2.0, label='Total Force $F_d$')
    if 'forceHysteresis_N' in df:
        ax4.plot(t, df['forceHysteresis_N'], color='#a855f7', lw=1.4, ls='--', label='Hysteretic Force $\\alpha z$')
    if 'forceViscous_N' in df:
        ax4.plot(t, df['forceViscous_N'], color='#38bdf8', lw=1.4, ls=':', label='Viscous Force $c_0(\\dot{x}-\\dot{y})$')
    if 'forceAccumulator_N' in df:
        ax4.plot(t, df['forceAccumulator_N'], color='#fb923c', lw=1.4, ls='-.', label='Accumulator $k_1(x-x_0)$')
    ax4.set_title("Internal Force Decomposition", color='#e2e8f0', fontsize=11, fontweight='semibold')
    ax4.set_xlabel("Simulation Time $t$ (s)", color='#94a3b8', fontsize=9)
    ax4.set_ylabel("Force Component (N)", color='#94a3b8', fontsize=9)
    ax4.tick_params(colors='#94a3b8', labelsize=8)
    ax4.legend(facecolor='#070d18', edgecolor='#334155', labelcolor='#cbd5e1', fontsize=8, loc='upper right')

    for ax in axs.flat:
        for spine in ax.spines.values():
            spine.set_color('#334155')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        plt.savefig(save_path, dpi=150, facecolor='#070d18', edgecolor='none')
        print(f"Plot saved successfully to: {save_path}")
    else:
        plt.show()
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Analyze MR Damper telemetry CSV files from MR Damper Lab.")
    parser.add_argument("csv_file", help="Path to exported telemetry CSV file")
    parser.add_argument("--save", "-s", help="Output path for telemetry characterization figure (.png)")
    parser.add_argument("--json", action="store_true", help="Print metrics in JSON format")

    args = parser.parse_args()

    if not os.path.exists(args.csv_file):
        print(f"Error: File not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(args.csv_file)
    metrics = compute_metrics(df)

    if args.json:
        import json
        print(json.dumps(metrics, indent=2))
    else:
        print("\n=======================================================")
        print("   MAGNETORHEOLOGICAL DAMPER TELEMETRY REPORT")
        print("=======================================================")
        print(f"Command Voltage         : {metrics['voltage_V']:.2f} V")
        print(f"Stroke Amplitude        : ±{metrics['stroke_amp_mm']:.2f} mm")
        print(f"Excitation Frequency    : {metrics['frequency_Hz']:.2f} Hz")
        print(f"Peak Force (F_max)      : {metrics['f_max_N']:+.1f} N")
        print(f"Min Force (F_min)       : {metrics['f_min_N']:+.1f} N")
        print(f"Peak Magnitude          : {metrics['f_peak_N']:.1f} N")
        print(f"Energy Dissipated (W_d) : {metrics['energy_dissipated_J']:.3f} J/cycle")
        print(f"Equiv. Damping (C_eq)   : {metrics['equivalent_damping_Ns_m']:.1f} N·s/m")
        print(f"Peak Power Dissipation  : {metrics['peak_power_W']:.1f} W")
        print(f"Average Power           : {metrics['avg_power_W']:.1f} W")
        print("=======================================================\n")

    plot_telemetry(df, metrics, save_path=args.save)

if __name__ == "__main__":
    main()
