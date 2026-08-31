"""Test error handling and edge cases using the AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestSignupErrorCases:
    """Tests for signup endpoint error scenarios."""

    def test_signup_to_nonexistent_activity_returns_404(self, client, reset_activities, sample_email):
        """Test that signup to a non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_already_registered_returns_400(self, client, reset_activities):
        """Test that signup fails if student is already registered."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered in reset_activities

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_same_student_twice_returns_400(self, client, reset_activities, sample_email):
        """Test that the same student cannot signup twice for the same activity."""
        # Arrange
        activity_name = "Art Studio"

        # Act
        response1 = client.post(f"/activities/{activity_name}/signup?email={sample_email}")
        response2 = client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Assert
        assert response1.status_code == 200  # First signup succeeds
        assert response2.status_code == 400  # Second signup fails
        assert "already signed up" in response2.json()["detail"]


class TestDeleteParticipantErrorCases:
    """Tests for delete participant endpoint error scenarios."""

    def test_delete_from_nonexistent_activity_returns_404(self, client, reset_activities, sample_email):
        """Test that deleting from a non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{sample_email}")

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_delete_nonexistent_participant_returns_404(self, client, reset_activities):
        """Test that deleting a non-existent participant returns 404."""
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_delete_participant_not_in_activity_returns_404(self, client, reset_activities):
        """Test that deleting a participant not in the activity returns 404."""
        # Arrange
        activity_name = "Chess Club"
        email = "sofia@mergington.edu"  # Not in Chess Club participants

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]


class TestDeleteParticipantSuccess:
    """Tests for successful delete operations."""

    def test_delete_participant_removes_from_activity(self, client, reset_activities):
        """Test that deleting a participant actually removes them."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]

        # Verify participant is removed
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email not in participants

    def test_delete_participant_success_response_format(self, client, reset_activities):
        """Test that successful delete returns proper response."""
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Removed" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]
