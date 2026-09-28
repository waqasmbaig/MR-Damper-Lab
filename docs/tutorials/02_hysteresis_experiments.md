# 🧪 Tutorial 02: Systematic Hysteresis Experiments

This tutorial details 5 foundational engineering experiments you can conduct using the **MR Damper Lab** simulator to characterize magnetorheological fluid properties and validate semi-active damping mechanics.

---

## 🔬 Experiment 1: Voltage Dependency & Dynamic Range

### Objective
Quantify how commanded coil voltage ($0.0\,\text{V}$ to $2.0\,\text{V}$) modulates yield force, energy dissipation ($W_d$), and equivalent viscous damping ($C_{eq}$).

### Procedure
1. Set **Excitation**: Harmonic Sine Wave, $f = 1.5\,\text{Hz}$, Amplitude $X_0 = 15\,\text{mm}$.
2. Record steady-state telemetry at 5 discrete voltage levels:
   - $V = 0.0\,\text{V}$ (Off-state / baseline viscosity)
   - $V = 0.5\,\text{V}$ (Low field)
   - $V = 1.0\,\text{V}$ (Nominal operational field)
   - $V = 1.5\,\text{V}$ (High field)
   - $V = 2.0\,\text{V}$ (Maximum magnetic saturation)
3. For each voltage level, click **Export Data (.csv)**.

### Expected Trends
| Voltage (V) | Yield Force ($\alpha z$) | Peak Force (N) | $W_d$ (J/cycle) | $C_{eq}$ (N·s/m) |
| :---: | :---: | :---: | :---: | :---: |
| **0.0 V** | Low ($\approx 120\,\text{N}$) | $\approx 220\,\text{N}$ | $\approx 9.5\,\text{J}$ | $\approx 1450\,\text{N}\cdot\text{s/m}$ |
| **0.5 V** | Moderate ($\approx 280\,\text{N}$) | $\approx 410\,\text{N}$ | $\approx 18.2\,\text{J}$ | $\approx 2750\,\text{N}\cdot\text{s/m}$ |
| **1.0 V** | Strong ($\approx 440\,\text{N}$) | $\approx 610\,\text{N}$ | $\approx 28.0\,\text{J}$ | $\approx 4200\,\text{N}\cdot\text{s/m}$ |
| **1.5 V** | High ($\approx 600\,\text{N}$) | $\approx 810\,\text{N}$ | $\approx 37.5\,\text{J}$ | $\approx 5650\,\text{N}\cdot\text{s/m}$ |
| **2.0 V** | Max ($\approx 760\,\text{N}$) | $\approx 1020\,\text{N}$ | $\approx 47.0\,\text{J}$ | $\approx 7100\,\text{N}\cdot\text{s/m}$ |

**Key Finding**: The dynamic control ratio $\frac{F_{\max}(2.0\,\text{V})}{F_{\max}(0.0\,\text{V})} \approx 4.6\times$ confirms strong semi-active authority.

---

## 🔬 Experiment 2: Excitation Frequency Sensitivity

### Objective
Examine how excitation frequency ($0.5\,\text{Hz}$ to $10.0\,\text{Hz}$) influences the Force–Velocity curve slope and dynamic loop opening.

### Procedure
1. Fix **Voltage** to $V = 1.0\,\text{V}$ and **Amplitude** to $X_0 = 8\,\text{mm}$.
2. Vary **Frequency**:
   - $f = 1.0\,\text{Hz}$ ($\dot{x}_{\max} = 0.050\,\text{m/s}$)
   - $f = 3.0\,\text{Hz}$ ($\dot{x}_{\max} = 0.151\,\text{m/s}$)
   - $f = 6.0\,\text{Hz}$ ($\dot{x}_{\max} = 0.302\,\text{m/s}$)
   - $f = 10.0\,\text{Hz}$ ($\dot{x}_{\max} = 0.503\,\text{m/s}$)
3. Observe the Force–Velocity ($F-v$) plot.

### Physical Mechanism
- As frequency increases, the maximum piston velocity increases linearly ($\dot{x}_{\max} = 2\pi f X_0$).
- In the post-yield region, the slope remains governed by viscous resistance $c_0$.
- The characteristic loop opening near $\dot{x} = 0$ broadens at higher frequencies due to fluid inertia and intermediate node delay ($\dot{y}$).

---

## 🔬 Experiment 3: Stroke Amplitude Linearity

### Objective
Investigate the transition from pre-yield micro-displacement to fully developed post-yield plastic flow.

### Procedure
1. Fix **Voltage** to $V = 1.0\,\text{V}$ and **Frequency** to $f = 2.0\,\text{Hz}$.
2. Test 4 stroke amplitudes:
   - $X_0 = 1.0\,\text{mm}$ (Micro-stroke / pre-yield elasticity test)
   - $X_0 = 5.0\,\text{mm}$ (Partial yield transition)
   - $X_0 = 15.0\,\text{mm}$ (Fully developed hysteresis loop)
   - $X_0 = 25.0\,\text{mm}$ (Long-stroke viscous-dominant regime)

### Physical Mechanism
- Below $X_0 \approx 1.5\,\text{mm}$, the iron-particle chains in the MR fluid deform elastically without breaking. The $F-x$ loop is narrow and ellipse-like.
- Above $X_0 = 5\,\text{mm}$, complete fluid shear occurs, yielding the classical rectangular/parallelogram hysteresis envelope.

---

## 🔬 Experiment 4: Active MR vs. Linear Viscous Passive

### Objective
Compare energy dissipation and peak acceleration forces between an Active MR Damper and a standard passive shock absorber.

### Procedure
1. Run active simulation at $V = 1.5\,\text{V}$, $f = 2.0\,\text{Hz}$, $X_0 = 15\,\text{mm}$. Note $W_d$ and $F_{\max}$.
2. Toggle mode to **Linear Passive**. Adjust passive damping $C_{\text{pass}}$ until $W_d$ matches the active damper.
3. Compare the peak forces $F_{\max}$.

### Key Finding
- To achieve identical energy dissipation per cycle, the linear passive damper requires a substantially higher peak velocity force ($F_{\max} \propto \dot{x}_{\max}$), transmitting harsher shock accelerations to the vehicle chassis.
- The MR damper distributes force evenly across the stroke, achieving superior comfort and vibration isolation.

---

## 🔬 Experiment 5: Triangle Wave Constant Velocity Test

### Objective
Isolate the pure yield force $\alpha z$ from viscous damping $c_0 \dot{x}$.

### Procedure
1. In the sidebar, select **Excitation Waveform**: `Triangle Wave (Constant Velocity)`.
2. Set $f = 1.0\,\text{Hz}$ and Amplitude $= 15\,\text{mm}$.
3. Observe the resulting $F-x$ plot.

### Physical Mechanism
- During triangle wave motion, velocity is constant ($\dot{x} = \pm 4 f X_0$).
- Because $\ddot{x} = 0$, viscous damping $c_0 \dot{x}$ is constant throughout each half-cycle.
- The resulting $F-x$ loop has flat, horizontal top and bottom plateaus, isolating the pure Bingham-like yield stress plateau.
