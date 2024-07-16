import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Methanol Flow Optimization

# Load data with the first row as the header
file_path = 'C:/Users/Shivam/Documents/JSPL/Code/Refrigeration-Load-Analysis/dpvar2.xlsx'
data = pd.read_excel(file_path, header=0)

# Strip any leading/trailing whitespace from column names
data.columns = data.columns.str.strip()

# Define the actual column names
raw_gas_flow_column = 'RAW GAS FLOW'
raw_gas_temp_column = 'RAW_GAS_TEMP'
co2_in_column = 'RawgasCO2(v%)'
co2_diff_column = 'CO2Diff'
methanol_flow_column = 'METH FLOW'
methanol_temp_column = 'METH TEMP'
cw_flow_column = 'CW FLOW'
cws_temp_column = 'CWS TEMP'
dis_press_column = 'DIS PRESS'

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

# Extract and print the optimized parameters
a_opt, log_K1_opt, b_opt, c_opt, d_opt, e_opt, f_opt = result.x
K1_opt = np.exp(log_K1_opt)
print(f'Optimized parameters:')
print(f'c={a_opt}')
print(f'A={K1_opt}')
print(f'b₁={b_opt}')
print(f'b₂={c_opt}')
print(f'b₃={d_opt}')
print(f'b₄={f_opt}')
print(f'b₅={e_opt}')


# Calculate predicted log(M) values
data['predicted_log_M'] = (a_opt * log_K1_opt + b_opt * data['log_rawgasflow'] + c_opt * data['log_rawtemp'] + 
                           d_opt * data['log_co2_diff'] + e_opt * data['log_co2in'] + f_opt * data['log_methanoltemp'] )

# Take the antilog to get the actual predicted methanol flow
data['predicted_M'] = np.exp(data['predicted_log_M'])
data['observed_M'] = data[methanol_flow_column]

# Calculate R-squared value
ss_total = np.sum((data['observed_M'] - np.mean(data['observed_M'])) ** 2)
ss_residual = np.sum((data['observed_M'] - data['predicted_M']) ** 2)
r_squared = 1 - (ss_residual / ss_total)
print()
print(f'R₂ score: {r_squared}')
print()

# Plotting the observed vs predicted M values
plt.figure(figsize=(10, 6))
plt.scatter(data['observed_M'], data['predicted_M'], color='blue', label='Predicted')
plt.plot([data['observed_M'].min(), data['observed_M'].max()], [data['observed_M'].min(), data['observed_M'].max()], color='red', linestyle='--', label='Perfect Fit')
plt.xlabel('Observed Methanol Flow')
plt.ylabel('Predicted Methanol Flow')
plt.title('Observed vs Predicted Methanol Flow')
plt.legend()
plt.grid(True)
plt.show()

# Define the function to predict methanol flow
def predict_methanol_flow(rawgasflow, rawgastemp, co2in, co2out, methanoltemp):
    log_rawgasflow = np.log(rawgasflow)
    log_rawtemp = np.log(rawgastemp)
    log_co2_diff = np.log(co2in - co2out)
    log_co2in = np.log(co2in)
    log_methanoltemp = np.log(methanoltemp)
    log_predicted_M = (a_opt * log_K1_opt + b_opt * log_rawgasflow + c_opt * log_rawtemp + 
                       d_opt * log_co2_diff + e_opt * log_co2in + f_opt * log_methanoltemp )
    predicted_M = np.exp(log_predicted_M)
    return predicted_M

# Example usage of the predict_methanol_flow function
rawgasflow_input = 119925.6  # Replace with your value
rawgastemp_input = 312.2  # Replace with your value
co2in_input = 27.19  # Replace with your value
co2out_input = 2.33  # Replace with your value
methanoltemp_input = 370.62  # Replace with your value

predicted_methanol = predict_methanol_flow(rawgasflow_input, rawgastemp_input, co2in_input, co2out_input, methanoltemp_input)
print(f'Predicted Methanol Flow: {0.936275*predicted_methanol}')


