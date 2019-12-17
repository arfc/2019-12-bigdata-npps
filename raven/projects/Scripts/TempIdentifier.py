import numpy as np
def evaluate(self):

    if self.Tave_fuel < 900:
       temp_identifier = '06'   
    elif self.Tave_fuel < 1200:
       temp_identifier = '09'
    else:
       temp_identifier = '12'
       
    # temp_identifier = str(int(self.Tave_fuel/100))    
    # if self.Tave_fuel < 1000:
        # temp_identifier = '0' + temp_identifier
    return temp_identifier
