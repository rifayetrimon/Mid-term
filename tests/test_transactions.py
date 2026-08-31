def test_create_transaction(client, headers):
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "title": "Salary",
            "amount": 5000,
            "type": "income",
            "category": "Job",
            "date": "2025-01-01",
        },
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Salary"
    assert response.json()["amount"] == 5000


def test_get_all_transactions(client, headers, transaction):
    response = client.get("/transactions", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Lunch"


def test_get_single_transaction(client, headers, transaction):
    response = client.get("/transactions/" + str(transaction["id"]), headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == transaction["id"]

    missing = client.get("/transactions/999", headers=headers)
    assert missing.status_code == 404


def test_update_transaction(client, headers, transaction):
    response = client.put(
        "/transactions/" + str(transaction["id"]),
        headers=headers,
        json={
            "title": "Dinner",
            "amount": 500,
            "type": "expense",
            "category": "Food",
            "date": "2025-01-11",
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Dinner"
    assert response.json()["amount"] == 500


def test_delete_transaction(client, headers, transaction):
    response = client.delete("/transactions/" + str(transaction["id"]), headers=headers)
    assert response.status_code == 200

    again = client.delete("/transactions/" + str(transaction["id"]), headers=headers)
    assert again.status_code == 404
