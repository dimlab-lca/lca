#!/usr/bin/env python3
"""
Passenger WSGI Entry Point for LCA TV
Domain: lca-tv.bf (points to /lca folder)
Deployment: Root level
"""

import sys
import os

# Add the application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask application directly from app.py
from app import application

# Passenger will use this 'application' object
# Make sure it's named 'application' (not 'app')