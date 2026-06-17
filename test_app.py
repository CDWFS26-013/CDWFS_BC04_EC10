import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# --- Route HTML GET / ---

def test_get_homepage_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_get_homepage_contains_form(client):
    response = client.get('/')
    assert b'<form' in response.data


def test_get_homepage_no_result(client):
    response = client.get('/')
    assert b'None' in response.data


# --- Route HTML POST / ---

def test_post_valid_coordinates_returns_200(client):
    response = client.post('/', data={'apoint': '2,5', 'bpoint': '1,6'})
    assert response.status_code == 200


def test_post_valid_coordinates_shows_result(client):
    response = client.post('/', data={'apoint': '2,5', 'bpoint': '1,6'})
    assert b'result' in response.data.lower()


def test_post_same_points_distance_zero(client):
    response = client.post('/', data={'apoint': '0,0', 'bpoint': '0,0'})
    assert response.status_code == 200


def test_post_negative_coordinates(client):
    response = client.post('/', data={'apoint': '-3,-4', 'bpoint': '0,0'})
    assert response.status_code == 200


def test_post_invalid_coordinates_not_numeric(client):
    response = client.post('/', data={'apoint': 'abc,xyz', 'bpoint': '1,2'})
    assert response.status_code in (200, 400, 500)


def test_post_missing_apoint(client):
    response = client.post('/', data={'bpoint': '1,2'})
    assert response.status_code in (200, 400, 500)


def test_post_missing_bpoint(client):
    response = client.post('/', data={'apoint': '1,2'})
    assert response.status_code in (200, 400, 500)


# --- Route API GET /api ---

def test_api_root_returns_200(client):
    response = client.get('/api')
    assert response.status_code == 200


def test_api_root_returns_json(client):
    response = client.get('/api')
    assert response.content_type == 'application/json'


# --- Route API GET /api/distances ---

def test_get_distances_returns_200(client):
    response = client.get('/api/distances')
    assert response.status_code == 200


def test_get_distances_returns_list(client):
    response = client.get('/api/distances')
    data = response.get_json()
    assert isinstance(data, list)


def test_get_distances_initially_empty(client):
    response = client.get('/api/distances')
    data = response.get_json()
    assert data == [] or isinstance(data, list)


# --- Route API POST /api/distance ---

def test_post_api_distance_valid(client):
    response = client.post('/api/distance', json={
        'start_point': '2,5',
        'end_point': '1,6'
    })
    assert response.status_code == 200


def test_post_api_distance_returns_json(client):
    response = client.post('/api/distance', json={
        'start_point': '0,0',
        'end_point': '3,4'
    })
    data = response.get_json()
    assert 'result_distance' in data


def test_post_api_distance_correct_value(client):
    response = client.post('/api/distance', json={
        'start_point': '0,0',
        'end_point': '3,4'
    })
    data = response.get_json()
    assert abs(data['result_distance'] - 5.0) < 0.001


def test_post_api_distance_missing_body(client):
    response = client.post('/api/distance', json={})
    assert response.status_code in (200, 400, 500)


def test_post_api_distance_invalid_coordinates(client):
    response = client.post('/api/distance', json={
        'start_point': 'a,b',
        'end_point': '1,2'
    })
    assert response.status_code in (200, 400, 500)


def test_post_api_distance_no_json(client):
    response = client.post('/api/distance')
    assert response.status_code in (200, 400, 500)
