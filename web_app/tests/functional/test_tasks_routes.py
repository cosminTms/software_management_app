def test_projects(logged_client):
    with logged_client:
        response = logged_client.get('/tasks')
        assert b'Tasks Page' in response.data