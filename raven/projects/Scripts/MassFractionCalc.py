
def return_value(keys, salt_type, fuel_type, U235F4_mole_frac, UF4_mole_frac):
    fuelsalt_weight_frac_dict = {}
    (salt_weight_frac_dict, salt_mole_frac_dict) = salt_isotopes(salt_type)
    fuelsalt_weight_frac_dict.update (salt_weight_frac_dict)
    fuel_weight_frac_dict = fuel_isotopes(fuel_type, salt_type, U235F4_mole_frac, UF4_mole_frac)
    fuelsalt_weight_frac_dict.update(fuel_weight_frac_dict)
    fuelsalt_weight_frac_dict['F19'] =fuel_weight_frac_dict['F19']+salt_weight_frac_dict['F19']
    #print(salt_type, fuel_type, U235F4_mole_frac, UF4_mole_frac)
    #print(fuelsalt_weight_frac_dict)
    total_weight_frac = sum(fuelsalt_weight_frac_dict.values())
    weight_frac_dict = {k: v / total_weight_frac * 100.0 * -1 for k, v in fuelsalt_weight_frac_dict.items() }
    #print(weight_frac_dict)
    
    return weight_frac_dict[keys]

def salt_isotopes(salt_type):
    
    atomic_weight={'Be9': 9.0121, 'F19': 18.9984, 'Li6': 6.0151, 'Li7': 7.0160, 'Cl35': 34.9688, 'Cl37': 36.9659, 'Na23': 22.9898}
    salt_weight_frac_dict = {k: 0 for k, v in atomic_weight.items() }
    
    if     salt_type == 1:
        # Samofar --> {'LiF': 77.7, 'UF4': 12.3, 'ThF4': 6.7, 'TRUF3': 3.3}
        # Transatomic --> {'LiF': 72, 'UF4': 0.232} enriched to 5%
        # MSFR/Mosart/Flibe --> {'LiF': 72, 'BeF2': 16, 'UF4': 0.232, 'ThF4': 12, 'PuF3': 0.0006} 
        # composition of Li6 and Li7 in lithium
        Li7_iso_frac = 0.999952
        Li6_iso_frac = 1 - Li7_iso_frac
        salt_mole_frac_dict = {'Li6F': (72*Li6_iso_frac), 'Li7F': (72*Li7_iso_frac), 'BeF2': 16}
        salt_weight_frac_dict['Li6'] = salt_mole_frac_dict['Li6F']*atomic_weight['Li6'] 
        salt_weight_frac_dict['Li7'] = salt_mole_frac_dict['Li7F']*atomic_weight['Li7'] 
        salt_weight_frac_dict['Be9'] = salt_mole_frac_dict['BeF2']*atomic_weight['Be9'] 
        salt_weight_frac_dict['F19'] = (salt_mole_frac_dict['Li6F']+salt_mole_frac_dict['Li7F']+2*salt_mole_frac_dict['BeF2'])*atomic_weight['F19'] 
    elif  salt_type == 2:   
        # Thorcon --> {'NaF': 76, 'BeF2': 12, 'UF4': 1.8, 'ThF4': 10.2, 'PuF3': 0} enriched to 19.7%
        salt_mole_frac_dict = {'NaF': 76, 'BeF2': 12}
        salt_weight_frac_dict['Na23'] = salt_mole_frac_dict['NaF']*atomic_weight['Na23'] 
        salt_weight_frac_dict['Be9'] = salt_mole_frac_dict['BeF2']*atomic_weight['Be9'] 
        salt_weight_frac_dict['F19'] = (salt_mole_frac_dict['NaF']+2*salt_mole_frac_dict['BeF2'])*atomic_weight['F19'] 
    else:
        # Terrapower/Elysium/Moltex --> {'NaCl': , 'UCl3': , 'ThCl4': , 'TRUCl3': }
        # composition of Cl35 and Cl37 in Cloride
        Cl35_iso_frac = 0.7577
        Cl37_iso_frac = 1 - Cl35_iso_frac
        salt_mole_frac_dict = {'NaCl35': (60*Cl35_iso_frac), 'NaCl37': (60*Cl37_iso_frac)}
        salt_weight_frac_dict['Na23'] = (salt_mole_frac_dict['NaCl35']+salt_mole_frac_dict['NaCl35'])*atomic_weight['Na23'] 
        salt_weight_frac_dict['Cl35'] = salt_mole_frac_dict['NaCl35']*atomic_weight['Cl35'] 
        salt_weight_frac_dict['Cl37'] = salt_mole_frac_dict['NaCl37']*atomic_weight['Cl37'] 
    
    return salt_weight_frac_dict, salt_mole_frac_dict

