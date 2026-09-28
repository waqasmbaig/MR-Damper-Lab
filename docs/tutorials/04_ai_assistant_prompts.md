# 🤖 Tutorial 04: AI Damper Consultant Workflows

The **MR Damper Lab** simulator includes an embedded **AI Vibration Consultant** powered by Google's Gemini models (with built-in heuristic engineering fallbacks). This guide demonstrates how to leverage the AI consultant for parameter optimization, stability verification, and suspension tuning.

---

## 1. Operating Modes of the AI Consultant

The consultant provides 4 specialized engineering inquiry channels:

| Mode | Focus Area | Key Output Metrics Evaluated |
| :--- | :--- | :--- |
| **Hysteresis Loop** | Shape optimization & corner sharpness | Pre-yield slope, post-yield slope, accumulator tilt, $\beta, \gamma, n$ |
| **Energy & Work** | Maximizing dissipated damping energy | Dissipated work $W_d$ (J/cycle), equivalent viscous damping $C_{eq}$ |
| **Model Stability** | Numerical consistency & non-physical check | Parameter bounds, stiff ODE mode checks, integrator step sanity |
| **Ride / Handling** | Automotive semi-active suspension compromise | Dynamic control authority, high-speed blow-off, low-speed roll control |

---

## 2. Recommended Consultation Prompts

When using the AI Consultant, click the engineering focus pill and press **`Analyze Current Damper State`**. Below are examples of queries and diagnostic interpretations:

### Scenario A: Optimizing Hysteresis Loop Sharpness
- **Problem**: The hysteresis loop appears too rounded or lacks distinct pre-yield vs. post-yield separation.
- **Consultant Recommendation**:
  > - Increase yield order $n$ from $2.0$ to $2.8$ to produce crisper bilinear corners.
  > - Check scaling parameter $A$: Ensure $A \ge 50$ to maintain adequate elastic stiffness prior to fluid shear.
  > - Verify accumulator damping $c_1$: Ensure $c_1 \gg c_0$ (ratio $\approx 10:1$) to preserve the sharp force knee.

### Scenario B: Maximizing Dissipated Work ($W_d$) without Excessive Peak Force
- **Problem**: High damping is desired for seismic isolation or off-road bump control, but peak force must not exceed structural mount limits ($F_{\max} \le 1200\,\text{N}$).
- **Consultant Recommendation**:
  > - Increase $\alpha_b$ to expand yield plateau height where velocity is high.
  > - Keep post-yield viscosity $c_0$ moderate ($1500 - 2500\,\text{N}\cdot\text{s/m}$) to avoid quadratic velocity force spikes.
  > - Decrease $\beta$ and $\gamma$ slightly to maintain full loop width across the displacement stroke.

### Scenario C: Diagnosing Dynamic Control Authority
- **Problem**: The difference between zero-field ($0.0\,\text{V}$) and full-field ($2.0\,\text{V}$) is too small.
- **Consultant Recommendation**:
  > - Compute dynamic force ratio $R = F_{\max}(2.0\,\text{V}) / F_{\max}(0.0\,\text{V})$.
  > - If $R < 3.0$, the off-state baseline parameters ($\alpha_a, c_{0a}, c_{1a}$) are dominating. Reduce zero-field viscosity $\alpha_a$ and increase field gain $\alpha_b$.
