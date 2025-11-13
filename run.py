#!/usr/bin/env python3
"""
Entry point to run the audio processing Flask application.
Usage: python run.py
"""

if __name__ == '__main__':
    from src.app import app
    import os
    
    # Use environment variable to control debug mode
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
