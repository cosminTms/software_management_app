def test_projects(logged_client):
    with logged_client:
        response = logged_client.get('/issues')
        assert b'Issues Page' in response.data