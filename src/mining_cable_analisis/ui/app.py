import customtkinter as ctk # This will import customtkinter for creating the desktop application
import matplotlib.pyplot as plt # This will import matplotlib functionality to plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Import module to convert matplotlib plot into a customtkinter widget
from matplotlib.ticker import ScalarFormatter # Import formatter method of matplotlib
import numpy as np # Import numpy for data handling

from mining_cable_analisis.domain.curves import (intermediate_overload_cable_curve, short_circuit_cable_curve, protection_curve) # Import modules of the mining_cable_analysis library

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Mining Cable Analysis")
        self.geometry("1000x700")

        # Create tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.tab_add = self.tabview.add("Add Curve")
        self.tab_plot = self.tabview.add("Plot Curve")

        # Align tabs to left
        self.tabview._segmented_button.grid(sticky="W")

        # Add widget to tab 1 (Add curve)
        self._build_add_tab()

        # Add widget to tab 2 (Plot curve)
        self._build_plot_tab()

        # Handle windows closing event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)



    def _build_add_tab(self):
        # Widget for adding curves go here
        add_label = ctk.CTkLabel(master=self.tab_add, text="Add curve to the database", font=("Arial",20), fg_color="transparent")
        add_label.pack(side="top", fill="x")

        # Frame for curve name
        row_1 = ctk.CTkFrame(master=self.tab_add, fg_color="transparent") # Frame to organize rows of two columns
        row_1.pack(side="top", fill="x")
        # Row curve_name
        curve_name = ctk.CTkLabel(master=row_1, text="Curve Name: ", anchor="w", justify="left", font=("Arial", 12), fg_color="transparent")
        curve_name.pack(side="left", fill="x")
        curve_name_input = ctk.CTkEntry(master=row_1, placeholder_text="Enter curve name")
        curve_name_input.pack(side="left", fill="x")

        # Frame for protection type
        row_2 = ctk.CTkFrame(master=self.tab_add, fg_color="transparent") # Frame to organize rows of two columns
        row_2.pack(side="top", fill="x")
        # Row protection type
        protection_type = ctk.CTkLabel(master=row_2, text="Protection Type: ", anchor="w", justify="left", font=("Arial", 12), fg_color="transparent")
        protection_type.pack(side="left", fill="x")
        protection_type_dropdown = ctk.CTkOptionMenu(master=row_2, values=[], command=None)
        protection_type_dropdown.pack(side="left", fill="x")

        # Frame for curve type
        row_3 = ctk.CTkFrame(master=self.tab_add, fg_color="transparent") # Frame to organize rows of two columns
        row_3.pack(side="top", fill="x")
        # Row curve type
        curve_type = ctk.CTkLabel(master=row_3, text="Curve Type: ", anchor="w", justify="left", font=("Arial", 12), fg_color="transparent")
        curve_type.pack(side="left", fill="x")
        curve_type_dropdown = ctk.CTkOptionMenu(master=row_3, values=[], command=None)
        curve_type_dropdown.pack(side="left", fill="x")

        # Frame for equation
        row_4 = ctk.CTkFrame(master=self.tab_add, fg_color="transparent") # Frame to organize rows of two columns
        row_4.pack(side="top", fill="x")
        # Row for equation
        equation_question = ctk.CTkLabel(master=row_4, text="If Equation: ", anchor="w", justify="left", font=("Arial", 12), fg_color="transparent")
        equation_question.pack(side="left", fill="x")
        equation_answer = ctk.CTkCheckBox(master=row_4)
        equation_answer.pack(side="left", fill="x")

        # Frame for formula
        row_5 = ctk.CTkFrame(master=self.tab_add, fg_color="transparent") # Frame to organize rows of two columns
        row_5.pack(side="top", fill="x")
        # Row for formula
        formula_question = ctk.CTkLabel(master=row_5, text="Curve Name: ", anchor="w", justify="left", font=("Arial", 12), fg_color="transparent")
        formula_question.pack(side="left", fill="x")
        formula_answer = ctk.CTkEntry(master=row_5, placeholder_text="Enter curve equation")
        formula_answer.pack(side="left", fill="x")

        # Frame for discrete point
        row_6 = ctk.CTkFrame(master=self.tab_add, fg_color="transparent") # Frame to organize rows of two columns
        row_6.pack(side="top", fill="x")
        # Row for discrete point
        discrete_question = ctk.CTkLabel(master=row_6, text="If discrete points: ", anchor="w", justify="left", font=("Arial", 12), fg_color="transparent")
        discrete_question.pack(side="left", fill="x")
        discrete_answer = ctk.CTkCheckBox(master=row_6)
        discrete_answer.pack(side="left", fill="x")

        # Row for importing csv
        importing_csv_button = ctk.CTkButton(master=self.tab_add, text="Import CSV") 
        importing_csv_button.pack(side="top", anchor="w")

        # Row for saving to database
        save_db_button = ctk.CTkButton(master=self.tab_add, text="Save to the database")
        save_db_button.pack(side="top", anchor="w")

    def _build_plot_tab(self):
        # Widget for plotting go here
        plot_label = ctk.CTkLabel(master=self.tab_plot, text="Plot curve from the database", font=("Arial",20), fg_color="transparent")
        plot_label.pack(side="top", fill="x")

        # Frame for curve selection
        row_1 = ctk.CTkFrame(master=self.tab_plot, fg_color="transparent") # Frame to organize rows of two columns
        row_1.pack(side="top", fill="x")
        # Row curve selection
        curve_select = ctk.CTkLabel(master=row_1, text="Select Curve: ", anchor="w", justify="left", font=("Arial", 12), fg_color="transparent")
        curve_select.pack(side="left", fill="x")
        curve_selection = ctk.CTkOptionMenu(master=row_1, values=[], command=None)
        curve_selection.pack(side="left", fill="x")

        # Frame for time dial
        row_2 = ctk.CTkFrame(master=self.tab_plot, fg_color="transparent") # Frame to organize rows of two columns
        row_2.pack(side="top", fill="x")
        # Row time dial
        time_dial = ctk.CTkLabel(master=row_2, text="Time dial: ", anchor="w", justify="left", font=("Arial", 12), fg_color="transparent")
        time_dial.pack(side="left", fill="x")
        time_dial_input = ctk.CTkEntry(master=row_2, placeholder_text="Enter time dial")
        time_dial_input.pack(side="left", fill="x")

        # Frame for pick up current
        row_3 = ctk.CTkFrame(master=self.tab_plot, fg_color="transparent") # Frame to organize rows of two columns
        row_3.pack(side="top", fill="x")
        # Row pick up
        pick_up = ctk.CTkLabel(master=row_3, text="Pick up: ", anchor="w", justify="left", font=("Arial", 12), fg_color="transparent")
        pick_up.pack(side="left", fill="x")
        pick_up_input = ctk.CTkEntry(master=row_3, placeholder_text="Enter pick up setting")
        pick_up_input.pack(side="left", fill="x")
        pass

        # Creates matplotlib figure (the "canvas" for the chart)
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # Embed the matplotlib figure into a Tkinter windows
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_plot)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Create a button to plot
        self.plot_button = ctk.CTkButton(self.tab_plot, text="Plot all curves", command=self.plot_all)
        self.plot_button.pack(pady=10)

    

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
        curve_type = "U1" # Time curve to plot
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
        relay_current, relay_time = protection_curve(curve_type=curve_type, time_dial=time_dial, pick_up=pick_up)


        # Clear previous plot
        self.ax.clear()

        # Plot curves
        self.ax.plot(cable_ratios, cable_time, label="Cable Overload")
        self.ax.plot(short_ratios, short_times, label="Cable Short Circuit")
        self.ax.plot(relay_current, relay_time, label=f"Relay {curve_type}")

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

        