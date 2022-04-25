from flask_login import current_user


def test_home(client):
    response = client.get('/home', follow_redirects=True)
    assert b'Please log in to access this page' in response.data

def test_home_no_login(client):
    response = client.get('/', follow_redirects=True)
    assert b'Please log in to access this page' in response.data

def test_home_with_login(logged_client):
    with logged_client:
        response = logged_client.get('/')
        assert current_user.username == 'admin'
        assert b'Hello' in response.data

def test_home_post_request(logged_client):
    with logged_client:
        response = logged_client.post('/', data={})
        assert response.status_code == 405

def test_my_account(logged_client):
    with logged_client:
        response = logged_client.get('/account')
        user_content = current_user.first_name + ' ' + current_user.last_name
        assert user_content.encode() in response.data

def test_account_valid_post(logged_client):
    with logged_client:
        response = logged_client.post('/account', data=dict(
            username = 'new_admin_username',
            first_name = 'Jaden',
            last_name = 'Suz',
            email = 'new_email@email.com'
        ), follow_redirects=True)
        assert response.status_code == 200

def test_update_invalid_username(logged_client):
    with logged_client:
        response = logged_client.post('/account', data=dict(
            username='josh',
        ), follow_redirects=True)
        assert b'Username already exists' in response.data

def test_update_invalid_email(logged_client):
    with logged_client:
        response = logged_client.post('/account', data=dict(
            email='josh@email.com',
        ), follow_redirects=True)
        assert b'Email already exists' in response.data

def test_register_new_user(logged_client):
    with logged_client:
        response = logged_client.get('/register')
        assert b'Register A New User' in response.data

def test_logout(logged_client):
    with logged_client:
        response = logged_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data

