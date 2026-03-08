def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_get_note_by_id(client):
    payload = {"title": "Detail", "content": "Single note"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()

    r = client.get(f"/notes/{created['id']}")
    assert r.status_code == 200
    note = r.json()
    assert note["id"] == created["id"]
    assert note["title"] == "Detail"


def test_get_note_not_found(client):
    r = client.get("/notes/9999")
    assert r.status_code == 404
    data = r.json()
    assert data["detail"] == "Note not found"
