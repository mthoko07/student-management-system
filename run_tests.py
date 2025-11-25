"""
Test Runner for Student Management System
Runs both backend and frontend tests
"""

import subprocess
import sys
import os
import webbrowser
import time

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_backend_tests():
    print_header("🧪 Running Backend Tests")
    
    # Check if pytest is installed
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "backend/test_app.py", "-v", "--tb=short"],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running backend tests: {e}")
        print("\n💡 Make sure pytest is installed:")
        print("   pip install pytest pytest-flask")
        return False

def run_frontend_tests():
    print_header("🌐 Opening Frontend Tests")
    
    test_file = os.path.abspath("frontend/test.html")
    
    if os.path.exists(test_file):
        print(f"📂 Opening: {test_file}")
        print("\n⚠️  Make sure the backend server is running on http://localhost:5000")
        print("   Run: python backend/app.py\n")
        
        # Open in browser
        webbrowser.open(f"file:///{test_file}")
        print("✅ Frontend test page opened in browser")
        print("   Click 'Run All Tests' button to execute tests")
        return True
    else:
        print(f"❌ Test file not found: {test_file}")
        return False

def main():
    print_header("🎓 Student Management System - Test Suite")
    
    print("Select test type:")
    print("1. Backend Tests (pytest)")
    print("2. Frontend Tests (browser)")
    print("3. Run All Tests")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        success = run_backend_tests()
        if success:
            print("\n✅ Backend tests completed successfully!")
        else:
            print("\n❌ Backend tests failed!")
            
    elif choice == "2":
        run_frontend_tests()
        
    elif choice == "3":
        backend_success = run_backend_tests()
        time.sleep(2)
        run_frontend_tests()
        
        if backend_success:
            print("\n✅ All tests initiated!")
        else:
            print("\n⚠️  Backend tests failed, but frontend tests opened")
            
    elif choice == "4":
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice!")
        sys.exit(1)

if __name__ == "__main__":
    main()
