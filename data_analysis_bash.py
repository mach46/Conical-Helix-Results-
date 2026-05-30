import os
from cmath import sqrt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from CoolProp.CoolProp import PropsSI
import matplotlib

matplotlib.use('Agg')

# test code
diameters = ["d2", "d3", "d4", "d5"]
rpms = ["5k", "10k", "15k", "20k", "25k", "30k", "35k", "40k", "45k", "50k", "55k", "60k", "65k", "70k"]

skip_cases = [
    ("d5", "70k"),
    ("d5", "65k"),
    ("d5", "60k"),
    ("d5", "55k"),
    ("d5", "50k"),
    ("d4", "70k"),
    ("d4", "65k"),
    ("d4", "60k"),
    ("d4", "55k"),
    ("d3", "70k"),
    ("d3", "65k"),
    ("d2", "70k"),
]

fluid = "Methane"

results = []

base_path = r"/scratch/24cr60r06/dhairya/data_files/extracted_data"
extracted_base = "/scratch/24cr60r06/dhairya/data_files/extracted_data/data_analysis"

output_csv = os.path.join(extracted_base, "power_efficiency_results.csv")
nsds_chart = os.path.join(extracted_base, "ns_ds_chart.png")
performance_chart = os.path.join(extracted_base, "power_vs_efficiency.png")
enthalpy_chart = os.path.join(extracted_base, "enthalpy_drop_vs_efficiency.png")
power_rpm_chart = os.path.join(extracted_base, "power_vs_rpm.png")
delta_ht_vs_ang_mom = os.path.join(extracted_base, "delta_ht_vs_ang_mom.png")
torque_vs_blade_speed_ratio = os.path.join(extracted_base, "torque_vs_blade_speed_ratio.png")
power_vs_blade_speed_ratio = os.path.join(extracted_base, "power_vs_blade_speed_ratio.png")
efficiency_tt_vs_blade_speed_ratio = os.path.join(extracted_base, "efficiency_vs_blade_speed_ratio.png")
pi1_chart = os.path.join(extracted_base, "efficiency_vs_flow_coefficient.png")
pi2_chart = os.path.join(extracted_base, "efficiency_vs_loading_coefficient.png")
pi3_chart = os.path.join(extracted_base, "efficiency_vs_pressure_coefficient.png")
pi3_chart_rpm = os.path.join(extracted_base, "efficiency_vs_pressure_coefficient_rpm.png")
pi4_chart = os.path.join(extracted_base, "efficiency_vs_rotational_reynolds_number.png")
pi1_vs_pi2_chart = os.path.join(extracted_base, "flow_coefficient_vs_loading_coefficient.png")
torque_force_ratio_x_vs_rpm = os.path.join(extracted_base, "torque_force_ratio_x_vs_rpm.png")
torque_d_vs_torque_e = os.path.join(extracted_base, "torque_d_vs_torque_e.png")

# Variables to plot
variables_to_plot = [
    "Pressure",
    "Velocity (mwa)",
    "Temperature",
    "Entropy",
    "Density (mwa)",
    "Mach Number (mwa)"
]


def plot_vs_rpm(
        df,
        y_column,
        ylabel,
        title,
        filename,
        scale=1,
        annotate=False
):
    plt.figure(figsize=(8, 6))

    for diameter in df["Diameter"].unique():

        subset = (
            df[df["Diameter"] == diameter]
            .sort_values("RPM_num")
        )

        plt.plot(
            subset["RPM_num"],
            subset[y_column] * scale,
            marker=marker_map[diameter],
            color=color_map[diameter],
            markersize=8,
            linewidth=1.5,
            label=diameter
        )

        if annotate:
            for _, row in subset.iterrows():
                plt.annotate(
                    f'{row[y_column]:.0f}',
                    (row["RPM_num"], row[y_column]),
                    fontsize=8,
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha="center"
                )

    plt.xlabel("RPM")
    plt.ylabel(ylabel)
    plt.title(title)

    plt.grid(True)
    plt.legend(title="Diameter")

    plt.savefig(
        os.path.join(extracted_base, filename),
        dpi=300,
        bbox_inches='tight',
        pad_inches=0.3
    )

    plt.close()


