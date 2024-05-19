#!/bin/bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Update pip and setuptools
pip install --upgrade pip setuptools

# Install Python dependencies
cd pyserver
pip install -r requirements.txt
cd ..

# Deactivate virtual environment
deactivate

# Build frontend
cd frontend
npm install
npm run build
cd ..

# Build server
cd server
npm install
npm run build
cd ..