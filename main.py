
import matplotlib.pyplot as plt # Import matplotlib to plot
import numpy as np # Import numpy for working with data
from mining_cable_analisis.domain.curves import (intermediate_overload_cable_curve, short_circuit_cable_curve, u_protection_curve) # Importing the modules fo the program

def main():
    ## This program will assume that you are only going to plot the emergency overload curve of a 300 MCM cable assuming that it have been working at his nominal current prior to emergency just to test the function
    # Data for 300 MCM @ 25 kV
    To = 40.0 # Ambient temperature (Centigrades)
    Tn = 90.0 # Conductor normal operating temperature at nominal current (Centigrades)
    Te = 130.0 # Conductor emergency operating temperature (Centigrades)
    K_constant = 2.5 # Constant for 300 MCM conductor in conduit in air
    conductor_type = "copper" # Material of the cable (copper or aluminum)
    time = np.arange(18000, 9, -1) # Time stamp (seconds)
    # time = list(range(18000, 9, -1)) # Time stamp (seconds)
    Io = 402.0 # Conductor operating current prior to emergency current (A)
    In = 402.0 # Conductor nominal current (A)


    ## This part of the program will calculate the short circuit cable curve for a 300 MCM cable
    cm = 300 # Effective cross sectional area of the shield (kcmils)
    Ts = 250 # Maximum short circuit allowed temperature
    

    ## This part of the program will calculate a protection curve for a U.S. U3 curve
    curve_type = "U3" # Time curve to plot
    time_dial = 10 # Time dial setting of the relay
    pick_up_current = In
    pick_up = (pick_up_current, "primary") # Pick up setting of the relay. Clarifying if the information is giving in secondary or primary current
    

    # Data to plot the overload cable curve
    cable_currents, cable_time = intermediate_overload_cable_curve(To=To, Tn=Tn, Te=Te, Io=Io, In=In, K=K_constant, time=time, conductor_type=conductor_type)
    cable_ratios = cable_currents / pick_up_current # Cable current in multiples of pick up current


    # Data to plot short circuit cable curve
    short_circuit_currents, short_times = short_circuit_cable_curve(cm=cm, Tn=Tn, Ts=Ts, conductor_type=conductor_type)
    short_ratios = short_circuit_currents / pick_up_current # Short circuit cable current in multiples of pick up current


    # Data to plot the protection time curve
    relay_current, relay_time = u_protection_curve(curve_type=curve_type, time_dial=time_dial, pick_up=pick_up)

    # Plotting
    plt.figure() # This creates a new figure, so we can plot the two curves in the same graph

    # Plot overload curve
    plt.plot(cable_ratios, cable_time) # Plot some data on the axes (overload damage curve)

    # Plot shortcircuit curve
    plt.plot(short_ratios, short_times)

    # Data to plot the protection curve
    plt.plot(relay_current, relay_time) # Plot some data on the axes (protection curve)

    # Plotting the curve with the two graphics
    plt.title("Coordination Plot")
    plt.xlabel("Multiples of pick-up current")
    plt.ylabel("Time (s)")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="-", linewidth=0.5, color="gray", alpha=0.5)
    plt.xlim(0.01, 1000)
    plt.ylim(0.01, 1000)

    plt.show() # Show the figure


if __name__ == "__main__":
    main()
