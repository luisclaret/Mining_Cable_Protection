
import matplotlib.pyplot as plt # Import matplotlib to plot
import numpy as np # Import numpy for working with data

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
    plt.xlim(0.01, 100000)
    plt.ylim(0.01, 100000)

    plt.show() # Show the figure



def intermediate_overload_cable_curve(To: float, Tn: float, Te: float, Io: float, In: float, K: float, time: np.array, conductor_type: str="average") -> tuple:
    '''
    The formula is the following from IEEE 3004.7 - 2021
    percentage = math.sqrt((((Te - To) / (Tn - To)) - (math.pow(Io / In, 2) * math.exp(-(delta/3600)/K)))/(1-math.exp(-(delta/3600)/K))*((230 + Tn)/(230 + Te))) 
    Where:
    Ie -> Emergency operating current rating
    In -> Normal current rating
    Io -> Operating current prior to emergency
    Te -> Conductor emergency operating temperature
    Tn -> Conductor normal operating temperature
    To -> Ambient temperature
    K -> Constant, dependent on cable size and installation type
    230 -> Zero-resistance temperature value (Average value. For copper use 234, for aluminum use 228)
    e -> Base for natural logarithms
    delta -> Time (seconds)
    '''
    # nominal_percentage = []
    seconds_to_hours = 1 / 3600
    # Find the zero resistance value according to material
    match conductor_type:
        case "average":
            zero_resistance = 230
        case "copper":
            zero_resistance = 234
        case "aluminum":
            zero_resistance = 228    

    nominal_percentage = np.sqrt((((Te - To) / (Tn - To)) - (((Io / In) ** 2) * np.exp(-(time * seconds_to_hours) / K)))/(1 - np.exp(-(time * seconds_to_hours) / K)) * ((zero_resistance + Tn)/(zero_resistance + Te))) * In
    
    return (nominal_percentage, time)

def short_circuit_cable_curve(cm: float, Tn: float, Ts: float, conductor_type: str) -> tuple:
    '''
    This function is going to calculate the curve for damage of a cable due to a short circuit, the formula depends on the temperature and the conductor material.
    '''
    kcmil_to_cmils = 1000 # 1 kcmil to circular mils
    time = np.arange(10, 0, -0.01) # Time to evaluate to find the maximum short circuit current to not damage the cable
    match conductor_type:
        case "copper":
            short_circuit_currents = 0.0779 * ((cm * kcmil_to_cmils) / np.sqrt(time)) # Maximum value of short circuit currents
        case _:
            raise ValueError(f"Unkown material of the conductor: {conductor_type}")
    return (short_circuit_currents, time)

def u_protection_curve(curve_type: str, time_dial: float, pick_up: tuple[float, str]) -> tuple:
    '''
    This functions is going to calculate the tripping time for a U.S. type curve. The formula will depend on the curve type the user input.
    '''
    pick_up_current = pick_up[0] # Pick_up current
    evaluated_currents = np.arange(pick_up_current + 1, 1000 * pick_up_current, 1) # np array of currents to evaluate for calculating the tripping time
    m_multipliers = evaluated_currents / pick_up_current # np array of multipliers

    # Check what type of cuve the user is requesting
    match curve_type:
        case "U3": # U3 (U.S. very inverse)
            tripping_times = time_dial * (0.0963 + (3.88 / ((m_multipliers ** 2) - 1))) # Formula for calculating tripping time of a U3 (U.S. very inverse) curve
        case _:
            raise ValueError(f"Unknow curve type: {curve_type}")
            
    return (m_multipliers, tripping_times)

if __name__ == "__main__":
    main()
