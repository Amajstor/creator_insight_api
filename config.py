import os

# Use environment variable for API URL, fallback to localhost for development
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://web-production-a7a8.up.railway.app/')