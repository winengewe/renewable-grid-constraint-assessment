# Renewable Integration & Grid Constraint Assessment Tool

An automated power system analysis tool built in Python using **Pandapower** to evaluate the connection viability of a new 30MW wind farm onto a constrained 33kV distribution network. 

This project simulates a real-world engineering workflow typical of network design consultancies, evaluating grid compliance against **UK Engineering Recommendation G99/G100 standards**.

## Project Overview
The objective of this study is to identify thermal and voltage bottlenecks caused by high renewable penetration over a time-series horizon, and implement an automated curtailment algorithm to maintain network security.

### Core Methodology
1. **Network Topology:** Programmatically constructs a radial 132/33kV substation feeding a local distribution network.
2. **Time-Series Simulation:** Evaluates network performance under fluctuating seasonal load profiles and localized wind generation data.
3. **Curtailment Optimization:** Implements an active management loop that dynamically scales back generation output when asset thermal capacities (100%) or statutory voltage limits (±6%) are breached.

## Repository Structure
* `/src/grid_model.py`: Core script to initialize the Pandapower network elements.
* `/notebooks/constraint_analysis.ipynb`: The main analytical notebook running the 24-hour simulation loops.
* `/data/`: Directory containing generation profiles and load curves.

## Key Technical Standards Referenced
* **Voltage Limits:** Statutory limits maintained at 33kV (0.94 pu to 1.06 pu) per UK regulations.
* **Thermal Limits:** Overhead line and underground cable ratings set to 100% maximum continuous capacity.
