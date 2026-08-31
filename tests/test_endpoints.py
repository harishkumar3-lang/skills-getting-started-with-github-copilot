"""Test core endpoint functionality using the AAA (Arrange-Act-Assert) pattern."""

import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all available activities."""
        # Arrange
        expected_activity_count = 9

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities

    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """Test that each activity has the required fields."""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"

    def test_get_activities_includes_participant_info(self, client, reset_activities):
        """Test that GET /activities returns participant lists."""
        # Arrange
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        chess_club = activities.get("Chess Club")
        assert chess_club is not None
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestGetRoot:
    """Tests for GET / endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """Test that GET / redirects to /static/index.html."""
        # Arrange
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307  # Redirect status code
        assert response.headers["location"] == "/static/index.html"


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_for_activity_success(self, client, reset_activities, sample_email):
        """Test successful signup for an activity."""
        # Arrange
        activity_name = "Chess Club"
        initial_count = len(activities := client.get("/activities").json()[activity_name]["participants"])

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert sample_email in response.json()["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities, sample_email):
        """Test that signup actually adds the participant to the activity."""
        # Arrange
        activity_name = "Programming Class"

        # Act
        client.post(f"/activities/{activity_name}/signup?email={sample_email}")
        response = client.get("/activities")

        # Assert
        activities_data = response.json()
        assert sample_email in activities_data[activity_name]["participants"]

    def test_signup_multiple_different_students(self, client, reset_activities):
        """Test that multiple different students can sign up for the same activity."""
        # Arrange
        activity_name = "Tennis Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"

        # Act
        response1 = client.post(f"/activities/{activity_name}/signup?email={email1}")
        response2 = client.post(f"/activities/{activity_name}/signup?email={email2}")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify both are in activity
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants
