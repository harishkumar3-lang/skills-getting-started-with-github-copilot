"""Pytest configuration and fixtures for the Mergington High School API tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a FastAPI TestClient for making requests."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Reset activities to a known state before each test.
    This prevents test pollution and ensures test independence.
    """
    # Save original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for intramural and league play",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["marcus@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis skills development and friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["sarah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and various art mediums",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["luna@mergington.edu", "alex@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Mondays and Thursdays, 4:30 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills through competitive debate",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["james@mergington.edu", "grace@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts through hands-on activities",
            "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["tyler@mergington.edu"]
        }
    }

    # Clear current activities
    activities.clear()

    # Restore original state
    activities.update(original_activities)

    yield

    # Cleanup: restore to original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_email():
    """Provide a test email address for signup operations."""
    return "test.student@mergington.edu"


@pytest.fixture
def new_activity_name():
    """Provide a name for a non-existent activity."""
    return "Nonexistent Activity"
