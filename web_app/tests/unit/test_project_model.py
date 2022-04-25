import datetime


def test_new_project(new_project):
    assert new_project.name == 'Project One'
    assert new_project.description == 'Project One Description'
    assert new_project.start_date == datetime.date(2022, 5, 4)
    assert new_project.deadline == datetime.date(2022, 6, 10)

def test_add_user_to_project(new_project, new_user):
    new_project.users = [new_user]
    assert new_project.name == 'Project One'
    assert new_project.description == 'Project One Description'
    assert new_project.start_date == datetime.date(2022, 5, 4)
    assert new_project.deadline == datetime.date(2022, 6, 10)
    assert new_user in new_project.users

def test_add_team_to_project(new_project, new_team):
    new_project.teams = [new_team]
    assert new_project.name == 'Project One'
    assert new_project.description == 'Project One Description'
    assert new_project.start_date == datetime.date(2022, 5, 4)
    assert new_project.deadline == datetime.date(2022, 6, 10)
    assert new_team in new_project.teams
