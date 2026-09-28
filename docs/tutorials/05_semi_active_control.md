# 🏎️ Tutorial 05: Semi-Active Vibration Control Architectures

This tutorial explains how to apply the **Modified Bouc-Wen MR Damper** digital twin to vehicle suspension systems, focusing on Karnopp 2-State Skyhook control, Groundhook damping, and torque coordination.

---

## 1. Semi-Active Passivity Constraint

Unlike active actuators that can inject mechanical energy into a system ($F \cdot \dot{x}_{\text{rel}} < 0$), a Magnetorheological damper is strictly **semi-active and dissipative**:
$$F_{\text{damper}} \cdot \dot{x}_{\text{rel}} \ge 0 \qquad \text{where } \dot{x}_{\text{rel}} = \dot{x}_s - \dot{x}_u$$

The control system can only modulate the rate of energy dissipation by adjusting coil current / voltage ($V \in [0, V_{\max}]$).

---

## 2. Karnopp 2-State Skyhook Control Law

The classical Skyhook control strategy aims to hook the sprung mass (vehicle chassis $m_s$) to a fictional stationary sky anchor:

$$V_{\text{command}} = \begin{cases} 
V_{\max} & \text{if } \dot{x}_s \cdot (\dot{x}_s - \dot{x}_u) \ge 0 \quad \text{(Dissipative quadrant)} \\
V_{\min} & \text{if } \dot{x}_s \cdot (\dot{x}_s - \dot{x}_u) < 0 \quad \text{(Energy-injection quadrant)}
\end{cases}$$

### Implementation Logic in Python:
```python
def skyhook_2state(v_sprung: float, v_rel: float, v_max=2.0, v_min=0.0) -> float:
    """
    Karnopp 2-state skyhook control logic.
    """
    if v_sprung * v_rel >= 0.0:
        return v_max  # High damping when moving in opposite direction
    else:
        return v_min  # Low damping to allow free wheel motion
```

---

## 3. Continuous Skyhook & Groundhook

To mitigate control chatter, continuous modulation is implemented:

$$F_{\text{desired}} = C_{\text{sky}} \dot{x}_s$$

The inverse Spencer model or a feedback loop determines the command voltage $V$ that matches $F_d \approx F_{\text{desired}}$ within the damper's dynamic envelope.

For road-holding optimization (tire deflection control), Groundhook targets unsprung mass velocity:
$$F_{\text{ground}} = C_{\text{ground}} \dot{x}_u$$

---

## 4. Vehicle Suspension Benchmark Reference

For full 2-DOF quarter-car simulations, ISO bump profiles, and motor suspension torque coordination benchmarks, refer to our companion repository:
- **Core Library & Simulink Model**: [waqasmbaig/MRD-Modified-Bouc-Wen-Model](https://github.com/waqasmbaig/MRD-Modified-Bouc-Wen-Model)
- **Primary Journal Paper**: Yu, Luo, Wu, Baig, Ma, Hou, *IEEE Transactions on Transportation Electrification*, 2025. [DOI: 10.1109/TTE.2025.3535765](https://doi.org/10.1109/TTE.2025.3535765)
