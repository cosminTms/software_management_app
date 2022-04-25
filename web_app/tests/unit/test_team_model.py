def test_new_team(new_team):
    assert new_team.name == 'Team One'
    assert new_team.description == 'Team One Description'

def test_add_user_to_team(new_team, new_user):
    new_team.users = [new_user]
    assert new_team.name == 'Team One'
    assert new_team.description == 'Team One Description'
    assert new_user in new_team.users