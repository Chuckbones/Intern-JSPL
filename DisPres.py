import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

#Bad fit discharge pressure

# Load data with the first row as the header
file_path = 'C:/Users/Shivam/Documents/JSPL/Code/Refrigeration-Load-Analysis/dpvar2.xlsx'
data = pd.read_excel(file_path, header=0)

# Strip any leading/trailing whitespace from column names
data.columns = data.columns.str.strip()

# Define the actual column names
methanol_flow_column = 'METH FLOW'
cws_temp_column = 'CWS TEMP'
cw_flow_column = 'CW FLOW'
dis_press_column = 'DIS PRESS'
prop_out_column = 'PROP OUT C'
prop_in_column = 'PROP IN'

# Calculate the logarithms of the necessary columns
data['log_dis_press'] = np.log(data[dis_press_column])
data['log_methanol_flow'] = np.log(data[methanol_flow_column])
data['log_cws_temp'] = np.log(data[cws_temp_column])
data['log_cw_flow'] = np.log(data[cw_flow_column])
data['log_prop_diff'] = np.log(-1*(data[prop_out_column] - data[prop_in_column]))

# Define the function to minimize
def objective(params, data):
    a, log_K1, b, d, e, f = params
    predicted_log_dis_press = (a * log_K1 + b * data['log_methanol_flow'] + 
                               d * data['log_cws_temp'] + e * data['log_cw_flow'] +
                               f * data['log_prop_diff'])
    error = np.sum((data['log_dis_press'] - predicted_log_dis_press) ** 2)
    return error

# Initial guess for the parameters
initial_guess = [1, 1, 0.2, 0.2, -0.2, 0.2]

# Optimize the parameters
result = minimize(objective, initial_guess, args=(data,), method='BFGS')

# Extract and print the optimized parameters
a_opt, log_K1_opt, b_opt, d_opt, e_opt, f_opt = result.x
K1_opt = np.exp(log_K1_opt)
print(f'Optimized parameters: ')
print(f'c={a_opt}')
print(f'A={K1_opt}')
print(f'b₁={b_opt}')
print(f'b₂={d_opt}')
print(f'b₃={e_opt}')
print(f'b₄={f_opt}')



# Calculate predicted log(discharge pressure) values
data['predicted_log_dis_press'] = (a_opt * log_K1_opt + b_opt * data['log_methanol_flow'] + 
                                   d_opt * data['log_cws_temp'] + e_opt * data['log_cw_flow'] +
                                   f_opt * data['log_prop_diff'])

# Take the antilog to get the actual predicted discharge pressure
data['predicted_dis_press'] = np.exp(data['predicted_log_dis_press'])
data['observed_dis_press'] = data[dis_press_column]

# Calculate R-squared value
ss_total = np.sum((data['observed_dis_press'] - np.mean(data['observed_dis_press'])) ** 2)
ss_residual = np.sum((data['observed_dis_press'] - data['predicted_dis_press']) ** 2)
r_squared = 1 - (ss_residual / ss_total)
print(f'R-squared: {r_squared}')

# Plotting the observed vs predicted discharge pressure values
plt.figure(figsize=(10, 6))
plt.scatter(data['observed_dis_press'], data['predicted_dis_press'], color='blue', label='Predicted')
plt.plot([data['observed_dis_press'].min(), data['observed_dis_press'].max()], 
         [data['observed_dis_press'].min(), data['observed_dis_press'].max()], color='red', linestyle='--', label='Perfect Fit')
plt.xlabel('Observed Discharge Pressure')
plt.ylabel('Predicted Discharge Pressure')
plt.title('Observed vs Predicted Discharge Pressure')
plt.legend()
plt.grid(True)
plt.show()

# Define the function to predict discharge pressure
def predict_dis_press(methanol_flow, cws_temp, cw_flow, prop_diff):
    log_methanol_flow = np.log(methanol_flow)
    log_cws_temp = np.log(cws_temp)
    log_cw_flow = np.log(cw_flow)
    log_prop_diff = np.log(prop_diff)
    log_predicted_dis_press = (a_opt * log_K1_opt + b_opt * log_methanol_flow + 
                               d_opt * log_cws_temp + e_opt * log_cw_flow + 
                               f_opt * log_prop_diff)
    predicted_dis_press = np.exp(log_predicted_dis_press)
    return predicted_dis_press

# Example usage of the predict_dis_press function
methanol_flow_input = 248.13  # Replace with your value
cws_temp_input = 30.74 + 273  # Replace with your value
cw_flow_input = 1442.2  # Replace with your value
prop_diff_input = 41.2  # Replace with your value

predicted_dis_press = predict_dis_press(methanol_flow_input, cws_temp_input, cw_flow_input, prop_diff_input)
print(f'Predicted Discharge Pressure: {predicted_dis_press}')
