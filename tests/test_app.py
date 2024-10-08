import pytest
from crud_app import app, storage
from hypothesis import given, strategies as st

# Reset storage before every test
def clear_storage():
    storage.clear()

@given(name=st.text(), value=st.integers())
def test_create_item(name, value):
    clear_storage()
    with app.test_client() as client:
        response = client.post("/item", json={"name": name, "value": value})
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == name
        assert data["value"] == value

@given(item_id=st.integers(min_value=1))
def test_get_non_existing_item(item_id):
    clear_storage()
    with app.test_client() as client:
        response = client.get(f"/item/{item_id}")
        assert response.status_code == 404

@given(item_id=st.integers(min_value=1), name=st.text(), value=st.integers())
def test_update_item(item_id, name, value):
    clear_storage()
    with app.test_client() as client:
        # Add an item before updating
        client.post("/item", json={"name": "item1", "value": 1})
        response = client.put(f"/item/{item_id}", json={"name": name, "value": value})
        if item_id == 1:
            assert response.status_code == 200
        else:
            assert response.status_code == 404