for diameter in diameters:

    for rpm in rpms:

        if (diameter, rpm) in skip_cases:
            continue

        filename_sp = f"{base_path}/statepoint_data/rotation_{diameter}_{rpm}_state_point_data.csv"

        # Rotor diameter map
        diameter_map = {
            "d2": 0.017711374999993368 * 2,
            "d3": 0.02102387500000713 * 2,
            "d4": 0.024020000000021437 * 2,
            "d5": 0.026768000000034556 * 2
        }

        D = diameter_map[diameter]
        D_mean = (D + 0.02) / 2

        try:
            df_sp = pd.read_csv(filename_sp)
            diameter_value = float(diameter.replace("d", "")) / 1000
            rpm_value = float(rpm.replace("k", "")) * 1000

            mdot = abs(df_sp["mdot"][0])

            vin = df_sp["vin"][0]
            vout = df_sp["vout"][0]

            Pin = df_sp["Pin"][0]
            Pout = df_sp["Pout"][0]

            P0in = df_sp["P0in"][0]
            P0out = df_sp["P0out"][0]

            Tin = df_sp["Tin"][0]
            Tout = df_sp["Tout"][0]

            T0in = df_sp["T0in"][0]
            T0out = df_sp["T0out"][0]

            htin = df_sp["htin"][0]
            htout = df_sp["htout"][0]

            hin = df_sp["hin"][0]
            hout = df_sp["hout"][0]

            sin = df_sp["sin"][0]
            sout = df_sp["sout"][0]

            muin = df_sp["muin"][0]
            muout = df_sp["muout"][0]

            rhoin = df_sp["rhoin"][0]
            rhoout = df_sp["rhoout"][0]

            Min = df_sp["Min"][0]
            Mout = df_sp["Mout"][0]

            VThetain = df_sp["VThetain"][0]
            VThetaout = df_sp["VThetaout"][0]

            Tx = df_sp["Tx"][0]
            Ty = df_sp["Ty"][0]
            Tz = df_sp["Tz"][0]

            Fx = df_sp["Fx"][0]
            Fy = df_sp["Fy"][0]
            Fz = df_sp["Fz"][0]

            tau_w = df_sp["tau_w"][0]

            Tp = df_sp["Tp"][0]
            Tv = df_sp["Tv"][0]
            Ttotal = df_sp["Ttotal"][0]

            # isentropic outlet enthalpy
            h_out_s = PropsSI('H', 'P', Pout, 'S', sin, fluid)
            h_out_ts = PropsSI('H', 'P', P0out, 'S', sin, fluid)

            # enthalpy drops
            delta_h_actual = htin - htout
            delta_h_isentropic_ts = htin - h_out_s
            delta_h_isentropic_tt = htin - h_out_ts

            # efficiency
            eta_ts = delta_h_actual / delta_h_isentropic_ts
            eta_tt = delta_h_actual / delta_h_isentropic_tt

            # Torque magnitude
            torque_t = abs(Tz)
            # torque_t = Tz

            # Force and torque magnitude
            force = abs(sqrt(Fx ** 2 + Fy ** 2))
            torque_f = force * D_mean / 2

            # Torque derived
            torque_d = Ttotal

            # Torque euler
            torque_e = mdot * (((D / 2) * VThetain) - (0.01 * VThetaout))

            # Angular velocity
            omega = 2 * np.pi * rpm_value / 60

            Uin = omega * D / 2
            Uout = omega * 0.01

            ang_mom = Uin * VThetain - Uout * VThetaout

            # Shaft power
            shaft_work_t = torque_t * omega
            shaft_work_f = torque_f * omega
            shaft_work_d = torque_d * omega
            shaft_work_e = torque_e * omega

            # Fluid power
            fluid_work = mdot * (htin - htout)

            # Efficiency
            eff_t = shaft_work_t / fluid_work
            eff_f = shaft_work_f / fluid_work
            eff_d = shaft_work_d / fluid_work
            eff_e = shaft_work_e / fluid_work

            # Volume flow rate
            Q = mdot / rhoin

            # Specific enthalpy drop
            delta_ht = htin - htout

            # Specific speed
            Ns = omega * np.sqrt(Q) / (delta_ht ** 0.75)

            # Specific diameter
            Ds = D_mean * (delta_ht ** 0.25) / np.sqrt(Q)

            # Blade Speed / Channel speed
            U = omega * (D_mean / 2)

            # Relative Velocity
            win = vin - U
            wout = vout - U

            # Blade speed ratio
            Bin = U / vin
            Bout = U / vout

            # Total Pressure drop
            delta_pt = P0in - P0out

            # Static Pressure Drop
            delta_p = Pin - Pout

            # Total Temperature drop
            delta_t0 = T0in - T0out

            # Static Temperature Drop
            delta_t = Tin - Tout

            # Torque Force Ratio
            TFRx = Tx / Fx
            TFRy = Ty / Fy
            TFRz = Tz / Fz

            # Check order of torque from this
            torque_c = mdot * delta_ht / omega

            Tr = Tp / Tv
            Tr = abs(Tr)

            delta_ht_torque = Ttotal * omega / mdot
            h_ratio = delta_h_actual / delta_ht_torque

            # Buckingham pi terms
            # Flow coefficient
            pi1 = mdot / ((D_mean ** 3) * omega * rhoin)

            # Loading coefficient
            pi2 = delta_ht / ((D_mean ** 2) * omega ** 2)

            # Expansion coefficient or non-dimensional pressure drop
            pi3 = delta_pt / ((D_mean ** 2) * omega ** 2 * rhoin)

            # Inverse rotational Reynolds number
            pi4 = muin / ((D_mean ** 2) * omega * rhoin)

            # Store results
            results.append({
                "Mdot": mdot,
                "Diameter": diameter,
                "RPM": rpm,
                "Diameter_value": diameter_value,
                "RPM_value": rpm_value,
                "Omega": omega,
                "Mean Radius": D_mean / 2,
                "Total Pressure drop": delta_pt,
                "Static Pressure drop": delta_p,
                "Total Temperature drop": delta_t0,
                "Static Temperature drop": delta_t,
                "Total Enthalpy drop": delta_ht,
                "Inlet Total Pressure": P0in,
                "Outlet Total Pressure": P0out,
                "Inlet Total Temperature": T0in,
                "Outlet Total Temperature": T0out,
                "Inlet Total Enthalpy": htin,
                "Outlet Total Enthalpy": htout,
                "Inlet Static Pressure": Pin,
                "Outlet Static Pressure": Pout,
                "Inlet Static Temperature": Tin,
                "Outlet Static Temperature": Tout,
                "Inlet Static Enthalpy": hin,
                "Outlet Static Enthalpy": hout,
                "Inlet Density": rhoin,
                "Outlet Density": rhoout,
                "Inlet Absolute Velocity": vin,
                "Outlet Absolute Velocity": vout,
                "Inlet Relative Velocity": win,
                "Outlet Relative Velocity": wout,
                "Blade Speed": U,
                "Inlet Blade Speed Ratio": Bin,
                "Outlet Blade Speed Ratio": Bout,
                "Inlet Mach Number": Min,
                "Outlet Mach Number": Mout,
                "Torque_t": torque_t,
                "Torque_f": torque_f,
                "Torque_d": torque_d,
                "Torque_c": torque_c,
                "Torque_e": torque_e,
                "Power_t": shaft_work_t,
                "Power_f": shaft_work_f,
                "Power_d": shaft_work_d,
                "Power_e": shaft_work_e,
                "Fluid Power": fluid_work,
                "Wall Shear Stress": tau_w,
                "Shaft_efficiency_t": eff_t,
                "Shaft_efficiency_f": eff_f,
                "Shaft_efficiency_d": eff_d,
                "Angular Momentum": ang_mom,
                "Efficiency Total-to-Static": eta_ts,
                "Efficiency Total-to-Total": eta_tt,
                "Torque Force Ratio X": TFRx,
                "Torque Force Ratio Y": TFRy,
                "Torque Force Ratio Z": TFRz,
                "Torque ratio (Tp/Tv)": Tr,
                "Enthalpy drop ratio": h_ratio,
                "Ns": Ns,
                "Ds": Ds,
                "pi1": pi1,
                "pi2": pi2,
                "pi3": pi3,
                "pi4": pi4
            })

        except FileNotFoundError:
            print(f"File not found: {filename_sp}")

