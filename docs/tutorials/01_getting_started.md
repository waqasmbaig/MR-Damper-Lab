# 🚀 Tutorial 01: Getting Started with MR Damper Lab

Welcome to the **MR Damper Lab** interactive digital twin! This guide walks you through launching the simulator, understanding the user interface, running real-time numerical experiments, and exporting telemetry data.

---

## 1. Accessing the Application

The web application runs entirely client-side with zero installation:
- **Primary Live App**: [https://modified-bouc-wen-model-simulation.ai.studio](https://modified-bouc-wen-model-simulation.ai.studio)
- **GitHub Pages Mirror**: [https://waqasmbaig.github.io/Modified-Bouc-Wen-Model-Simulation/](https://waqasmbaig.github.io/Modified-Bouc-Wen-Model-Simulation/)

Alternatively, run locally on your machine:
```bash
git clone https://github.com/waqasmbaig/Modified-Bouc-Wen-Model-Simulation.git
cd Modified-Bouc-Wen-Model-Simulation
npx serve .
```

---

## 2. Interface Overview

```
+---------------------------+-------------------------------------------------------------+
| SIDEBAR CONTROLS          | MAIN DASHBOARD DISPLAY                                      |
|                           |                                                             |
| - Mode (Active / Passive) | [ DIGITAL TWIN PISTON ]  [ TELEMETRY CARDS ]               |
| - Benchmark Presets       |   Stroke, Velocity, Yield    Energy/Cyc, Peak Force, C_eq   |
| - RK4 Simulation Controls |                                                             |
|   (Run / Pause / Reset)   | [ TABS: Hysteresis Loops | Force Decomp | State Variables ] |
| - Excitation Settings     |                                                             |
|   (Waveform, Freq, Amp)   |   Left: Force-Displacement    Right: Force-Velocity         |
| - 14-Param Model Tuning   |                                                             |
|                           | [ TIME-SERIES SIGNALS: x(t), v(t), F(t) ]                   |
| [ AI DAMPER CONSULTANT ]  |                                                             |
|   (Gemini 3.8 Advisory)   | [ Top Bar: Model Theory • Export Telemetry (.csv) ]         |
+---------------------------+-------------------------------------------------------------+
```

### Key Functional Sections:
1. **Operating Mode Toggle**:
   - **Active MR Damper**: Full 14-parameter Spencer model with field-dependent yield stress $\alpha(u)$, viscous damping $c_0(u)$, and coil lag $\eta$.
   - **Linear Passive**: Standard viscous dashpot ($F = C_{\text{pass}} \cdot \dot{x}$) for side-by-side performance benchmarking.
2. **RK4 Numerical Engine**:
   - Fixed step size: $\Delta t = 0.2\,\text{ms}$ (resolving modes up to $500\,\text{Hz}$).
   - Execution rate: 60 FPS real-time animation.
   - Time multiplier slider: $0.1\times$ (slow motion) to $3.0\times$ (fast-forward).
3. **Digital Twin Piston**:
   - Real-time kinematic animation of the piston shaft inside the Lord RD-1005-3 damper housing.
   - Dynamic yield indicator: Automatically displays whether the fluid is in **Pre-Yield**, **Post-Yield**, or undergoing **Yield Transition**.
4. **Live Performance Telemetry**:
   - **Energy per Cycle ($W_d$)**: Dissipated work computed via numerical loop line integral ($\oint F_d \, dx$).
   - **Peak Force ($F_{\max}$)**: Maximum dynamic reaction force.
   - **Equivalent Damping ($C_{eq}$)**: Calculated as $W_d / (\pi \omega X_0^2)$.
   - **Average & Peak Power**: Dissipated thermal power rating.

---

## 3. Running Your First Simulation

1. Click **`Run Live`** in the sidebar. The piston rod will begin oscillating at the baseline harmonic stroke ($f = 1.5\,\text{Hz}$, $X_0 = 15\,\text{mm}$, $V = 1.0\,\text{V}$).
2. Observe the **Hysteresis Loop (Force vs. Displacement)** on the left. The enclosed blue area represents dissipated mechanical energy.
3. Switch to the **Force Decomposition** tab: Note how total force is synthesized from the hysteretic spring $\alpha z$, the viscous dashpot $c_0(\dot{x}-\dot{y})$, and the accumulator gas spring $k_1(x-x_0)$.
4. Adjust the **Command Voltage (V)** slider from $0.0\,\text{V}$ to $2.0\,\text{V}$ and watch the yield force expand dynamically!

---

## 4. Exporting Telemetry Data

Click the **`Export Data (.csv)`** button in the top navigation bar. The application will download a timestamped CSV containing the full 60 FPS simulation buffer:
```csv
time_s,displacement_m,velocity_mps,filteredVelocity_mps,commandVoltage_V,effectiveVoltage_V,totalForce_N,forceHysteresis_N,forceViscous_N,forceAccumulator_N,forceDashpot1_N,hystereticState_z_m,internalState_y_m
0.00000,0.000000,0.141372,0.141372,1.00,0.0000,28.45,0.00,28.45,0.00,28.45,0.0000000,0.0000000
...
```

You can immediately analyze this data with the Python tools provided in this repository:
```bash
python3 scripts/analyze_telemetry.py path/to/exported_file.csv --save output.png
```
