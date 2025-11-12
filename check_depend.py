import sys

def check_module(module_name, install_name=None):
    """Check if a module is installed"""
    if install_name is None:
        install_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {module_name} is installed")
        return True
    except ImportError:
        print(f"❌ {module_name} is NOT installed")
        print(f"   Run: pip install {install_name}")
        return False

def main():
    print("🔍 Checking dependencies...")
    print(f"Python version: {sys.version}")
    print(f"Virtual environment: {hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)}")
    print()
    
    dependencies = [
        ("streamlit", "streamlit"),
        ("plotly", "plotly"),
        ("pandas", "pandas"),
        ("requests", "requests"),
        ("flask", "Flask"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_installed = True
    for module_name, install_name in dependencies:
        if not check_module(module_name, install_name):
            all_installed = False
    
    print()
    if all_installed:
        print("🎉 All dependencies are installed! You can run:")
        print("   streamlit run dashboard.py")
    else:
        print("⚠️  Some dependencies are missing.")
        print("   Run: pip install -r requirements.txt")

if __name__ == "__main__":
    main()