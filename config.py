import os

# Use environment variable for API URL, fallback to localhost for development
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:5000')