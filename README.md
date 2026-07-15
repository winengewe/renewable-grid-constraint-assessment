# Active Network Management (ANM): Renewable Integration & Grid Constraint Assessment Tool

![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![pandapower](https://img.shields.io/badge/pandapower-orange?style=flat&logo=pandas&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)
![Pandas](https://img.shields.io/badge/pandas-%3E%3D2.0.0-150458?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%3E%3D1.24.0-013243?style=flat&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/matplotlib-%3E%3D3.7.0-ffffff?style=flat&logo=python&logoColor=11557c)

## 📌 Project Overview & Engineering Context
As the UK transitions toward Net Zero, distribution network operators (DNOs) face unprecedented thermal and voltage constraints due to the rapid connection of distributed generation (DG). Traditional "firm" connection agreements often require expensive, multi-year network reinforcement. 

This repository contains a professional-grade **Active Network Management (ANM)** simulation tool. Built in Python using the physics-based **pandapower** load-flow engine, it models a standard UK **132/33kV distribution sub-transmission network** to evaluate the connection viability of a proposed 30MW wind farm. The tool automates a 24-hour time-series simulation, evaluates network code compliance, and executes a dynamic, non-linear generation curtailment algorithm to prevent asset thermal degradation and overvoltage conditions.

---

## 🎯 Key Objectives
1. **Grid Compliance Modeling:** Assess a high-penetration renewable connection against statutory **UK Grid Code** and **Engineering Recommendation G99/G100 standards**.
2. **Constraint Bottleneck Identification:** Identify specific operating hours where low localized demand paired with peak wind generation results in thermal OHL/cable overloads (>100% rating) or statutory voltage rise breaches (>1.06 pu).
3. **Automated Active Management:** Implement a closed-loop Active Network Management (ANM) curtailment algorithm to dynamically trim renewable output to the maximum allowable hosting capacity of the grid in 0.5 MW increments.
4. **Commercial Impact Quantification:** Calculate total curtailed energy (MWh lost) over the simulation horizon to assist developers in evaluating the financial viability of a non-firm connection.

---

## 🛠️ Code Capabilities & Analytical Workflow
The codebase is decoupled into modular engineering blocks designed to automate a standard power systems consultancy workflow:

* **Deterministic Grid Modeling (`grid_model.py`):** Programmatically constructs a 4-bus radial network including a 132kV transmission slack bus, a 90MVA grid transformer, a 15km mixed copper/aluminium 33kV distribution feeder, localized municipal load, and the target renewable asset.
* **Time-Series Power Flow Engine (`curtailment_engine.py`):** Executes sequential AC Newton-Raphson power flow calculations across an hourly profile. It handles data frame injections via `pandas` to scale loads and generation dynamically.
* **Proportional Curtailment Feedback Loop:** If an asset breach is detected, the engine enters an iterative feedback loop, reducing the active power (P) output of the wind farm in 0.5MW steps. It re-solves the power flow continuously until the network returns to a secure operating state.
* **Visual Insight Generation (`visualize_results.py`):** Synthesizes power system telemetry into a dual-axis analytical plot, correlating physical asset loading thresholds directly with generation curtailment events.

---

## 📂 Repository Structure
```text
renewable-grid-constraint-assessment/
│
├── src/
│   ├── __init__.py              # Marks directory as an importable package
│   ├── grid_model.py            # Pandapower topology setup and custom line registration
│   ├── curtailment_engine.py    # Active Network Management loop and power flow controller
│   └── visualize_results.py     # Matplotlib publication-quality dual-axis plotting script
│
├── .gitignore                  # Project ignore rules
├── LICENSE                     # MIT License
├── network_curtailment_plot.png # Output visualization highlighting active grid management
├── README.md                    # Professional executive report and documentation
└── requirements.txt             # Project software dependencies
```
*(Note: Time-series generation and load profiles are declared directly in `curtailment_engine.py` for immediate execution.)*

---

## 🚀 How To Use & Execute

### 1. Prerequisites
Ensure you have Python 3.10 or higher installed. This project relies on `pandapower` (which utilizes the high-performance `scipy` wrapper for solving sparse matrix AC power flows) alongside standard data science libraries.

### 2. Installation
Clone the repository and install the required dependencies using pip:
```bash
git clone https://github.com/your-username/renewable-grid-constraint-assessment
cd renewable-grid-constraint-assessment
pip install -r requirements.txt
pip install matplotlib
```

### 3. Execution
Because the scripts inside `src/` use relative-style flat imports, you must add the `src` directory to your environment's search path when executing from the project root folder.

**On macOS/Linux:**
```bash
export PYTHONPATH=$(pwd)/src
python src/visualize_results.py
```

**On Windows (PowerShell):**
```powershell
$env:PYTHONPATH=".\src"
python src/visualize_results.py
```

**On Windows (Command Prompt):**
```cmd
set PYTHONPATH=src
python src/visualize_results.py
```

---

## 📊 Technical Standards & Asset Profiles
This simulation strictly grades network performance against established UK distribution standards:
* **Voltage Limits:** Maintained tightly between 0.94 pu and 1.06 pu at the 33kV point of common coupling (PCC), mapping to standard UK Distribution Network Operator (DNO) statutory bandwidths.
* **Thermal Limits:** Overhead lines and underground cables are constrained to a maximum of 100% continuous thermal rating. Any value exceeding 100% triggers instant ANM intervention to prevent thermal breakdown of cable insulation.

### Custom Physical Asset Registrations
Rather than using generic standard types, the grid model programmatically registers physical, representative UK distribution assets:
* **Feeder Section 1 (Substation to Mid-Line):** 10 km of 300 mm² Copper Cable (rated at 300 A continuous thermal current, R = 0.06 Ω/km, X = 0.11 Ω/km).
* **Feeder Section 2 (Mid-Line to Wind Farm PCC):** 5 km of 150 mm² Aluminum Cable (rated at 150 A continuous thermal current, R = 0.21 Ω/km, X = 0.11 Ω/km).
* **Main Grid Transformer:** 90 MVA 132/33 kV substation transformer (vk = 12.0%, vkr = 0.3%).

---

## 📈 Key Findings & Simulation Analysis
The active power management script evaluates a highly constrained scenario where a mid-day wind surge coincides with minimum industrial and domestic demand. 

### Simulation Summary Table
The grid's physical state transitions from an unmanaged, highly overloaded baseline to a perfectly stabilized active state:

| Parameter | Unmanaged Baseline Snapshot | Managed 24h Peak Performance | Action Taken |
| :--- | :---: | :---: | :--- |
| **Substation Voltage** | 1.0170 pu | 1.0186 pu | Normal operations within limits |
| **Wind Farm PCC Voltage** | 1.0494 pu | 1.0510 pu | Controlled safely below 1.060 pu limit |
| **Critical Cable Loading** | 83.06% | **100.0%** | **Dynamic Curtailment** activated to prevent overload |

### Executive Summary
* **Constraint Diagnosis:** The primary bottleneck on this network is strictly **thermal**. Under peak export conditions, the line loading would exceed safe cable operating capacities before statutory overvoltages (1.060 pu) are reached.
* **Mitigation Success:** The dynamic ANM closed-loop algorithm successfully restricts the peak loading of Feeder Section 1 to exactly **100.0%** of its continuous thermal rating. The peak operational voltage was safely maintained at **1.051 pu**.
* **Commercial Metrics:** Over the 24-hour cycle, the wind farm required only **4.50 MWh of active curtailment**. Out of a theoretical 24-hour yield of 432 MWh, this constitutes a minor **1.04% energy yield loss**. 
* **Investment Conclusion:** A curtailment rate of 1.04% is highly attractive. It demonstrates that a non-firm ANM connection is highly viable for the developer, completely bypassing the need for multi-million pound asset reinforcement or years of connection delays.