results_df = pd.DataFrame(results)
results_df.to_csv(output_csv, index=False)

marker_map = {
    "d2": "o",
    "d3": "s",
    "d4": "^",
    "d5": "D"
}

color_map = {
    "d2": "C0",
    "d3": "C1",
    "d4": "C2",
    "d5": "C3"
}

results_df["RPM_num"] = (
        results_df["RPM"]
        .str.replace("k", "", regex=False)
        .astype(int) * 1000
)

# ----------------------------------------
# Ns-Ds plot
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():

    subset = results_df[results_df["Diameter"] == diameter]

    # Sort by RPM for proper connection
    # subset = subset.sort_values("RPM")

    plt.plot(
        subset["Ns"],
        subset["Ds"],
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )

    # Add text near each point
    for _, row in subset.iterrows():
        # Efficiency label
        plt.text(
            row["Ns"] - 0.002,
            row["Ds"],
            f'{row["Efficiency Total-to-Total"] * 100:.1f}%',
            fontsize=8,
            ha='right',
            va='center'
        )

        # RPM label
        plt.text(
            row["Ns"] + 0.002,
            row["Ds"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='top'
        )

plt.xlabel("Specific Speed (Ns)")
plt.ylabel("Specific Diameter (Ds)")
plt.title("Ns-Ds Chart")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    nsds_chart,
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.3
)
plt.close()

