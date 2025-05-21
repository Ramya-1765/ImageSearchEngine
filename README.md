# ImageSearchEngine
Searches image through image or description
# Intial setup
## Backend Setup
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 builvector.py
    export KMP_DUPLICATE_LIB_OK=TRUE(only once before running flask app)
    python3 app.py
## Frontend Setup
    cd frontend
    npm create vite@latest frontend
    cd frontend
    npm run dev