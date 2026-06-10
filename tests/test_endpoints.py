from fastapi import status


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in {status.HTTP_307_TEMPORARY_REDIRECT, status.HTTP_308_PERMANENT_REDIRECT}
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == status.HTTP_200_OK
    activities = response.json()

    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(activities["Chess Club"]["participants"], list)


def test_signup_for_activity_success(client):
    activity_name = "Art Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activity_response = client.get("/activities")
    activities = activity_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_for_nonexistent_activity_returns_404(client):
    response = client.post("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_when_already_registered_returns_400(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_success(client):
    activity_name = "Gym Class"
    email = "john@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activity_response = client.get("/activities")
    activities = activity_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_from_nonexistent_activity_returns_404(client):
    response = client.delete("/activities/Nope/participants", params={"email": "student@mergington.edu"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_registered_returns_404(client):
    activity_name = "Swimming Club"
    email = "notregistered@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Participant not found"
