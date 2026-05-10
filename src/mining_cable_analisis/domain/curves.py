import numpy as np

def intermediate_overload_cable_curve(To: float, Tn: float, Te: float, Io: float, In: float, K: float, time: np.ndarray, conductor_type: str="average") -> tuple:
    '''
    The formula is the following from IEEE 3003.7 - 2021
    percentage = math.sqrt((((Te - To) / (Tn - To)) - (math.pow(Io / In, 1) * math.exp(-(delta/3600)/K)))/(1-math.exp(-(delta/3600)/K))*((230 + Tn)/(230 + Te))) 
    Where:
    Ie -> Emergency operating current rating
    In -> Normal current rating
    Io -> Operating current prior to emergency
    Te -> Conductor emergency operating temperature
    Tn -> Conductor normal operating temperature
    To -> Ambient temperature
    K -> Constant, dependent on cable size and installation type
    229 -> Zero-resistance temperature value (Average value. For copper use 234, for aluminum use 228)
    e -> Base for natural logarithms
    delta -> Time (seconds)
    '''
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
    time = np.arange(9, 0, -0.01) # Time to evaluate to find the maximum short circuit current to not damage the cable
    match conductor_type:
        case "copper":
            short_circuit_currents = 0.0779 * ((cm * kcmil_to_cmils) / np.sqrt(time)) # Maximum value of short circuit currents
        case _:
            raise ValueError(f"Unkown material of the conductor: {conductor_type}")
    return (short_circuit_currents, time)

def protection_curve(curve_type:str, time_dial: float, pick_up: tuple[float, str]) -> tuple:
    # Checking if curve type is a standard curve
    if curve_type in ["U1", "U2", "U3", "U4", "U5"]:
        return u_protection_curve(curve_type=curve_type, time_dial=time_dial, pick_up=pick_up)
    elif curve_type in ["C1", "C2", "C3", "C4", "C5"]:
        return c_protection_curve(curve_type=curve_type, time_dial=time_dial, pick_up=pick_up)
    elif curve_type in ["E1", "E2", "E3"]:
        return e_protection_curve(curve_type=curve_type, time_dial=time_dial, pick_up=pick_up)
    else:
        pass # This is going to be reserve to look for a previously loaded protection curve (custom curve)

def u_protection_curve(curve_type: str, time_dial: float, pick_up: tuple[float, str]) -> tuple:
    '''
    This functions is going to calculate the tripping time for a U.S. type curve. The formula will depend on the curve type the user input.
    '''
    pick_up_current = pick_up[0] # Pick_up current
    evaluated_currents = np.arange(pick_up_current + 1, 1000 * pick_up_current, 1) # np array of currents to evaluate for calculating the tripping time
    m_multipliers = evaluated_currents / pick_up_current # np array of multipliers

    # Check what type of cuve the user is requesting
    match curve_type:
        case "U1": # U1 (U.S. Moderately inverse)
            tripping_times = time_dial * (0.026 + (0.0104 / ((m_multipliers ** 0.02) - 1))) # Formula for calculating tripping time
        case "U2": # U2 (U.S. Inverse)
            tripping_times = time_dial * (0.18 + (5.95 / ((m_multipliers ** 2) - 1))) # Formula for calculating tripping time
        case "U3": # U3 (U.S. very inverse)
            tripping_times = time_dial * (0.0963 + (3.88 / ((m_multipliers ** 2) - 1))) # Formula for calculating tripping time
        case "U4": # U4 (U.S. Extremly inverse)
            tripping_times = time_dial * (0.0352 + (5.67 / ((m_multipliers ** 2) - 1))) # Formula for calculating tripping time
        case "U5": # U5 (U.S. Short-time inverse)
            tripping_times = time_dial * (0.00262 + (0.00342 / ((m_multipliers ** 0.02) - 1))) # Formula for calculating tripping time
        case _:
            raise ValueError(f"Unknow curve type: {curve_type}")
            
    return (m_multipliers, tripping_times)

def c_protection_curve(curve_type: str, time_dial: float, pick_up: tuple[float, str]) -> tuple:
    '''
    This functions is going to calculate the tripping time for a IEC type curve. The formula will depend on the curve type the user input.
    '''
    pick_up_current = pick_up[0] # Pick_up current
    evaluated_currents = np.arange(pick_up_current + 1, 1000 * pick_up_current, 1) # np array of currents to evaluate for calculating the tripping time
    m_multipliers = evaluated_currents / pick_up_current # np array of multipliers

    # Check what type of cuve the user is requesting
    match curve_type:
        case "C1": # C1 (IEC Standard inverse)
            tripping_times = time_dial * (0.14 / ((m_multipliers ** 0.02) - 1)) # Formula for calculating tripping time
        case "C2": # C2 (IEC Very Inverse)
            tripping_times = time_dial * (13.5 / (m_multipliers - 1)) # Formula for calculating tripping time
        case "C3": # C3 (IEC Extremly inverse)
            tripping_times = time_dial * (80 / ((m_multipliers ** 2) - 1)) # Formula for calculating tripping time
        case "C4": # C4 (IEC Long-time inverse)
            tripping_times = time_dial * (120 / (m_multipliers - 1)) # Formula for calculating tripping time
        case "C5": # C5 (IEC Short-time inverse)
            tripping_times = time_dial * (0.05 / ((m_multipliers ** 0.04) - 1)) # Formula for calculating tripping time
        case _:
            raise ValueError(f"Unknow curve type: {curve_type}")
            
    return (m_multipliers, tripping_times)

def e_protection_curve(curve_type: str, time_dial: float, pick_up: tuple[float, str]) -> tuple:
    '''
    This functions is going to calculate the tripping time for a IEEE type curve. The formula will depend on the curve type the user input.
    '''
    pick_up_current = pick_up[0] # Pick_up current
    evaluated_currents = np.arange(pick_up_current + 1, 1000 * pick_up_current, 1) # np array of currents to evaluate for calculating the tripping time
    m_multipliers = evaluated_currents / pick_up_current # np array of multipliers

    # Check what type of cuve the user is requesting
    match curve_type:
        case "E1": # E1 (IEEE Moderately inverse)
            tripping_times = time_dial * (0.1140 + (0.0515 / ((m_multipliers ** 0.02) - 1))) # Formula for calculating tripping time
        case "E2": # E2 (IEEE Very Inverse)
            tripping_times = time_dial * (0.491 + (19.61 / ((m_multipliers ** 2) - 1))) # Formula for calculating tripping time
        case "E3": # E3 (IEEE Extremely inverse)
            tripping_times = time_dial * (0.1217 + (28.2 / ((m_multipliers ** 2) - 1))) # Formula for calculating tripping time
        case _:
            raise ValueError(f"Unknow curve type: {curve_type}")
            
    return (m_multipliers, tripping_times)