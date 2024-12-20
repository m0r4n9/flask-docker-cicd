import pytest
import json
from app import app, db, User
import time

@pytest.fixture(scope='session')
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db_test:5432/flask_db_test'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Ждем, пока база данных будет готова
    time.sleep(3)
    
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()  # На всякий случай удаляем старые таблицы
            db.create_all()  # Создаем новые таблицы
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture(autouse=True)
def cleanup():
    # Выполняется перед каждым тестом
    yield
    # Очистка после каждого теста
    with app.app_context():
        db.session.remove()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert json.loads(response.data)['status'] == 'OK'

def test_create_user(client):
    """Test user creation"""
    data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    response = client.post('/users',
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'User created successfully'

def test_get_users(client):
    """Test getting all users"""
    # Create a test user first
    data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    client.post('/users',
                data=json.dumps(data),
                content_type='application/json')
    
    # Get users
    response = client.get('/users')
    assert response.status_code == 200
    users = json.loads(response.data)
    assert len(users) == 1
    assert users[0]['username'] == 'testuser'

def test_update_user(client):
    """Test user update"""
    # Create a test user
    data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    client.post('/users',
                data=json.dumps(data),
                content_type='application/json')
    
    # Get user ID
    response = client.get('/users')
    users = json.loads(response.data)
    user_id = users[0]['id']
    
    # Update user
    update_data = {
        'username': 'updateduser',
        'email': 'updated@example.com'
    }
    response = client.put(f'/users/{user_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'User updated successfully'

def test_delete_user(client):
    """Test user deletion"""
    # Create a test user
    data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    client.post('/users',
                data=json.dumps(data),
                content_type='application/json')
    
    # Get user ID
    response = client.get('/users')
    users = json.loads(response.data)
    user_id = users[0]['id']
    
    # Delete user
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'User deleted successfully'

def test_404_error(client):
    """Test handling of non-existent routes"""
    response = client.get('/nonexistent')
    assert response.status_code == 404