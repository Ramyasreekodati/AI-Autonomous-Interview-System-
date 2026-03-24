import uvicorn
import os
import sys

# Get the absolute path of the current file (main.py)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # should be backend/
PROJECT_ROOT = os.path.dirname(ROOT_DIR) # should be c:\Users\Lenovo\Desktop\AI interview\AI-Autonomous-Interview-System-

# Adding both root directories to sys.path to allow app and ai_modules imports
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
