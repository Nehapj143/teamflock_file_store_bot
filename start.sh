#!/bin/bash

# Activate the virtual environment
source /opt/render/project/src/.venv/bin/activate

pip install requests

# Upgrade pip
pip install --upgrade pip

# Install dependencies listed in requirements.txt
pip install -r requirements.txt

# Run your Python script (main.py)
python3 main.py
