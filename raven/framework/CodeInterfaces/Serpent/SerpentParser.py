import numpy as np
import csv

def OutputFailure(self,output,workingDir):

    errorWord = "Input error:"
    failure = True
    try:
      outputToRead = open(os.path.join(workingDir,output),"r")
    except IOError:
    # the output does not exist 
      return failure    
    readLines = outputToRead.readlines()
    for goodMsg in errorWord:
      if any(goodMsg in x for x in readLines):
        failure = False
        break
    return failure

def SearchKinf(res_file):

    with open(res_file) as f:
        lines = f.readlines()
    for i in range(0, len(lines)):
        if 'IMP_KEFF' in lines[i]:
            k_inf = LineParsing(lines[i])
    return k_inf

def SearchConversionRatio(res_file):

    with open(res_file) as f:
        lines = f.readlines()
    for i in range(0, len(lines)):
        if 'CONVERSION_RATIO' in lines[i]:
            conversion_ratio = LineParsing(lines[i])
    return conversion_ratio

def SearchFastFluxGraph(det_file):

    with open(det_file) as f:
        lines = f.readlines()
    for i in range(0, len(lines)):
        if '2    2    1    1    1    1    1    1    1    1' in lines[i]:
            values = lines[i].strip(' ')
            values = values.split(' ')
            fast_flux_graph = values[len(values)-3]
    return fast_flux_graph

def SearchFeedbackDoppler(res_file):

    # import csv
    # input_file = csv.DictReader(open("../Feedback_output.csv"))
    # feedback_doppler = 1e5 * (float(k_inf) - float(row["age"])) / (Tave_fuel-600))
    
    with open(res_file) as f:
        lines = f.readlines()
    for i in range(0, len(lines)):
        if 'IMP_KEFF' in lines[i]:
            k_inf = LineParsing(lines[i])
    return k_inf

    return feedback_doppler

def JoinCSV(grid_file,feedback_file):

    import csv
    grid_file_dict = csv.DictReader(open(grid_file+".csv"))
    feedback_file_dict = csv.DictReader(open(feedback_file+".csv"))
    for i in grid_file_dict:
       for j in grid_file_dict[i]:
          print(j)
           #grid_file_dict["k_inf"] = 1e5 * (float(grid_file_dict["k_inf"]) - float(feedback_file_dict["k_inf"])) / (float(grid_file_dict["Tave_fuel"]) - 600))
    with open("combined.csv", 'w') as csv_file:
       writer = csv.writer(csv_file)
       writer.writerow(grid_file_dict)
       
    return feedback_doppler

def LineParsing(get_value_line):

    start = get_value_line.find('=')
    new_kinf_line = get_value_line[start:]
    start = new_kinf_line.find('[')
    end = new_kinf_line.find(']')
    value_sd = new_kinf_line[start + 3:end - 1]
    (value, sd) = value_sd.split(' ')
    return value

def MakeCSV(fileout, k_inf, conversion_ratio, fast_flux_graph, feedback_doppler):
    with open(fileout, 'w') as csv_file:
        writer = csv.writer(csv_file)
        headers = ['k_inf', 'conversion_ratio', 'fast_flux_graph', 'feedback_doppler']
        writer.writerow(headers)
        values =  [k_inf, conversion_ratio, fast_flux_graph, feedback_doppler] 
        writer.writerow(values)