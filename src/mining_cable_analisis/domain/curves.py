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
            tripping_times = time_dial * (0.026 + (0.0104 / ((m_multipliers ** 0.02) - 1))) # Formula for calculating tripping time of a U1 (U.S. Moderately inverse) curve
        case "U2": # U2 (U.S. Inverse)
            tripping_times = time_dial * (0.18 + (5.95 / ((m_multipliers ** 2) - 1))) # Formula for calculating tripping time of a U2 (U.S.  inverse) curve
        case "U3": # U3 (U.S. very inverse)
            tripping_times = time_dial * (0.0963 + (3.88 / ((m_multipliers ** 2) - 1))) # Formula for calculating tripping time of a U3 (U.S. very inverse) curve
        case "U4": # U4 (U.S. Extremly inverse)
            tripping_times = time_dial * (0.0352 + (5.67 / ((m_multipliers ** 2) - 1))) # Formula for calculating tripping time of a U4 (U.S. extremly inverse) curve
        case "U5": # U5 (U.S. Short-time inverse)
            tripping_times = time_dial * (0.00262 + (0.00342 / ((m_multipliers ** 0.02) - 1))) # Formula for calculating tripping time of a U5 (U.S. short-time inverse) curve
        case _:
            raise ValueError(f"Unknow curve type: {curve_type}")
            
    return (m_multipliers, tripping_times)