# ----------------------------------------
# Power vs Efficiency
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():

    subset = results_df[results_df["Diameter"] == diameter]

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["Power_d"],
        marker=marker_map[diameter],
        color=color_map[diameter],
        markersize=8,
        linewidth=1.5,
        label=diameter
    )

    # Add RPM labels
    for _, row in subset.iterrows():
        plt.annotate(
            f'{row["RPM"]}',
            (
                row["Efficiency Total-to-Total"] * 100,
                row["Power_d"]
            ),
            fontsize=8,
            xytext=(-10, 5),
            textcoords="offset points",
            ha="center"
        )

plt.xlabel("Efficiency Total-to-Total (%)")
plt.ylabel("Power (W)")
plt.title("Power vs Efficiency")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    performance_chart,
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.3
)
plt.close()

# ----------------------------------------
# Enthalpy drop vs Efficiency
# One plot per diameter
# ----------------------------------------
for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
        ]

    plt.figure(figsize=(8, 6))

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["Total Enthalpy drop"],
        marker=marker_map[diameter],
        color=color_map[diameter],
        markersize=8,
        linewidth=1.5
    )

    for _, row in subset.iterrows():
        plt.text(
            row["Efficiency Total-to-Total"] * 100,
            row["Total Enthalpy drop"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

    plt.xlabel("Efficiency Total-to-Total (%)")
    plt.ylabel("Total Enthalpy Drop (J/kg)")
    plt.title(f"Total Enthalpy Drop vs Efficiency ({diameter})")

    plt.grid(True)

    plt.savefig(
        enthalpy_chart.replace(
            ".png",
            f"_{diameter}.png"
        ),
        dpi=300,
        bbox_inches='tight',
        pad_inches=0.3
    )

    plt.close()

plot_vs_rpm(
    results_df,
    "Enthalpy drop ratio",
    "Enthalpy drop ratio (del_h / del_h_Ttotal)",
    "Enthalpy drop ratio (del_h / del_h_Ttotal) vs RPM",
    "enthalpy_drop_ratio_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Torque ratio (Tp/Tv)",
    "Torque ratio (Tp/Tv)",
    "Torque ratio (Tp/Tv) vs RPM",
    "torque_ratio_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Shaft_efficiency_d",
    "Shaft Efficiency (%)",
    "Shaft Efficiency (from Ttotal)vs RPM",
    "Shaft_efficiency_d_vs_rpm.png",
    scale=100
)

plot_vs_rpm(
    results_df,
    "Total Pressure drop",
    "Total Pressure drop (Pa)",
    "Total Pressure drop vs RPM",
    "total_pressure_drop_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Static Pressure drop",
    "Static Pressure drop (Pa)",
    "Static Pressure drop vs RPM",
    "static_pressure_drop_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Total Temperature drop",
    "Total Temperature drop (K)",
    "Total Temperature drop vs RPM",
    "total_temperature_drop_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Static Temperature drop",
    "Static Temperature drop (K)",
    "Static Temperature drop vs RPM",
    "static_temperature_drop_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Total Enthalpy drop",
    "Total Enthalpy drop (J/kg)",
    "Total Enthalpy drop vs RPM",
    "total_enthalpy_drop_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Torque_d",
    "Total Torque (N·m) (Tp+Tv)",
    "Torque vs RPM",
    "torque_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Torque_c",
    "Torque (N·m)",
    "Torque vs RPM",
    "torque_check_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Torque_e",
    "Torque (N·m)",
    "Torque (Euler equation) vs RPM",
    "torque_euler_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Torque_t",
    "Torque (N·m)",
    "Torque (CFD post) vs RPM",
    "torque_cfdpost_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Power_d",
    "Power (W)",
    "Power vs RPM",
    "power_vs_rpm.png",
    annotate=True
)

plot_vs_rpm(
    results_df,
    "Torque Force Ratio X",
    "Torque Force Ratio X",
    "Torque Force Ratio X vs RPM",
    "torque_force_ratio_x_vs_rpm.png"
)
plot_vs_rpm(
    results_df,
    "Torque Force Ratio Y",
    "Torque Force Ratio Y",
    "Torque Force Ratio Y vs RPM",
    "torque_force_ratio_y_vs_rpm.png"
)
plot_vs_rpm(
    results_df,
    "Torque Force Ratio Z",
    "Torque Force Ratio Z",
    "Torque Force Ratio Z vs RPM",
    "torque_force_ratio_z_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "Efficiency Total-to-Total",
    "Efficiency Total-to-Total (%)",
    "Efficiency vs RPM",
    "efficiency_tt_vs_rpm.png",
    scale=100
)

plot_vs_rpm(
    results_df,
    "Efficiency Total-to-Static",
    "Efficiency Total-to-Static (%)",
    "Efficiency vs RPM",
    "efficiency_ts_vs_rpm.png",
    scale=100
)

plot_vs_rpm(
    results_df,
    "Wall Shear Stress",
    "Wall Shear Stress (Pa)",
    "Wall Shear Stress vs RPM",
    "wall_shear_stress_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "pi1",
    "Flow coefficient",
    "Flow coefficient vs RPM",
    "flow_coefficient_vs_rpm.png"
)

plot_vs_rpm(
    results_df,
    "pi2",
    "Loading coefficient",
    "Loading coefficient vs RPM",
    "loading_coefficient_vs_rpm.png"
)

# ----------------------------------------
# Enthalpy drop vs Angular Momentum
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():
    """subset = (
        results_df[results_df["Diameter"] == diameter]
        .sort_values("Angular Momentum")
    )"""

    plt.plot(
        subset["Torque_d"],
        subset["Torque_e"],
        marker=marker_map[diameter],
        color=color_map[diameter],
        markersize=8,
        linewidth=1.5,
        label=diameter
    )

plt.xlabel("Torque total")
plt.ylabel("Torque euler")
plt.title("Torque euler vs Torque total")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    torque_d_vs_torque_e,
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Enthalpy drop vs Angular Momentum
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():
    subset = (
        results_df[results_df["Diameter"] == diameter]
        .sort_values("Angular Momentum")
    )

    plt.plot(
        subset["Angular Momentum"],
        subset["Total Enthalpy drop"],
        marker=marker_map[diameter],
        color=color_map[diameter],
        markersize=8,
        linewidth=1.5,
        label=diameter
    )

plt.xlabel("Angular Momentum")
plt.ylabel("Total Enthalpy drop")
plt.title("Total Enthalpy drop vs Angular Momentum")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    delta_ht_vs_ang_mom,
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Torque vs Inlet Blade Speed Ratio
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():
    subset = (
        results_df[results_df["Diameter"] == diameter]
        .sort_values("Inlet Blade Speed Ratio")
    )

    plt.plot(
        subset["Inlet Blade Speed Ratio"],
        subset["Torque_d"],
        marker=marker_map[diameter],
        color=color_map[diameter],
        markersize=8,
        linewidth=1.5,
        label=diameter
    )

plt.xlabel("Inlet Blade Speed Ratio")
plt.ylabel("Torque (N·m)")
plt.title("Torque vs Inlet Blade Speed Ratio")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    torque_vs_blade_speed_ratio,
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Power vs Inlet Blade Speed Ratio
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():
    subset = (
        results_df[results_df["Diameter"] == diameter]
        .sort_values("Inlet Blade Speed Ratio")
    )

    plt.plot(
        subset["Inlet Blade Speed Ratio"],
        subset["Power_d"],
        marker=marker_map[diameter],
        color=color_map[diameter],
        markersize=8,
        linewidth=1.5,
        label=diameter
    )

plt.xlabel("Inlet Blade Speed Ratio")
plt.ylabel("Power (W)")
plt.title("Power vs Inlet Blade Speed Ratio")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    power_vs_blade_speed_ratio,
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Efficiency tt vs Inlet Blade Speed Ratio
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():
    subset = (
        results_df[results_df["Diameter"] == diameter]
        .sort_values("Inlet Blade Speed Ratio")
    )

    plt.plot(
        subset["Inlet Blade Speed Ratio"],
        subset["Efficiency Total-to-Total"],
        marker=marker_map[diameter],
        color=color_map[diameter],
        markersize=8,
        linewidth=1.5,
        label=diameter
    )

plt.xlabel("Inlet Blade Speed Ratio")
plt.ylabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency Total-to-Total vs Inlet Blade Speed Ratio")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    efficiency_tt_vs_blade_speed_ratio,
    dpi=300,
    bbox_inches='tight',
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Efficiency vs Flow Coefficient (pi1)
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
        ]

    # Optional: sort by RPM
    subset = subset.sort_values("RPM_value")

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["pi1"],
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )

    # Add RPM labels
    for _, row in subset.iterrows():
        plt.text(
            row["pi1"],
            row["Efficiency Total-to-Total"] * 100,
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

plt.ylabel("Flow Coefficient ($\\pi_1$)")
plt.xlabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency vs Flow Coefficient")

equation_text = (
    r"$\pi_1 = \frac{\dot{m}}{d^3 \, \omega \, \rho_{in}}$"
)

plt.text(
    0.15, 0.95,  # x,y in axes coordinates
    equation_text,
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=1
    )
)

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    pi1_chart,
    dpi=300,
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Efficiency vs Loading Coefficient (pi2)
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
        ]

    # Optional: sort by RPM
    subset = subset.sort_values("RPM_value")

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["pi2"],
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )

    # Add RPM labels
    for _, row in subset.iterrows():
        plt.text(
            row["Efficiency Total-to-Total"] * 100,
            row["pi2"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

plt.ylabel("Loading Coefficient ($\\pi_2$)")
plt.xlabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency vs Loading Coefficient")

equation_text = (
    r"$\pi_2 = \frac{\Delta h_0}{d^2 \, \omega^2}$"
)

plt.text(
    0.15, 0.95,  # x,y in axes coordinates
    equation_text,
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=1
    )
)

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    pi2_chart,
    dpi=300,
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Efficiency vs Pressure Coefficient (pi3)
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
        ]

    # Optional: sort by RPM
    subset = subset.sort_values("RPM_value")

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["pi3"],
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )

    plt.yscale("log")

    # Add RPM labels
    for _, row in subset.iterrows():
        plt.text(
            row["Efficiency Total-to-Total"] * 100,
            row["pi3"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

plt.ylabel("Pressure Coefficient ($\\pi_3$)")
plt.xlabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency vs Pressure Coefficient")

equation_text = (
    r"$\pi_3 = \frac{\Delta P_0}{d^2 \, \omega^2 \, \rho_{in}}$"
)

plt.text(
    0.15, 0.95,  # x,y in axes coordinates
    equation_text,
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=1
    )
)

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    pi3_chart,
    dpi=300,
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Efficiency vs Rotational Reynolds number (pi4)
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
        ]

    # Optional: sort by RPM
    subset = subset.sort_values("RPM_value")

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["pi4"] ** (-1),
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )
    plt.yscale("log")

    # Add RPM labels
    for _, row in subset.iterrows():
        plt.text(
            row["Efficiency Total-to-Total"] * 100,
            row["pi4"] ** (-1),
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

plt.ylabel("Rotational Reynolds number ($\\pi_4^{-1}$)")
plt.xlabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency vs Rotational Reynolds number")

equation_text = (
    r"$\pi_4^{-1} = \frac{D_{mean}^2 \, \omega \, \rho}{\mu}$"
)

plt.text(
    0.15, 0.95,  # x,y in axes coordinates
    equation_text,
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=1
    )
)

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    pi4_chart,
    dpi=300,
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Flow Coefficient (pi1) vs Loading Coefficient (pi2)
# ----------------------------------------
plt.figure(figsize=(8, 6))

