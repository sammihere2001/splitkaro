import pytest


@pytest.fixture
def flat(client, make_user):
    """Three flatmates in one group. Returns (group_id, {name: (user_id, headers)})."""
    users = {
        "ali": make_user("Ali", "ali@example.com"),
        "sara": make_user("Sara", "sara@example.com"),
        "hamza": make_user("Hamza", "hamza@example.com"),
    }
    ali_headers = users["ali"][1]
    group_id = client.post("/groups", json={"name": "Flat 4B"}, headers=ali_headers).json()["id"]
    for email in ("sara@example.com", "hamza@example.com"):
        res = client.post(f"/groups/{group_id}/members", json={"email": email}, headers=ali_headers)
        assert res.status_code == 200, res.text
    return group_id, users


def test_creator_is_a_member(client, make_user):
    user_id, headers = make_user("Ali", "ali@example.com")

    group = client.post("/groups", json={"name": "Trip to Murree"}, headers=headers).json()

    assert [m["id"] for m in group["members"]] == [user_id]
    assert client.get("/groups", headers=headers).json()[0]["name"] == "Trip to Murree"


def test_non_members_cannot_see_a_group(client, make_user, flat):
    group_id, _ = flat
    _, outsider_headers = make_user("Outsider", "outsider@example.com")

    assert client.get(f"/groups/{group_id}", headers=outsider_headers).status_code == 404
    assert client.get(f"/groups/{group_id}/balances", headers=outsider_headers).status_code == 404


def test_adding_unknown_or_existing_member(client, flat):
    group_id, users = flat
    headers = users["ali"][1]

    unknown = client.post(f"/groups/{group_id}/members", json={"email": "nobody@example.com"}, headers=headers)
    again = client.post(f"/groups/{group_id}/members", json={"email": "sara@example.com"}, headers=headers)

    assert unknown.status_code == 404
    assert again.status_code == 409


def test_expense_is_split_equally_with_leftover_paisa(client, flat):
    group_id, users = flat

    res = client.post(
        f"/groups/{group_id}/expenses",
        json={"description": "Electricity bill", "amount": "100.00"},
        headers=users["ali"][1],
    )

    assert res.status_code == 201, res.text
    expense = res.json()
    assert expense["paid_by_id"] == users["ali"][0]
    assert sorted(s["amount"] for s in expense["shares"]) == ["33.33", "33.33", "33.34"]


def test_balances_after_expenses(client, flat):
    group_id, users = flat
    ali_id, ali = users["ali"]
    sara_id, sara = users["sara"]
    hamza_id, _ = users["hamza"]

    # Ali pays Rs 3000 rent split 3 ways; Sara pays Rs 600 for groceries for her and Hamza.
    client.post(f"/groups/{group_id}/expenses", json={"description": "Rent", "amount": "3000"}, headers=ali)
    client.post(
        f"/groups/{group_id}/expenses",
        json={"description": "Groceries", "amount": "600", "split_between": [sara_id, hamza_id]},
        headers=sara,
    )

    balances = {b["user_id"]: b["balance"] for b in client.get(f"/groups/{group_id}/balances", headers=ali).json()}

    assert balances == {ali_id: "2000.00", sara_id: "-700.00", hamza_id: "-1300.00"}


def test_invalid_expenses_are_rejected(client, make_user, flat):
    group_id, users = flat
    headers = users["ali"][1]
    outsider_id, _ = make_user("Outsider", "outsider@example.com")
    url = f"/groups/{group_id}/expenses"

    assert client.post(url, json={"description": "x", "amount": "0"}, headers=headers).status_code == 422
    assert client.post(url, json={"description": "x", "amount": "10.555"}, headers=headers).status_code == 422
    assert (
        client.post(url, json={"description": "x", "amount": "10", "paid_by_id": outsider_id}, headers=headers).status_code
        == 400
    )
    assert (
        client.post(url, json={"description": "x", "amount": "10", "split_between": [outsider_id]}, headers=headers).status_code
        == 400
    )


def test_only_payer_or_creator_can_delete(client, flat):
    group_id, users = flat
    sara = users["sara"][1]
    hamza = users["hamza"][1]
    ali = users["ali"][1]
    expense_id = client.post(
        f"/groups/{group_id}/expenses", json={"description": "Pizza", "amount": "1500"}, headers=sara
    ).json()["id"]

    assert client.delete(f"/groups/{group_id}/expenses/{expense_id}", headers=hamza).status_code == 403
    assert client.delete(f"/groups/{group_id}/expenses/{expense_id}", headers=ali).status_code == 204
    assert client.get(f"/groups/{group_id}/expenses", headers=ali).json() == []


def test_settle_up_endpoint(client, flat):
    group_id, users = flat
    ali_id, ali = users["ali"]
    client.post(f"/groups/{group_id}/expenses", json={"description": "Rent", "amount": "3000"}, headers=ali)

    res = client.get(f"/groups/{group_id}/settle-up", headers=ali)

    assert res.status_code == 200
    payments = res.json()
    assert len(payments) == 2
    assert all(p["to_user_id"] == ali_id and p["amount"] == "1000.00" for p in payments)
