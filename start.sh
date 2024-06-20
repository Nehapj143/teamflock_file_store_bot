#!/bin/bash

# Activate the virtual environment
source /opt/render/project/src/.venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies listed in requirements.txt
pip install -r requirements.txt

# Run your Python application
python /opt/render/project/src/main.py
