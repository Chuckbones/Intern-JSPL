# this is where your code will go
import pandas as pd
import numpy as np
import os
from scipy.optimize import minimize

#Functions for Extracting data from data

def extract_data_from_mf_file(file_path):
  data = pd.read_excel(os.path.join(os.getcwd(), file_path), header=0)
  # Strip any leading/trailing whitespace from column names
  data.columns = data.columns.str.strip()

# Define the actual column names
  raw_gas_flow_column = 'RAW GAS FLOW'
  raw_gas_temp_column = 'RAW_GAS_TEMP'
  co2_in_column = 'RawgasCO2(v%)'
  co2_diff_column = 'CO2Diff'
  methanol_flow_column = 'METH FLOW'
  methanol_temp_column = 'METH TEMP'
  

# Calculate the logarithms of the necessary columns
  data['log_M'] = np.log(data[methanol_flow_column])
  data['log_rawgasflow'] = np.log(data[raw_gas_flow_column])
  data['log_rawtemp'] = np.log(data[raw_gas_temp_column])
  data['log_co2_diff'] = np.log(data[co2_in_column] - data[co2_diff_column])
  data['log_co2in'] = np.log(data[co2_in_column])
  data['log_methanoltemp'] = np.log(data[methanol_temp_column])

# Define the function to minimize
  def objective(params, data):
    a, log_K1, b, c, d, e, f = params
    predicted_log_M = (a * log_K1 + b * data['log_rawgasflow'] + c * data['log_rawtemp'] + 
                       d * data['log_co2_diff'] + e * data['log_co2in'] + f * data['log_methanoltemp'] )
    error = np.sum((data['log_M'] - predicted_log_M) ** 2)
    return error

# Initial guess for the parameters
  initial_guess = [1, 1, 0.2, 0.1, 0.1, 0.1, 1]

# Optimize the parameters
  result = minimize(objective, initial_guess, args=(data,), method='BFGS')
  opt_para=result.x
  # print(opt_para)
  return list(opt_para)

def extract_data_from_dp_file(file_path):
  data = pd.read_excel(os.path.join(os.getcwd(), file_path), header=0)
  # Strip any leading/trailing whitespace from column names
  data.columns = data.columns.str.strip()

# Define the actual column names
  methanol_flow_column = 'METH FLOW'
  cws_temp_column = 'CWS TEMP'
  cw_flow_column = 'CW FLOW'
  dis_press_column = 'DIS PRESS'
  raw_gas_flow_column = 'RAW GAS FLOW LL'
  prop_out_column = 'PROP OUT'

# Calculate the logarithms of the necessary columns
  data['log_dis_press'] = np.log(data[dis_press_column])
  data['log_methanol_flow'] = np.log(data[methanol_flow_column])
  data['log_cws_temp'] = np.log(data[cws_temp_column])
  data['log_cw_flow'] = np.log(data[cw_flow_column])
  data['log_raw_gas_flow'] = np.log(data[raw_gas_flow_column])
  data['log_prop_out'] = np.log(data[prop_out_column])

# Define the function to minimize
  def objective(params, data):
    a, log_K1, b, d, e, c, f = params
    predicted_log_dis_press = (a * log_K1 + b * data['log_methanol_flow'] + 
                               d * data['log_cws_temp'] + e * data['log_cw_flow'] +
                               c * data['log_raw_gas_flow'] + f * data['log_prop_out'])
    error = np.sum((data['log_dis_press'] - predicted_log_dis_press) ** 2)
    return error

# Initial guess for the parameters
  initial_guess = [1, 1, 0.2, 0.2,-0.21, 0.2, 0.5]

# Optimize the parameters
  result = minimize(objective, initial_guess, args=(data,), method='BFGS')
  opt_para=result.x
  print(opt_para)
  return list(opt_para)

#Functions for getting output from data

def get_output_from_dp_model(model_variables, model_arguments):
    # Unpack model_variables (optimized parameters)
    print(model_variables)
    a_opt, log_K1_opt, b_opt, d_opt, e_opt, c_opt, f_opt = model_variables
    
    # Unpack model_arguments (input variables)
    methanol_flow = model_arguments[0]
    cws_temp = model_arguments[1]
    cw_flow = model_arguments[2]
    prop_out = model_arguments[3]
    raw_gas_flow = model_arguments[4]
    
    print(model_arguments)
    # Calculate logarithms
    log_methanol_flow = np.log(methanol_flow)
    log_cws_temp = np.log(cws_temp)
    log_cw_flow = np.log(cw_flow)
    log_raw_gas_flow = np.log(raw_gas_flow)
    log_prop_out = np.log(prop_out)
    log_predicted_dis_press = (a_opt * log_K1_opt + b_opt * log_methanol_flow + 
                               d_opt * log_cws_temp + e_opt * log_cw_flow + 
                               c_opt * log_raw_gas_flow + f_opt * log_prop_out)
    
    predicted_dis_press = np.exp(log_predicted_dis_press)
    
    return predicted_dis_press
 


def get_output_from_mf_model(model_variables, model_arguments):
  # Unpack model_variables (optimized parameters)
    print(model_variables)
    a_opt, log_K1_opt, b_opt, c_opt, d_opt, e_opt, f_opt = model_variables
    
    # Unpack model_arguments (input variables)
    rawgasflow = model_arguments[0]
    rawgastemp = model_arguments[1]
    co2in = model_arguments[2]
    co2out = model_arguments[3]
    methanoltemp = model_arguments[4]
    
    # Calculate logarithms
    log_rawgasflow = np.log(rawgasflow)
    log_rawtemp = np.log(rawgastemp)
    log_co2_diff = np.log(co2in - co2out)
    log_co2in = np.log(co2in)
    log_methanoltemp = np.log(methanoltemp)
    
    # Calculate predicted methanol flow
    log_predicted_M = (a_opt * log_K1_opt + b_opt * log_rawgasflow + 
                       c_opt * log_rawtemp + d_opt * log_co2_diff + 
                       e_opt * log_co2in + f_opt * log_methanoltemp)
    
    predicted_M = np.exp(log_predicted_M)
    correction_error=0.936275
    return correction_error*predicted_M
  
  