def fuel_isotopes(fuel_type, salt_type, U235F4_mole_frac, UF4_mole_frac):

    (salt_weight_frac_dict, salt_mole_frac_dict) = salt_isotopes(salt_type)
    total_fuel_mole_frac = 1-sum(salt_mole_frac_dict.values())/100
    
    U233F4_mole_frac = 0    
    atomic_weight={'F19': 18.9984, 'Th232': 232.038, 'U233': 233.0396, 'U235': 235.0439, 'U238': 238.0508,
                       'Pu238': 238.0495, 'Pu239': 239.0522, 'Pu240': 240.0538, 'Pu241': 241.0568, 'Pu242': 242.0587}
    fuel_weight_frac_dict = {k: 0 for k, v in atomic_weight.items() }
    
    if      fuel_type == 1:   # fuel type 1: U
        fuel_mole_frac_dic = {'U233F4': U233F4_mole_frac, 'U235F4': U235F4_mole_frac, 
                                        'U238F4': (100 - U233F4_mole_frac - U235F4_mole_frac)}
        fuel_mole_frac_dic = {k: total_fuel_mole_frac*v for k, v in fuel_mole_frac_dic.items() }
        
        fuel_weight_frac_dict['U233'] = fuel_mole_frac_dic['U233F4']*atomic_weight['U233']
        fuel_weight_frac_dict['U235'] = fuel_mole_frac_dic['U235F4']*atomic_weight['U235']
        fuel_weight_frac_dict['U238'] = fuel_mole_frac_dic['U238F4']*atomic_weight['U238'] 
        fuel_weight_frac_dict['F19'] = 4*(fuel_mole_frac_dic['U233F4']+fuel_mole_frac_dic['U235F4']+fuel_mole_frac_dic['U238F4'])*atomic_weight['F19'] 
    elif   fuel_type == 2:   # fuel type 2: U-Th
        fuel_mole_frac_dic = {'Th232F4': (100-UF4_mole_frac), 'U233F4': (U233F4_mole_frac*UF4_mole_frac/100), 'U235F4': (U235F4_mole_frac*UF4_mole_frac/100), 
                                        'U238F4': (100 - U233F4_mole_frac - U235F4_mole_frac)*UF4_mole_frac/100}
        fuel_mole_frac_dic = {k: total_fuel_mole_frac*v for k, v in fuel_mole_frac_dic.items() } 
        
        fuel_weight_frac_dict['Th232'] = fuel_mole_frac_dic['Th232F4']*atomic_weight['Th232']
        fuel_weight_frac_dict['U233'] = fuel_mole_frac_dic['U233F4']*atomic_weight['U233']
        fuel_weight_frac_dict['U235'] = fuel_mole_frac_dic['U235F4']*atomic_weight['U235']
        fuel_weight_frac_dict['U238'] = fuel_mole_frac_dic['U238F4']*atomic_weight['U238'] 
        fuel_weight_frac_dict['F19'] = 4*(fuel_mole_frac_dic['Th232F4']+fuel_mole_frac_dic['U233F4']+ \
                                                   fuel_mole_frac_dic['U235F4']+fuel_mole_frac_dic['U238F4'])*atomic_weight['F19'] 
    else:                          # fuel type 3: U-Pu
        # composition of Pu isotopes in Weapon Grade Plutonium
        Pu_iso_frac = {'Pu238': 0.05e-2, 'Pu239': 94.3e-2, 'Pu240': 5.0e-2, 'Pu241': 0.6e-2, 'Pu242': 0.05e-2 }
        fuel_mole_frac_dic = {'U233F4': (U233F4_mole_frac*UF4_mole_frac/100), 'U235F4': (U235F4_mole_frac*UF4_mole_frac/100), 
                                        'U238F4': (100-U233F4_mole_frac-U235F4_mole_frac)*UF4_mole_frac/100, 
                                        'Pu238F3': (100-UF4_mole_frac)*Pu_iso_frac['Pu238'], 'Pu239F3': (100-UF4_mole_frac)*Pu_iso_frac['Pu239'], 
                                        'Pu240F3': (100-UF4_mole_frac)*Pu_iso_frac['Pu240'], 'Pu241F3': (100-UF4_mole_frac)*Pu_iso_frac['Pu241'], 
                                        'Pu242F3': (100-UF4_mole_frac)*Pu_iso_frac['Pu242']}
        fuel_mole_frac_dic = {k: total_fuel_mole_frac*v for k, v in fuel_mole_frac_dic.items() }                                
        
        fuel_weight_frac_dict['U233'] = fuel_mole_frac_dic['U233F4']*atomic_weight['U233']
        fuel_weight_frac_dict['U235'] = fuel_mole_frac_dic['U235F4']*atomic_weight['U235']
        fuel_weight_frac_dict['U238'] = fuel_mole_frac_dic['U238F4']*atomic_weight['U238'] 
        fuel_weight_frac_dict['Pu238'] = fuel_mole_frac_dic['Pu238F3']*atomic_weight['Pu238']
        fuel_weight_frac_dict['Pu239'] = fuel_mole_frac_dic['Pu239F3']*atomic_weight['Pu239']
        fuel_weight_frac_dict['Pu240'] = fuel_mole_frac_dic['Pu240F3']*atomic_weight['Pu240'] 
        fuel_weight_frac_dict['Pu241'] = fuel_mole_frac_dic['Pu241F3']*atomic_weight['Pu241']
        fuel_weight_frac_dict['Pu242'] = fuel_mole_frac_dic['Pu242F3']*atomic_weight['Pu242'] 
        fuel_weight_frac_dict['F19'] = (4*(fuel_mole_frac_dic['U233F4']+fuel_mole_frac_dic['U235F4']+fuel_mole_frac_dic['U238F4'])+ \
                                                   3*(fuel_mole_frac_dic['Pu239F3']+fuel_mole_frac_dic['Pu240F3']+ \
                                                   fuel_mole_frac_dic['Pu240F3']+fuel_mole_frac_dic['Pu241F3']+fuel_mole_frac_dic['Pu242F3'])*atomic_weight['F19'])
     
    return fuel_weight_frac_dict

if __name__ == "__main__":
    return_value('F19', 2, 3, 10, 50)