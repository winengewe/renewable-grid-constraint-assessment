import matplotlib.pyplot as plt
from curtailment_engine import run_time_series_curtailment

# 1. Run the simulation engine to generate data
df = run_time_series_curtailment()

# 2. Initialize the plot figure
fig, ax1 = plt.subplots(figsize=(11, 6), dpi=120)

# Color palette definition (clean and professional)
color_wind_avail = "#B0BEC5"  # Light Grey
color_wind_actual = "#1E88E5"  # Electric Blue
color_loading = "#D81B60"  # Deep Pink/Red

# --- Subplot 1: Power Generation Profiles (Left Axis) ---
ax1.set_xlabel("Time of Day (Hour)", fontsize=11, fontweight="bold", labelpad=10)
ax1.set_ylabel(
    "Wind Generation Power (MW)",
    fontsize=11,
    fontweight="bold",
    color=color_wind_actual,
)

# Plot available wind power vs actual delivered wind power
ax1.plot(
    df["Hour"],
    df["Wind_Available_MW"],
    label="Theoretical Available Wind",
    color=color_wind_avail,
    linestyle="--",
    linewidth=1.5,
)
ax1.plot(
    df["Hour"],
    df["Wind_Actual_MW"],
    label="Active Managed Wind (Delivered)",
    color=color_wind_actual,
    linewidth=2.5,
)

# Shade the area representing lost energy/curtailment
ax1.fill_between(
    df["Hour"],
    df["Wind_Actual_MW"],
    df["Wind_Available_MW"],
    where=(df["Curtailment_MW"] > 0),
    facecolor=color_loading,
    alpha=0.15,
    label="Energy Curtailed (MWh Lost)",
)

ax1.tick_params(axis="y", labelcolor=color_wind_actual)
ax1.set_xlim(0, 23)
ax1.set_xticks(range(0, 24, 2))
ax1.grid(True, linestyle=":", alpha=0.5)

# --- Subplot 2: Asset Loading Constraints (Right Axis) ---
ax2 = ax1.twinx()  # Share the same x-axis
ax2.set_ylabel(
    "Critical Feeder Cable Loading (%)",
    fontsize=11,
    fontweight="bold",
    color=color_loading,
)

# Plot the cable loading percentage
ax2.plot(
    df["Hour"],
    df["Feeder_Loading_Pct"],
    label="Feeder Cable Loading",
    color=color_loading,
    linewidth=2,
    linestyle="-.",
)

# Draw the 100% strict operating limit threshold line
ax2.axhline(
    100.0,
    color="black",
    linestyle=":",
    linewidth=1.5,
    alpha=0.8,
    label="Statutory Asset Capacity Limit (100%)",
)
ax2.tick_params(axis="y", labelcolor=color_loading)
ax2.set_ylim(0, 115)

# --- Legends & Layout Optimization ---
# Combine legends from both axes into a single box
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(
    lines1 + lines2,
    labels1 + labels2,
    loc="upper left",
    frameon=True,
    facecolor="white",
    edgecolor="none",
    shadow=True,
)

plt.title(
    "Automated Constraint Management: 30MW Wind Farm Active Grid Curtailment Loop",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
fig.tight_layout()

# Save the plot directly to the directory so you can link it into your README.md file
plt.savefig("network_curtailment_plot.png", bbox_inches="tight")
print(
    "\nSuccess: Saved analytical chart to root folder as 'network_curtailment_plot.png'"
)
plt.show()
