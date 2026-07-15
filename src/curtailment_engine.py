import pandas as pd
import numpy as np
import pandapower as pp
from grid_model import create_constrained_33kv_network


def run_time_series_curtailment():
    """
    Simulates a 24-hour horizon under high wind generation and low load conditions.
    Dyanmically curtails wind output if thermal or voltage limits are violated.
    """
    # 1. Initialize the network model
    net = create_constrained_33kv_network()

    # 2. Generate a highly constrained 24-hour scenario
    # Low demand paired with a massive mid-day wind surge forces grid bottlenecks
    hours = np.arange(24)
    wind_profile = [
        10,
        12,
        15,
        18,
        22,
        25,
        28,
        30,
        30,
        30,
        30,
        30,
        30,
        28,
        25,
        22,
        18,
        15,
        12,
        10,
        8,
        7,
        6,
        5,
    ]  # MW
    load_profile = [
        12,
        11,
        10,
        9,
        8,
        8,
        9,
        11,
        12,
        13,
        12,
        11,
        11,
        12,
        13,
        14,
        16,
        18,
        19,
        17,
        15,
        14,
        13,
        12,
    ]  # MW

    # Storage for analytical logging
    results_log = []

    print("Executing 24-Hour Active Network Management Simulation...")

    for h in hours:
        # Step A: Inject baseline profiles for the current hour
        p_available_wind = wind_profile[h]
        net.load.at[0, "p_mw"] = load_profile[h]
        net.sgen.at[0, "p_mw"] = p_available_wind

        # Step B: Run initial Power Flow to check for natural bottlenecks
        try:
            pp.runpp(net)
        except pp.LoadflowNotConverged:
            print(
                f" Hour {h}: Power flow failed to converge due to extreme instability."
            )
            continue

        # Step C: Evaluate Network Health against UK Statutory Grid Standards
        v_pcc = net.res_bus.at[3, "vm_pu"]  # Wind Farm Bus Index = 3
        loading_f1 = net.res_line.at[0, "loading_percent"]  # Feeder 1 Index = 0

        curtailed_mw = 0.0
        p_actual_wind = p_available_wind

        # Step D: Dynamic Curtailment Loop (Iterative reduction to clear violations)
        # Violations: Voltage exceeding 1.06 pu OR Cable thermal loading exceeding 100%
        iteration = 0
        while (
            (v_pcc > 1.06 or loading_f1 > 100.0)
            and p_actual_wind > 0
            and iteration < 20
        ):
            # Step down wind generation by 0.5 MW increments until safe
            p_actual_wind -= 0.5
            p_actual_wind = max(0.0, p_actual_wind)
            net.sgen.at[0, "p_mw"] = p_actual_wind

            # Re-verify network response
            pp.runpp(net)
            v_pcc = net.res_bus.at[3, "vm_pu"]
            loading_f1 = net.res_line.at[0, "loading_percent"]
            iteration += 1

        curtailed_mw = p_available_wind - p_actual_wind

        # Log final metrics for the hour
        results_log.append(
            {
                "Hour": h,
                "Demand_MW": load_profile[h],
                "Wind_Available_MW": p_available_wind,
                "Wind_Actual_MW": p_actual_wind,
                "Curtailment_MW": curtailed_mw,
                "PCC_Voltage_pu": v_pcc,
                "Feeder_Loading_Pct": loading_f1,
            }
        )

    # 3. Process and Output Summary Statistics
    df_results = pd.DataFrame(results_log)
    total_curtailment = df_results["Curtailment_MW"].sum()
    max_loading = df_results["Feeder_Loading_Pct"].max()
    max_voltage = df_results["PCC_Voltage_pu"].max()

    print("\n--- Simulation Summary ---")
    print(f"Total Grid Curtailment over 24h: {total_curtailment:.2f} MWh")
    print(f"Peak Asset Thermal Loading:     {max_loading:.1f}%")
    print(f"Peak Operational Voltage:       {max_voltage:.3f} pu")

    return df_results


if __name__ == "__main__":
    df = run_time_series_curtailment()
