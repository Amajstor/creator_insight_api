import os
import streamlit as st

def get_api_base_url():
    try:
        # First try to get from Streamlit secrets (production)
        if hasattr(st, 'secrets') and 'general' in st.secrets and 'API_BASE_URL' in st.secrets.general:
            return st.secrets.general.API_BASE_URL
        # Then try environment variable
        elif os.environ.get('API_BASE_URL'):
            return os.environ.get('API_BASE_URL')
        else:
            # Local development fallback
            return 'http://localhost:5000'
    except:
        # Fallback for any errors
        return os.environ.get('API_BASE_URL', 'http://localhost:5000')

API_BASE_URL = get_api_base_url()