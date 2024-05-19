#!/bin/bash
# Update pip and setuptools
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip install --upgrade pip setuptools

# Install Python dependencies
cd pyserver
pip install -r requirements.txt
cd ..

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
