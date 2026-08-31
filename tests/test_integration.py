"""Integration tests for multi-step workflows using the AAA (Arrange-Act-Assert) pattern."""

import pytest


@pytest.mark.integration
class TestSignupAndView:
    """Tests for signup workflow followed by verification."""

    def test_signup_then_view_in_activities_list(self, client, reset_activities, sample_email):
        """Test that a newly signed up participant appears in the activities list."""
        # Arrange
        activity_name = "Debate Team"

        # Act - Sign up
        signup_response = client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Act - Verify in list
        activities_response = client.get("/activities")
        activities_data = activities_response.json()

        # Assert
        assert signup_response.status_code == 200
        assert activities_response.status_code == 200
        assert sample_email in activities_data[activity_name]["participants"]

    def test_signup_increments_participant_count(self, client, reset_activities, sample_email):
        """Test that participant count increases after signup."""
        # Arrange
        activity_name = "Science Club"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        client.post(f"/activities/{activity_name}/signup?email={sample_email}")
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])

        # Assert
        assert updated_count == initial_count + 1


@pytest.mark.integration
class TestSignupAndDelete:
    """Tests for signup followed by deletion workflow."""

    def test_signup_then_delete_removes_participant(self, client, reset_activities, sample_email):
        """Test that a participant can be deleted after signup."""
        # Arrange
        activity_name = "Basketball Team"

        # Act - Sign up
        client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Act - Verify signup
        verify_response = client.get("/activities")
        assert sample_email in verify_response.json()[activity_name]["participants"]

        # Act - Delete
        delete_response = client.delete(f"/activities/{activity_name}/participants/{sample_email}")

        # Assert delete succeeds
        assert delete_response.status_code == 200

        # Act - Verify removal
        final_response = client.get("/activities")

        # Assert participant is removed
        assert sample_email not in final_response.json()[activity_name]["participants"]

    def test_signup_delete_then_signup_again(self, client, reset_activities, sample_email):
        """Test that a participant can signup again after being deleted."""
        # Arrange
        activity_name = "Art Studio"

        # Act - Sign up
        client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Act - Delete
        client.delete(f"/activities/{activity_name}/participants/{sample_email}")

        # Act - Sign up again
        second_signup = client.post(f"/activities/{activity_name}/signup?email={sample_email}")

        # Assert
        assert second_signup.status_code == 200

        # Verify they're back in the list
        activities_response = client.get("/activities")
        assert sample_email in activities_response.json()[activity_name]["participants"]


@pytest.mark.integration
class TestMultipleSignups:
    """Tests for multiple participants signing up for the same activity."""

    def test_multiple_signups_all_appear_in_list(self, client, reset_activities):
        """Test that multiple different students all appear in the activity."""
        # Arrange
        activity_name = "Tennis Club"
        emails = [
            "alice@mergington.edu",
            "bob@mergington.edu",
            "charlie@mergington.edu"
        ]

        # Act - All sign up
        for email in emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200

        # Act - Verify
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]

        # Assert
        for email in emails:
            assert email in participants

    def test_activity_respects_max_participants_count(self, client, reset_activities):
        """Test that activity correctly tracks participants against max capacity."""
        # Arrange
        activity_name = "Tennis Club"
        max_participants = 16
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        new_emails = [f"student{i}@mergington.edu" for i in range(5)]
        for email in new_emails:
            client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        final_response = client.get("/activities")
        activity_data = final_response.json()[activity_name]
        final_count = len(activity_data["participants"])
        
        # Verify count increased correctly
        assert final_count == initial_count + 5
        # Verify max capacity isn't exceeded (we're not at max yet)
        assert final_count <= max_participants


@pytest.mark.integration
class TestDeleteAndReverify:
    """Tests for delete operations and verification."""

    def test_delete_frees_up_capacity(self, client, reset_activities):
        """Test that deleting a participant frees up a spot in the activity."""
        # Arrange
        activity_name = "Chess Club"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act - Delete a participant
        email_to_delete = "michael@mergington.edu"
        client.delete(f"/activities/{activity_name}/participants/{email_to_delete}")

        # Act - Verify count decreased
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])

        # Assert
        assert final_count == initial_count - 1

    def test_delete_specific_participant_preserves_others(self, client, reset_activities):
        """Test that deleting one participant doesn't affect others."""
        # Arrange
        activity_name = "Programming Class"
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"].copy()

        # Act - Delete first participant
        email_to_delete = initial_participants[0]
        client.delete(f"/activities/{activity_name}/participants/{email_to_delete}")

        # Act - Verify
        final_response = client.get("/activities")
        final_participants = final_response.json()[activity_name]["participants"]

        # Assert - Deleted participant is gone
        assert email_to_delete not in final_participants

        # Assert - Other participants remain
        for email in initial_participants[1:]:
            assert email in final_participants
