# start.py - One-click launcher
import subprocess
import sys
import os

def install_basic_packages():
    """📦 Install only essential packages"""
    packages = ["pymongo==4.6.1", "python-dotenv==1.0.0"]
    
    for package in packages:
        print(f"📦 Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"✅ {package} installed!")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    return True

def check_mongodb():
    """🔍 Check if MongoDB is accessible"""
    try:
        from database import db_connection
        if db_connection.connect():
            print("✅ MongoDB connection successful!")
            db_connection.close_connection()
            return True
        else:
            print("❌ MongoDB not accessible")
            print("💡 Make sure MongoDB is running:")
            print("   - Download from: https://www.mongodb.com/try/download/community")
            print("   - Or run: mongod")
            return False
    except ImportError:
        print("⚠️ MongoDB packages not installed yet")
        return False

def generate_sample_data():
    """🎨 Add sample recipes"""
    try:
        from generate_sample_data import populate_database
        populate_database()
        return True
    except Exception as e:
        print(f"⚠️ Could not generate sample data: {e}")
        return False

def start_app():
    """🚀 Start the web application"""
    print("🚀 Starting Recipe Management System...")
    try:
        from simple_app import run_server
        run_server()
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
    except Exception as e:
        print(f"❌ Error starting app: {e}")

def main():
    """🎯 Main launcher"""
    print("🍳 Recipe Management System - Simple Setup")
    print("=" * 50)
    
    # Step 1: Install packages
    print("1️⃣ Installing required packages...")
    if not install_basic_packages():
        print("❌ Installation failed. Please check your internet connection.")
        return
    
    # Step 2: Check MongoDB
    print("\n2️⃣ Checking MongoDB connection...")
    if not check_mongodb():
        print("⚠️ MongoDB not available. App will still work but data won't persist.")
        input("Press Enter to continue anyway, or Ctrl+C to exit...")
    
    # Step 3: Generate sample data
    print("\n3️⃣ Setting up sample data...")
    generate_sample_data()
    
    # Step 4: Start app
    print("\n4️⃣ Starting web application...")
    start_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        input("Press Enter to exit...")