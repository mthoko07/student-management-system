# 🚀 Quick Start - Testing

## Run Tests in 3 Steps

### Step 1: Make sure backend is running
```bash
python backend/app.py
```

### Step 2: Run the test suite
```bash
python run_tests.py
```

### Step 3: Choose your test type
- Press `1` for Backend API tests
- Press `2` for Frontend browser tests
- Press `3` for All tests

## Quick Commands

### Backend Tests Only
```bash
pytest backend/test_app.py -v
```

### Frontend Tests Only
```bash
start frontend/test.html
```
(Then click "Run All Tests" button)

## What Gets Tested?

### Backend (20 tests)
✅ All API endpoints (GET, POST, PUT, DELETE)
✅ Data validation (email, age, name, course)
✅ Error handling (404, 400 errors)
✅ Search functionality

### Frontend (10 tests)
✅ API connection
✅ CRUD operations
✅ Form validation
✅ Search functionality

## Expected Results

All tests should pass if:
- Backend is running on port 5000
- Database file is writable
- All dependencies are installed

## Need Help?

See `TESTING.md` for detailed documentation.
