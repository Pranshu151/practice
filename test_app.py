# import pytest
# from app import app as flask_app
#
# @pytest.fixture()
# def app():
#     return flask_app
#
# @pytest.fixture()
# def client(app):
#     return app.test_client()
#
# def test_home_route(client):
#     """
#     GIVEN a Flask application
#     WHEN the "/" route is requested (GET)
#     THEN check that the response is valid
#     """
#     response = client.get("/")
#     assert response.status_code == 200
#     assert b"Hello, this is the CI/CD demo!" in response.data
#
# def test_data_route(client):
#     """
#     GIVEN a Flask application
#     WHEN the "/data" route is requested (GET)
#     THEN check that the response is valid
#     """
#     response = client.get("/data")
#     assert response.status_code == 200
#     json_data = response.get_json()
#     assert json_data["status"] == "success"
#     assert json_data["value"] == 42

import pytest
from app import app as flask_app

@pytest.fixture()
def app():
    yield flask_app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_home_route(client):
    """
    GIVEN a Flask application
    WHEN the '/' route is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, this is the CI/CD demo!" in response.data

def test_data_route(client):
    """
    GIVEN a Flask application
    WHEN the '/data' route is requested (GET)
    THEN check that the JSON response is valid
    """
    response = client.get('/data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert json_data["value"] == 42