#!/usr/bin/env bash
# Script to automate the process of starting the flask application

# Run the environment variables in this session
source ~/.bashrc

# Running the virtual environment
source venv/bin/activate

# Running the flask app
flask run
