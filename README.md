# Refrigeration Load Analysis
This repository consists of work done during my summer internship at **Jindal Steel and Power**


This Flask application allows users to calculate methanol flow and discharge pressure by uploading Excel files with relevant data or by entering values manually. The application processes the input data, applies pre-trained models, and displays the results.


## Features

- **File Upload:** Users can upload Excel files containing data to be processed.
- **Manual Input:** Users can enter data manually if no file is uploaded.
- **Session Management:** Data is stored in sessions to maintain state across different steps.
- **Output Display:** The results are displayed on the same page after processing.

## Requirements

- Python 3.7+
- Pip
- Flask

## Environment Variables



Developed in a virtual environment. Create a virtual environment via

```bash 
python -m venv ./env/
```

Activate environment via
```bash
source /env/bin/activate
```
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/methanol-flow-discharge-pressure.git 
1. Install all requirements in the `requirements.txt` file via the command

```bash
pip install -r requirements. txt
```
2.   Install all requirements in the `requirements.txt` file via the command

```bash
pip install -r requirements. txt
```


## Deployment

To run program, do: 

```bash
python -m flask --app server.py run
```

Go to (localhost)[http://127.0.0.1:5000] for viewing the app. 