from werkzeug.security import check_password_hash


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, first_name, last_name, username, and role fields are defined correctly
    """
    assert new_user.email == 'johnSmith@email.com'
    assert check_password_hash(new_user.password, 'password')
    assert new_user.first_name == 'John'
    assert new_user.last_name == 'Smith'
    assert new_user.username == 'john'
    assert new_user.roles[0].name == 'Developer'

def test_new_user_is_admin(admin_user):
    assert admin_user.roles[0].name == 'Admin'

def test_new_user_is_developer(developer_user):
    assert developer_user.roles[0].name == 'Developer'

def test_new_user_is_pm(pm_user):
    assert pm_user.roles[0].name == 'Project Manager'

def test_new_user_is_cto(cto_user):
    assert cto_user.roles[0].name == 'CTO'