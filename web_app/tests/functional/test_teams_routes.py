def test_teams(logged_client):
    with logged_client:
        response = logged_client.get('/teams')
        assert b'Teams' in response.data

def test_teams_not_allowed_post_request(logged_client):
    with logged_client:
        response = logged_client.post('/teams', data={})
        assert response.status_code == 405

def test_new_team(logged_client):
    with logged_client:
        response = logged_client.get('/teams/new')
        assert b'New Team' in response.data
        assert b'Team Members' in response.data
        assert b'admin admin' in response.data

def test_team(logged_client):
    with logged_client:
        response = logged_client.get('/teams/1')
        assert b'Team One' in response.data
        assert b'Team One Description' in response.data

def test_invalid_team_id(logged_client):
    with logged_client:
        response = logged_client.get('/teams/0')
        assert response.status_code == 404

def test_team_not_allowed_post_request(logged_client):
    with logged_client:
        response = logged_client.post('/teams/1', data={})
        assert response.status_code == 405