for diameter in results_df["Diameter"].unique():

    subset = results_df[
        results_df["Diameter"] == diameter
        ]

    # Optional: sort by RPM
    subset = subset.sort_values("RPM_value")

    plt.plot(
        subset["pi1"],
        subset["pi2"],
        marker=marker_map[diameter],
        linewidth=1.5,
        markersize=7,
        label=diameter
    )
    plt.xscale("log")
    plt.yscale("log")

    # Add RPM labels
    for _, row in subset.iterrows():
        plt.text(
            row["pi1"],
            row["pi2"],
            f'{row["RPM"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

plt.ylabel("Flow Coefficient ($\\pi_1$)")
plt.xlabel("Loading Coefficient ($\\pi_2$)")
plt.title("Flow Coefficient vs Loading Coefficient")

plt.grid(True)
plt.legend(title="Diameter")

plt.savefig(
    pi1_vs_pi2_chart,
    dpi=300,
    pad_inches=0.3
)

plt.close()

# ----------------------------------------
# Efficiency vs Pressure Coefficient (pi3)
# grouped by RPM
# ----------------------------------------
plt.figure(figsize=(8, 6))

# Marker map for RPMs
marker_map = {
    5000.0: "o",
    10000.0: "s",
    15000.0: "^",
    20000.0: "D",
    25000.0: "v",
    30000.0: "P",
    35000.0: "X",
    40000.0: "*",
    45000.0: "<",
    50000.0: ">",
    55000.0: "h",
    60000.0: "H",
    65000.0: "8",
    70000.0: "p"
}

for rpm in results_df["RPM_value"].unique():

    subset = results_df[
        results_df["RPM_value"] == rpm
        ]

    # Sort by diameter
    subset = subset.sort_values("Diameter_value")

    plt.plot(
        subset["Efficiency Total-to-Total"] * 100,
        subset["pi3"],
        marker=marker_map[rpm],
        linewidth=1.5,
        markersize=7,
        label=f"{int(rpm / 1000)}k"
    )

    # Add diameter labels
    for _, row in subset.iterrows():
        plt.text(
            row["Efficiency Total-to-Total"] * 100,
            row["pi3"],
            f'{row["Diameter"]}',
            fontsize=8,
            ha='left',
            va='bottom'
        )

# Log scale for pi3 axis
plt.yscale("log")

plt.ylabel("Pressure Coefficient ($\\pi_3$)")
plt.xlabel("Efficiency Total-to-Total (%)")
plt.title("Efficiency vs Pressure Coefficient")

# Equation textbox
equation_text = (
    r"$\pi_3 = \frac{\Delta P_0}{D^2 \, \omega^2 \, \rho_{in}}$"
)

plt.text(
    0.15, 0.95,
    equation_text,
    transform=plt.gca().transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=1
    )
)

plt.grid(True)
plt.legend(title="RPM")

plt.savefig(
    pi3_chart_rpm,
    dpi=300,
    pad_inches=0.3
)

plt.close()

