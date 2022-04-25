from web_app.models import Project


def test_projects(logged_client):
    with logged_client:
        response = logged_client.get('/projects')
        assert b'Projects' in response.data

def test_projects_not_allowed_post_request(logged_client):
    with logged_client:
        response = logged_client.post('/projects', data={})
        assert response.status_code == 405

def test_project(logged_client):
    with logged_client:
        project = Project.query.get(1)
        response = logged_client.get('/projects/1')
        assert project.name.encode() in response.data
        assert project.description.encode() in response.data
        assert project.deadline.strftime('%d %B %Y').encode() in response.data


def test_invalid_project_id(logged_client):
    with logged_client:
        response = logged_client.get('/projects/0')
        assert response.status_code == 404


def test_project_not_allowed_post_request(logged_client):
    with logged_client:
        response = logged_client.post('/projects/1', data={})
        assert response.status_code == 405

def test_new_project(logged_client):
    with logged_client:
        response = logged_client.get('/projects/new')
        assert b'New Project' in response.data
        assert b'Timetable' in response.data
        assert b'Project Manager' in response.data
        assert b'Teams' in response.data
        assert b'Members' in response.data