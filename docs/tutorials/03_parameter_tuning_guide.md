# 🎛️ Tutorial 03: Parameter Tuning Guide & Sensitivity Analysis

This guide provides an engineering reference for tuning each of the **14 Spencer Modified Bouc-Wen (MBW)** parameters, explaining their physical mechanism, diagnostic symptoms, and adjustment recipes.

---

## 📊 Parameter Tuning Cheat Sheet

<p align="center">
  <img src="../assets/parameter_sensitivity.png" alt="Spencer MBW Parameter Sensitivity Cheat Sheet" width="100%" />
</p>

---

## 1. Hysteresis Shape Parameters ($\alpha, \beta, \gamma, n, A$)

### $\alpha$ (Yield Force Scaling Factor)
- **SI Units**: $\text{N/m}$
- **Formula**: $\alpha(u) = \alpha_a + \alpha_b u$
- **Physical Meaning**: Scales the hysteretic restoring force $\alpha z$. Directly dictates the height (vertical separation) of the hysteresis loop.
- **Tuning Rule**:
  - *If loop is too thin vertically*: Increase $\alpha_b$ (or command higher voltage $V$).
  - *If off-state force is too stiff*: Decrease $\alpha_a$.

### $\beta$ and $\gamma$ (Hysteresis Loop Curvature & Area)
- **SI Units**: $\text{m}^{-2}$
- **Physical Meaning**:
  - $(\beta + \gamma)$ dictates the rate of transition into the post-yield plastic state.
  - $(\gamma - \beta)$ dictates whether the loop is softening or hardening. For typical MR dampers, $\beta \approx \gamma > 0$ yields symmetric cyclic energy dissipation.
- **Tuning Rule**:
  - *Loop too narrow*: Decrease $\beta$ and $\gamma$ (e.g., from $5\times 10^6$ to $2\times 10^6\,\text{m}^{-2}$).
  - *Loop too fat or bulging*: Increase $\beta$ and $\gamma$.

### $n$ (Transition Smoothness Order)
- **SI Units**: Dimensionless (typically $n \in [1.5, 3.0]$, default $n = 2.0$)
- **Physical Meaning**: Controls the sharpness of the corner as the fluid transitions from pre-yield elastic shear to post-yield macroscopic flow.
- **Tuning Rule**:
  - $n = 1.0$: Gradual, rounded yield knee.
  - $n = 2.0$: Standard Spencer benchmark (smooth physical knee).
  - $n \ge 3.0$: Sharp bilinear corner transition.

### $A$ (Restoring Force Scale)
- **SI Units**: Dimensionless (typically $A \approx 50 - 300$)
- **Physical Meaning**: Dictates initial pre-yield linear stiffness slope ($k_{\text{pre}} \approx \alpha A$).

---

## 2. Viscous & Mechanical Dashpots ($c_0, c_1, k_0$)

### $c_0$ (High-Velocity Viscous Damping)
- **SI Units**: $\text{N}\cdot\text{s/m}$
- **Formula**: $c_0(u) = c_{0a} + c_{0b} u$
- **Physical Meaning**: Fluid viscous shear resistance between piston plate and housing at large velocities.
- **Tuning Rule**:
  - Controls the **slope** of the post-yield Force–Velocity line.
  - *If post-yield force does not rise with velocity*: Increase $c_{0a}$ or $c_{0b}$.

### $c_1$ (Low-Velocity Accumulator Damping)
- **SI Units**: $\text{N}\cdot\text{s/m}$
- **Formula**: $c_1(u) = c_{1a} + c_{1b} u$
- **Physical Meaning**: Fluid resistance through flow passages acting on intermediate node $y$.
- **Tuning Rule**:
  - Directly governs the **opening width of the Force–Velocity loop** near zero velocity ($\dot{x} \approx 0$).
  - *If F–V loop has no opening*: Increase $c_1$.

### $k_0$ (Dashpot Stiffness)
- **SI Units**: $\text{N/m}$
- **Physical Meaning**: Mechanical compliance of fluid column and internal damper linkages at high velocities.

---

## 3. Gas Accumulator Parameters ($k_1, x_0$)

### $k_1$ (Accumulator Gas Spring Compliance)
- **SI Units**: $\text{N/m}$
- **Physical Meaning**: Nitrogen reservoir elasticity that accommodates piston rod insertion volume.
- **Tuning Rule**:
  - Controls the **overall tilt** (angle of principal axis) of the Force–Displacement loop.
  - Higher $k_1$ tilts the loop counter-clockwise, creating an upward slope with positive displacement.

### $x_0$ (Accumulator Pre-Charge Offset)
- **SI Units**: $\text{m}$ (typically $10 - 30\,\text{mm}$)
- **Physical Meaning**: Pre-compression stroke of the accumulator chamber.
- **Tuning Rule**:
  - Introduces vertical asymmetric force bias ($F_{\text{bias}} = -k_1 x_0$).
  - For automotive struts, $x_0 > 0$ provides a static gas lift force supporting vehicle sprung mass.
  - Set $x_0 = 0.0$ for symmetric seismic structural dampers.

---

## 4. Electromagnetic Coil Lag ($\eta$)

### $\eta$ (Coil Response Rate)
- **SI Units**: $\text{s}^{-1}$
- **Physical Meaning**: First-order lag representing coil inductance and magnetic eddy currents ($\tau = 1/\eta$).
- **Benchmark**: $\eta = 190\,\text{s}^{-1} \implies \tau \approx 5.26\,\text{ms}$.
- **Tuning Rule**:
  - *Faster coil response (PWM driver)*: Increase $\eta \to 300\,\text{s}^{-1}$ ($\tau \approx 3.3\,\text{ms}$).
  - *Slow iron core*: Decrease $\eta \to 80\,\text{s}^{-1}$ ($\tau \approx 12.5\,\text{ms}$).
