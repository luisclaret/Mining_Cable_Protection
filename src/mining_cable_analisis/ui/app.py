import customtkinter as ctk # This will import customtkinter for creating the desktop application
import matplotlib.pyplot as plt # This will import matplotlib functionality to plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Import module to convert matplotlib plot into a customtkinter widget
from matplotlib.ticker import ScalarFormatter # Import formatter method of matplotlib
import numpy as np # Import numpy for data handling

from mining_cable_analisis.domain.curves import (intermediate_overload_cable_curve, short_circuit_cable_curve, u_protection_curve) # Import modules of the mining_cable_analysis library

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Mining Cable Analysis")
        self.geometry("1000x700")

        # Creates matplotlib figure (the "canvas" for the chart)
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # Embed the matplotlib figure into a Tkinter windows
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Create a button (does nothing yet)
        self.plot_button = ctk.CTkButton(self, text="Plot all curves", command=self.plot_all)
        self.plot_button.pack(pady=10)

        # Handle windows closing event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def plot_all(self):
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


        # Clear previous plot
        self.ax.clear()

        # Plot curves
        self.ax.plot(cable_ratios, cable_time, label="Cable Overload")
        self.ax.plot(short_ratios, short_times, label="Cable Short Circuit")
        self.ax.plot(relay_current, relay_time, label="Relay U3")

        # Configure plot
        self.ax.set_title("Coordination Plot")
        self.ax.set_xlabel("Multiple of pick-up current")
        self.ax.set_ylabel("Time (s)")
        self.ax.set_xscale("log")
        self.ax.set_yscale("log")
        # Change axis notation to regular numbers
        self.ax.xaxis.set_major_formatter(ScalarFormatter())
        self.ax.yaxis.set_major_formatter(ScalarFormatter())
        self.ax.grid(True, which="both", linestyle="-", linewidth=0.5, color="gray", alpha=0.5)
        self.ax.set_xlim(0.01, 1000)
        self.ax.set_ylim(0.01, 1000)
        self.ax.legend()
        
        # Redraw the canvas
        self.canvas.draw()


    def on_closing(self):
        plt.close(self.fig) # Close matplotlib figure
        self.quit() # Exit the main loop
        self.destroy() # Destroy the window


if __name__ == "__main__":
    app = App()
    app.mainloop()

        