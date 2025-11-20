"""
Student Management System - Flask Backend
Simple, clean, production-ready code
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Data file path
DATA_FILE = os.path.join(os.path.dirname(__file__), 'students.json')

# Initialize data file
def init_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

# Read students
def read_students():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

# Write students
def write_students(students):
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=2)

# Validate student data
def validate_student(data):
    if not data.get('name') or len(data['name'].strip()) < 2:
        return False, "Name must be at least 2 characters"
    if not data.get('email') or '@' not in data['email']:
        return False, "Invalid email address"
    try:
        age = int(data.get('age', 0))
        if age < 1 or age > 150:
            return False, "Age must be between 1 and 150"
    except:
        return False, "Age must be a number"
    if not data.get('course') or len(data['course'].strip()) < 2:
        return False, "Course must be at least 2 characters"
    return True, "Valid"

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Student Management System API',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/students': 'Get all students',
            'POST /api/students': 'Create student',
            'PUT /api/students/<id>': 'Update student',
            'DELETE /api/students/<id>': 'Delete student',
            'GET /api/students/search?q=query': 'Search students'
        }
    })

@app.route('/api/students', methods=['GET'])
def get_students():
    students = read_students()
    return jsonify(students), 200

@app.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    students = read_students()
    student = next((s for s in students if s['id'] == id), None)
    if student:
        return jsonify(student), 200
    return jsonify({'error': 'Student not found'}), 404

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    
    # Validate
    is_valid, message = validate_student(data)
    if not is_valid:
        return jsonify({'error': message}), 400
    
    students = read_students()
    new_id = max([s['id'] for s in students], default=0) + 1
    
    new_student = {
        'id': new_id,
        'name': data['name'].strip(),
        'email': data['email'].strip(),
        'age': int(data['age']),
        'course': data['course'].strip(),
        'created_at': datetime.now().isoformat()
    }
    
    students.append(new_student)
    write_students(students)
    
    return jsonify(new_student), 201

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    
    # Validate
    is_valid, message = validate_student(data)
    if not is_valid:
        return jsonify({'error': message}), 400
    
    students = read_students()
    student = next((s for s in students if s['id'] == id), None)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    student['name'] = data['name'].strip()
    student['email'] = data['email'].strip()
    student['age'] = int(data['age'])
    student['course'] = data['course'].strip()
    student['updated_at'] = datetime.now().isoformat()
    
    write_students(students)
    return jsonify(student), 200

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    students = read_students()
    filtered = [s for s in students if s['id'] != id]
    
    if len(filtered) == len(students):
        return jsonify({'error': 'Student not found'}), 404
    
    write_students(filtered)
    return jsonify({'message': 'Student deleted'}), 200

@app.route('/api/students/search', methods=['GET'])
def search_students():
    query = request.args.get('q', '').lower()
    students = read_students()
    
    results = [s for s in students if 
               query in s['name'].lower() or
               query in s['email'].lower() or
               query in s['course'].lower()]
    
    return jsonify(results), 200

if __name__ == '__main__':
    init_db()
    print("🎓 Student Management System Backend")
    print("📍 Running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)