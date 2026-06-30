# Interactive Physics Simulation & Learning Analytics Application

An interactive, web-based virtual laboratory application designed for Higher National Diploma (HND) Physics programs. This platform serves as a software-defined physics engine to model classical kinematics under quadratic atmospheric resistance across different planetary environments, while actively tracking student pedagogical metrics.

---

## 📌 Project Overview
In tertiary institutions, providing access to open-air ballistics labs or environments with varying gravitational fields and atmospheric fluid densities is physically impossible. 

This project bridges that gap by implementing an **Interactive Physics Simulation Layer** using Python and Streamlit. The application computes the non-linear differential equations of motion for a projectile experiencing quadratic fluid drag via Euler's numerical approximation method. Concurrently, an embedded **Learning Analytics Engine** logs student interaction telemetry data, mapping procedural variables tuning and problem-solving behaviors for academic evaluation.

---

## 🛠️ Features

* **Numerical Integration Physics Engine:** Evaluates two-dimensional kinematics under air resistance dynamically based on real-world fluid dynamics constraints.
* **Variable Planetary Environment Simulator:** Allows students to alter environmental gravity profiles, simulating flight on Earth, the Moon, Mars, or Jupiter.
* **Aerodynamic Drag Modeling:** Simulates quadratic atmospheric resistance ($C_d$) to visually demonstrate asymmetric trajectory degradation and energy dissipation.
* **Interactive Visual Workspace:** Uses responsive Plotly graphs to enable precise, vector-coordinate querying when hover paths are engaged.
* **Persistent Student Telemetry Log:** Captures and serializes parameter changes, timestamps, and evaluation scores asynchronously into a structured format.
* **Instructor Dashboard Portal:** Synthesizes aggregated data trends to show cohort interaction distributions and evaluate engagement styles.

---

## 📐 System Architecture

The application is structured into three unified tiers to maintain absolute separation of concerns:

```text
[Student Frontend UI Panel] <─── Session State ───> [Learning Analytics Tracker]
              │                                                    │
              ▼                                                    ▼
 [Mathematical Physics Engine]                     [Persistent Analytics CSV Database]
