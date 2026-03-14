def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_action_items_pagination(client):
    for i in range(5):
        client.post("/action-items/", json={"description": f"Item {i}"})
    r = client.get("/action-items/", params={"skip": 1, "limit": 2})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2


def test_action_items_sorting(client):
    for desc in ["Zebra", "Apple", "Mango"]:
        client.post("/action-items/", json={"description": desc})
    r = client.get("/action-items/", params={"sort": "description"})
    assert r.status_code == 200
    items = r.json()
    descriptions = [a["description"] for a in items]
    assert descriptions == sorted(descriptions)

