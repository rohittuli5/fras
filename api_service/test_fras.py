import os
import tempfile
import json
import pytest
import fras_app
import common
from io import BytesIO
@pytest.fixture
def client():
    db_fd, fras_app.app.config['DATABASE'] = tempfile.mkstemp()
    fras_app.app.config['TESTING'] = True

    with fras_app.app.test_client() as client:
        with fras_app.app.app_context():
            fras_app.init()
        yield client

    os.close(db_fd)
    os.unlink(fras_app.app.config['DATABASE'])

def login(client, username, password):
    x={
        "login_id":username,
        "password":password
    }

    return client.post('fras/app/login', data=json.dumps(x), follow_redirects=True)


def logout(client):
    return client.get('fras/app/logout', follow_redirects=True)

def login_logout_test(client):
    # logout test, success expected
    rv = login(client, "admin", "admin")
    assert b'nav' in rv.data
    # logout test, success expected
    rv = logout(client)
    assert b'Logged out.' in rv.data
    # login test, wrong username, failiure expected
    rv = login(client, "admin"+'x', "admin")
    assert b'Invalid user/password.' in rv.data
    # login test, wrong password, failiure expected
    rv = login(client, "admin", "admin" + 'x')
    assert b'Invalid user/password.' in rv.data

def curr_user_test(client):
    #current_user test when logged in, success expected
    rv = login(client, "admin", "admin")
    rv = client.get('fras/app/current_user', follow_redirects="True")
    assert b'user' in rv.data

    #current_user test when logged out, failiure expected
    rv = logout(client)
    rv = client.get('fras/app/current_user', follow_redirects="True")
    assert b'User not logged in.' in rv.data


def users_upload_test(client):
    rv = login(client, "admin", "admin")
    rv = client.post('fras/app/users_upload', content_type='multipart/form-data', data = {
            "users_file": (BytesIO(b'FILE CONTENT'), '../test_data/users.csv')
        }, follow_redirects=True)
    assert b'Users added successfully!' in rv.data

    rv = logout(client)
    rv = login(client, "test", "test")
    rv = client.post('fras/app/users_upload', content_type='multipart/form-data', data = {
            "users_file": (BytesIO(b'FILE CONTENT'), '../test_data/users.csv')
        }, follow_redirects=True)

    assert b'Operation not allowed' in rv.data
    rv = login(client, "admin", "admin")
    rv = client.post('fras/app/users_upload', content_type='multipart/form-data', data={ "users_file":" ",
    }, follow_redirects=True)
    assert b'Error when handling users upload request.' in rv.data

def kface_bulk_add_test(client):
    rv = login(client, "admin", "admin")
    rv = client.post('fras/app/kface_bulk_add', content_type='multipart/form-data', data = {
            "zip_file": (BytesIO(b'FILE CONTENT'), '../test_data/Archieve.zip')
        }, follow_redirects=True)
    assert b'Saved' in rv.data
    rv = login(client, "admin", "admin")
    rv = client.post('fras/app/kface_bulk_add', content_type='multipart/form-data', data = {
            "zip_file": (BytesIO(b'FILE CONTENT'), '')
        }, follow_redirects=True)
    assert b'No file supplied!' in rv.data
    rv = client.post('fras/app/kface_bulk_add', content_type='multipart/form-data', data = {}, follow_redirects=True)
    assert b'Error when handling ZIP file.' in rv.data

def kface_find_test(client):
    rv = login(client, "admin", "admin")
    rv = client.post('fras/app/kface',  data = json.dumps({
            "pg_no":1,
            "first_name":"Amitabh",
            

        }), follow_redirects=True)
    assert b'pg_size' in rv.data
    rv = client.post('fras/app/kface', content_type='multipart/form-data', data = {
            "pg_no":1,
            "first_name":"Amitabh"

        }, follow_redirects=True)
    assert b'Error when finding known faces.' in rv.data


def kface_id_test(client):
    rv = login(client, "admin", "admin")
    rv = client.get('fras/app/kface/0', follow_redirects=True)
    assert b'Error when fetching known face.' in rv.data

def kface_save_test(client):
    rv = login(client, "admin", "admin")
    image=open("../test_data/amitabh.jpg")
    data={
        'photo':image.read(),
        'id':0,
    }
    rv = client.post('fras/app/kface_save',data=json.dumps(data), follow_redirects=True)
def test_all_tests(client):
    login_logout_test(client)
    curr_user_test(client)
    users_upload_test(client)
    kface_bulk_add_test(client)
    kface_find_test(client)
    kface_id_test(client)
    #kface_save_test(client)
    
    