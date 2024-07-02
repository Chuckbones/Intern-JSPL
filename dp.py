import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Load data with the first row as the header
file_path = 'C:/Users/Shivam/Documents/JSPL/Code/dpvar.xlsx'
data = pd.read_excel(file_path, header=0)

# Strip any leading/trailing whitespace from column names
data.columns = data.columns.str.strip()

# Define the actual column names from your file after verifying them
raw_gas_flow_column = 'RAW GAS FLOW'
raw_gas_temp_column = 'RAW_GAS_TEMP'
co2_in_column = 'RawgasCO2(v%)'
co2_diff = 'CO2Diff'
methanol_flow_column = 'METH FLOW'

# Extract variables
raw_gas_flow = data[raw_gas_flow_column].values
raw_gas_temp = data[raw_gas_temp_column].values
co2_in = data[co2_in_column].values
co2_diff = data[co2_diff].values
methanol_flow = data[methanol_flow_column].values


# Scale the data to avoid numerical instability
rgf = np.max(raw_gas_flow)
rgt = np.max(raw_gas_temp)
c2in = np.max(co2_in)
c2df = np.max(co2_diff)
mf = np.max(methanol_flow)

raw_gas_flow = raw_gas_flow / np.max(raw_gas_flow)
raw_gas_temp = raw_gas_temp / np.max(raw_gas_temp)
co2_in = co2_in / np.max(co2_in)
co2_diff = co2_diff / np.max(co2_diff)
methanol_flow = methanol_flow / np.max(methanol_flow)

# Define the model
def methanol_flow_model(params, raw_gas_flow, raw_gas_temp,co2_in,co2_diff):
    a,b,c,d,constant,e = params
    return (constant**e) * (raw_gas_flow ** a) * (raw_gas_temp ** b)*(co2_in ** c) * (co2_diff ** d)

# Define the objective function
def objective_function(params, raw_gas_flow, raw_gas_temp,co2_in,co2_diff, observed_methanol_flow):
    predicted_methanol_flow = methanol_flow_model(params, raw_gas_flow, raw_gas_temp,co2_in, co2_diff)
    return np.sum((observed_methanol_flow - predicted_methanol_flow) ** 2)

# Initial guess for the parameters [a, b, c, d, constant]
initial_guess = [0.5, 0.5, 0.5,0.5, 0.1,1]

# Minimize the objective function
result = minimize(objective_function, initial_guess, args=(raw_gas_flow, raw_gas_temp,co2_in ,co2_diff, methanol_flow))

# Optimized parameters
optimized_params = result.x

# Print optimized parameters
a, b,c, d, constant,e = optimized_params

print('Optimized parameters:')
print(f'a: {a}')
print(f'b: {b}')
print(f'c: {c}')
print(f'd: {d}')
print(f'constant: {constant}')
print(f'e: {e}')


# Calculate predicted methanol flow using optimized parameters
predicted_methanol_flow = methanol_flow_model(optimized_params, raw_gas_flow, raw_gas_temp,co2_in ,co2_diff)

# Calculate RMSE
rmse = np.sqrt(np.mean((methanol_flow - predicted_methanol_flow) ** 2))
print(f'Root Mean Squared Error (RMSE): {rmse*100}%')
