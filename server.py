
from flask import Flask, render_template, request, session, redirect
from data import extract_data_from_dp_file, extract_data_from_mf_file, get_output_from_dp_model, get_output_from_mf_model

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # in order to use sessions

# global constants
MF_VARIABLES_KEY = 'mf-variables'
DP_VARIABLES_KEY = 'dp-variables'


@app.route('/', methods=('GET', 'POST'))
def index_page():
  return render_template('index.html')

@app.route('/clean/mf')
def clean_mf(): 
  session[MF_VARIABLES_KEY] = []
  return redirect('/mf')

@app.route('/clean/dp')
def clean_dp(): 
  session[DP_VARIABLES_KEY] = []
  return redirect('/dp')


@app.route('/mf', methods=('GET', 'POST'))
def methanol_flow():
  # variables to control html
  hide_argument_inputs = True
  hide_file_upload = False
  show_output = False
  output_value = 0

  # print(request.files, len(request.files))
  # print(session)
  # handle file upload 
  if request.method == 'POST':
    # if it is file upload
    if len(request.files) > 0: 
      f = request.files['file'] 
      # save file to system for reading
      save_file_path = "files/" + f.filename
      f.save(save_file_path)

      # get variables from excel file (train your model - b0, b1, b2)
      variables = extract_data_from_mf_file(save_file_path)

      # save variables to session (session is a dictionary)
      session[MF_VARIABLES_KEY] = variables

      # move to arguments screen
      hide_file_upload = True
      hide_argument_inputs = False
      show_output = False

    
    # if it is via inputs
    elif len(request.form) > 0:
      # get input from form
      raw_gas_flow = request.form.get('raw-gas-flow')
      raw_gas_temp = request.form.get('raw-gas-temp')
      co2_in = request.form.get('co2-in')
      co2_out = request.form.get('co2-out')
      methanol_temp = request.form.get('methanol-temp')

      # clean inputs -> make it into numbers from strings
      model_arguments = [
        float(raw_gas_flow), 
        float(raw_gas_temp), 
        float(co2_in),  
        float(co2_out), 
        float(methanol_temp), 
      ]

      # get output from model
      output_value = get_output_from_mf_model(session[MF_VARIABLES_KEY], model_arguments)

      # move to output screen
      hide_file_upload = True
      hide_argument_inputs = False
      show_output = True
    
    # rerender template
    return render_template(
      'methanol-flow.html', 
      hide_file_upload=hide_file_upload, 
      hide_argument_inputs=hide_argument_inputs,
      show_output=show_output, 
      output_value=output_value
    )

  # what happens if there are no variables in the session
  # that means we don't 
  # return file template
  if session.get(MF_VARIABLES_KEY, []) == []: 
    hide_argument_inputs = True
    hide_file_upload = False
    show_output = False
    return render_template(
      'methanol-flow.html', 
      hide_file_upload=hide_file_upload, 
      hide_argument_inputs=hide_argument_inputs, 
      show_output=show_output, 
      output_value=output_value
    )
  
  # return arguments template
  hide_argument_inputs = False
  hide_file_upload = True
  show_output = False
  return render_template(
    'methanol-flow.html', 
    hide_file_upload=hide_file_upload, 
    hide_argument_inputs=hide_argument_inputs, 
    show_output=show_output, 
      output_value=output_value
  )

@app.route('/dp', methods=('GET', 'POST'))
def discharge_pressure():
  # variables to control html
  hide_argument_inputs = True
  hide_file_upload = False
  show_output = False
  output_value = 0

  # print(request.files, len(request.files))
  # print(session)
  # handle file upload 
  if request.method == 'POST':
    # if it is file upload
    if len(request.files) > 0: 
      f = request.files['file'] 
      # save file to system for reading
      save_file_path = "files/" + f.filename
      f.save(save_file_path)

      # get variables from excel file (train your model - b0, b1, b2)
      variables = extract_data_from_dp_file(save_file_path)

      # save variables to session (session is a dictionary)
      session[DP_VARIABLES_KEY] = variables

      # move to arguments screen
      hide_file_upload = True
      hide_argument_inputs = False
      show_output = False

    
    # if it is via inputs
    elif len(request.form) > 0:
      # get input from form
      methanol_flow = request.form.get('methanol-flow')
      cooling_water_inlet_temp = request.form.get('cooling-water-inlet-temp')
      cooling_water_flow = request.form.get('cooling-water-flow')
      prop_out_temp = request.form.get('prop-out-temp')
      raw_gas_flow = request.form.get('raw-gas-flow')

      # clean inputs -> make it into numbers from strings
      model_arguments = [
        float(methanol_flow), 
        float(cooling_water_inlet_temp), 
        float(cooling_water_flow), 
        float(prop_out_temp), 
        float(raw_gas_flow), 
      ]

      # get output from model
      output_value = get_output_from_dp_model(session[DP_VARIABLES_KEY], model_arguments)

      # move to output screen
      hide_file_upload = True
      hide_argument_inputs = False
      show_output = True
    
    # rerender template
    return render_template(
      'discharge-pressure.html', 
      hide_file_upload=hide_file_upload, 
      hide_argument_inputs=hide_argument_inputs,
      show_output=show_output, 
      output_value=output_value
    )

  # what happens if there are no variables in the session
  # that means we don't 
  # return file template
  if session.get(DP_VARIABLES_KEY, []) == []: 
    hide_argument_inputs = True
    hide_file_upload = False
    show_output = False
    return render_template(
      'discharge-pressure.html', 
      hide_file_upload=hide_file_upload, 
      hide_argument_inputs=hide_argument_inputs, 
      show_output=show_output, 
      output_value=output_value
    )
  
  # return arguments template
  hide_argument_inputs = False
  hide_file_upload = True
  show_output = False
  return render_template(
    'discharge-pressure.html', 
    hide_file_upload=hide_file_upload, 
    hide_argument_inputs=hide_argument_inputs, 
    show_output=show_output, 
      output_value=output_value
  )