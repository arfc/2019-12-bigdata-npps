import numpy as np
def evaluate(self):
    # salt_density = 13.652 - 7.943e-3*self.Tave_fuel  # UCl3 
    # salt_density = 7.784 - 9.92e-4*self.Tave_fuel  # UCl3   
    # salt_density = 4.823 - 1.4e-3*self.Tave_fuel  # ThCl4  
    # salt_density = 7.108 - 7.59e-4*self.Tave_fuel  # ThF4   
    if self.salt_type == 1:   # {'Li6F': (72*Li6_iso_frac), 'Li7F': (72*Li7_iso_frac), 'BeF2': 16}
        salt_density = 3.628 - 6.6e-4*(self.Tave_fuel-273)  # LiFBeF2-UF4-ThF4   73-16%
        # salt_density = 2.158 - 2.39e-4*self.Tave_fuel  # LiFBeF2   75-25%
        # salt_density = 4.044 - 8.05e-4*self.Tave_fuel  # LiFBeF2-ThF4   70-18-12%
        # salt_density = -3.3304
    elif self.salt_type == 2:   # {'NaF': 76, 'BeF2': 12}
        # salt_density = 3.881- 8.61e-4*self.Tave_fuel  # NaF-ThF4   88-12%
        salt_density = 5.52- 1.964e-3*self.Tave_fuel  # NaF-UF4   85-15%
        # salt_density = -3.3304
    else:   # {'NaCl35': (60*Cl35_iso_frac), 'NaCl37': (60*Cl37_iso_frac)}
        # salt_density = 2.1389 - 5.429e-4*self.Tave_fuel  # NaCl
        # salt_density = 3.828 - 9.9e-4*self.Tave_fuel  # NaCl-ThCl4  60-40%
        salt_density = 4.29 - 1.59e-3*self.Tave_fuel  # NaCl-UCl3    75-25%
        # salt_density = -3.3304
    return salt_density