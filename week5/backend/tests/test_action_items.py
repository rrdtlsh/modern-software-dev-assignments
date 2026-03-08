def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1


# ---------- Filter tests ----------


def _seed_items(client):
    """Create 3 items and complete the first one. Returns list of created items."""
    ids = []
    for desc in ["alpha", "beta", "gamma"]:
        r = client.post("/action-items/", json={"description": desc})
        ids.append(r.json())
    client.put(f"/action-items/{ids[0]['id']}/complete")
    return ids


def test_filter_completed_true(client):
    _seed_items(client)
    r = client.get("/action-items/", params={"completed": True})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["description"] == "alpha"
    assert items[0]["completed"] is True


def test_filter_completed_false(client):
    _seed_items(client)
    r = client.get("/action-items/", params={"completed": False})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    assert all(i["completed"] is False for i in items)


def test_filter_no_param_returns_all(client):
    _seed_items(client)
    r = client.get("/action-items/")
    assert r.status_code == 200
    assert len(r.json()) == 3


# ---------- Bulk-complete tests ----------


def test_bulk_complete_success(client):
    items = _seed_items(client)  # ids[0] already completed
    ids_to_complete = [items[1]["id"], items[2]["id"]]

    r = client.post("/action-items/bulk-complete", json={"ids": ids_to_complete})
    assert r.status_code == 200
    result = r.json()
    assert len(result) == 2
    assert all(i["completed"] is True for i in result)

    # All three should now be completed
    r = client.get("/action-items/", params={"completed": True})
    assert len(r.json()) == 3


def test_bulk_complete_missing_id_returns_404(client):
    items = _seed_items(client)
    r = client.post("/action-items/bulk-complete", json={"ids": [items[0]["id"], 9999]})
    assert r.status_code == 404
    assert "9999" in r.json()["detail"]


def test_bulk_complete_empty_ids_rejected(client):
    r = client.post("/action-items/bulk-complete", json={"ids": []})
    assert r.status_code == 422  # validation error


def test_bulk_complete_rollback_on_missing(client):
    """If any ID is missing the whole request fails; no items are updated."""
    items = _seed_items(client)
    # beta and gamma are incomplete; try to complete gamma + non-existent
    r = client.post("/action-items/bulk-complete", json={"ids": [items[2]["id"], 9999]})
    assert r.status_code == 404

    # gamma should still be incomplete
    r = client.get("/action-items/", params={"completed": False})
    descs = {i["description"] for i in r.json()}
    assert "gamma" in descs
