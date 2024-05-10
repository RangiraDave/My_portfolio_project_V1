#!/usr/bin/env bash
# Script to automate the process of starting the flask application

# Run the environment variables in this session
source ~/.bashrc

# Running the virtual environment
source venv/bin/activate

# Running the flask app
# flask run --host=0.0.0.0 --port=5000

# Quietly install requirements
pip install -r -q requirements.txt

# Installing gunicorn
pip install gunicorn -q

# Running flask app using gunicorn
venv/bin/gunicorn -b 0.0.0.0:5000 -w 4 app:app
