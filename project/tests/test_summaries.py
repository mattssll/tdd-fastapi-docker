# project/tests/test_summaries.py


import json


def test_post_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_post_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_get_summary(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]  # response from post request

    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_get_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("summaries/9999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_get_all_summaries(test_app_with_db):
    response_a = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response_a.json()["id"]
    response_b = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://newfoo.bar"})
    )
    summary_id_b = response_b.json()
    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1
    assert len(summary_id_b) == 2
