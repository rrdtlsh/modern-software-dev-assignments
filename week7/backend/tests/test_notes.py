def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_notes_pagination(client):
    for i in range(5):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
    r = client.get("/notes/", params={"skip": 1, "limit": 2})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2


def test_notes_sorting(client):
    for title in ["Zebra", "Apple", "Mango"]:
        client.post("/notes/", json={"title": title, "content": "x"})
    r = client.get("/notes/", params={"sort": "title"})
    assert r.status_code == 200
    items = r.json()
    titles = [n["title"] for n in items]
    assert titles == sorted(titles)

