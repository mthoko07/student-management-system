"""
Backend API Tests for Student Management System
"""

import pytest
import json
import os
import sys
from app import app, init_db, validate_student

# Test configuration
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_data_file(tmp_path):
    """Create a temporary data file for testing"""
    test_file = tmp_path / "test_students.json"
    with open(test_file, 'w') as f:
        json.dump([], f)
    return test_file

# Test home endpoint
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'endpoints' in data

# Test get all students
def test_get_students(client):
    response = client.get('/api/students')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

# Test create student - valid data
def test_create_student_valid(client):
    student_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 20,
        'course': 'Computer Science'
    }
    response = client.post('/api/students',
                          data=json.dumps(student_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'John Doe'
    assert 'id' in data

# Test create student - invalid name
def test_create_student_invalid_name(client):
    student_data = {
        'name': 'J',
        'email': 'john@example.com',
        'age': 20,
        'course': 'Computer Science'
    }
    response = client.post('/api/students',
                          data=json.dumps(student_data),
                          content_type='application/json')
    assert response.status_code == 400

# Test create student - invalid email
def test_create_student_invalid_email(client):
    student_data = {
        'name': 'John Doe',
        'email': 'invalid-email',
        'age': 20,
        'course': 'Computer Science'
    }
    response = client.post('/api/students',
                          data=json.dumps(student_data),
                          content_type='application/json')
    assert response.status_code == 400

# Test create student - invalid age
def test_create_student_invalid_age(client):
    student_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 200,
        'course': 'Computer Science'
    }
    response = client.post('/api/students',
                          data=json.dumps(student_data),
                          content_type='application/json')
    assert response.status_code == 400

# Test get student by ID
def test_get_student_by_id(client):
    # First create a student
    student_data = {
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'age': 22,
        'course': 'Mathematics'
    }
    create_response = client.post('/api/students',
                                 data=json.dumps(student_data),
                                 content_type='application/json')
    created_student = json.loads(create_response.data)
    
    # Get the student
    response = client.get(f'/api/students/{created_student["id"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Jane Smith'

# Test get non-existent student
def test_get_nonexistent_student(client):
    response = client.get('/api/students/99999')
    assert response.status_code == 404

# Test update student
def test_update_student(client):
    # Create a student
    student_data = {
        'name': 'Bob Wilson',
        'email': 'bob@example.com',
        'age': 21,
        'course': 'Physics'
    }
    create_response = client.post('/api/students',
                                 data=json.dumps(student_data),
                                 content_type='application/json')
    created_student = json.loads(create_response.data)
    
    # Update the student
    updated_data = {
        'name': 'Bob Wilson Jr',
        'email': 'bob.jr@example.com',
        'age': 22,
        'course': 'Advanced Physics'
    }
    response = client.put(f'/api/students/{created_student["id"]}',
                         data=json.dumps(updated_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Bob Wilson Jr'
    assert data['age'] == 22

# Test update non-existent student
def test_update_nonexistent_student(client):
    updated_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'age': 20,
        'course': 'Test Course'
    }
    response = client.put('/api/students/99999',
                         data=json.dumps(updated_data),
                         content_type='application/json')
    assert response.status_code == 404

# Test delete student
def test_delete_student(client):
    # Create a student
    student_data = {
        'name': 'Alice Brown',
        'email': 'alice@example.com',
        'age': 19,
        'course': 'Chemistry'
    }
    create_response = client.post('/api/students',
                                 data=json.dumps(student_data),
                                 content_type='application/json')
    created_student = json.loads(create_response.data)
    
    # Delete the student
    response = client.delete(f'/api/students/{created_student["id"]}')
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get(f'/api/students/{created_student["id"]}')
    assert get_response.status_code == 404

# Test delete non-existent student
def test_delete_nonexistent_student(client):
    response = client.delete('/api/students/99999')
    assert response.status_code == 404

# Test search students
def test_search_students(client):
    # Create test students
    students = [
        {'name': 'Charlie Davis', 'email': 'charlie@example.com', 'age': 20, 'course': 'Biology'},
        {'name': 'Diana Evans', 'email': 'diana@example.com', 'age': 21, 'course': 'Chemistry'}
    ]
    
    for student in students:
        client.post('/api/students',
                   data=json.dumps(student),
                   content_type='application/json')
    
    # Search by name
    response = client.get('/api/students/search?q=charlie')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) >= 1
    assert any('Charlie' in s['name'] for s in data)

# Test validation function
def test_validate_student_function():
    # Valid student
    valid_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'age': 20,
        'course': 'Test Course'
    }
    is_valid, message = validate_student(valid_data)
    assert is_valid == True
    
    # Invalid name
    invalid_name = {
        'name': 'T',
        'email': 'test@example.com',
        'age': 20,
        'course': 'Test Course'
    }
    is_valid, message = validate_student(invalid_name)
    assert is_valid == False
    
    # Invalid email
    invalid_email = {
        'name': 'Test User',
        'email': 'invalid',
        'age': 20,
        'course': 'Test Course'
    }
    is_valid, message = validate_student(invalid_email)
    assert is_valid == False

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
