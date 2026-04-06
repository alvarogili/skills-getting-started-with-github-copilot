"""
Pytest configuration and fixtures for FastAPI app tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def reset_activities():
    """
    Fixture to reset activities to initial state before each test.
    This ensures test isolation and prevents state pollution between tests.
    """
    # Store the initial state
    initial_activities = {
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
        "Basketball": {
            "description": "Practice basketball skills and play games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": []
        },
        "Soccer": {
            "description": "Learn soccer techniques and participate in matches",
            "schedule": "Wednesdays and Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 25,
            "participants": []
        },
        "Art Club": {
            "description": "Explore painting, drawing, and creative arts",
            "schedule": "Mondays, 3:00 PM - 4:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Drama Club": {
            "description": "Practice acting, theater, and stage performances",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop argumentation skills and debate current topics",
            "schedule": "Fridays, 4:00 PM - 5:00 PM",
            "max_participants": 12,
            "participants": []
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": []
        }
    }
    
    # Clear and reset the activities dictionary
    activities.clear()
    activities.update(initial_activities)
    
    yield
    
    # Cleanup: reset again after test
    activities.clear()
    activities.update(initial_activities)


@pytest.fixture
def client(reset_activities):
    """
    Fixture that provides a TestClient instance for testing the FastAPI app.
    Depends on reset_activities to ensure clean state.
    """
    return TestClient(app)


@pytest.fixture
def test_data():
    """
    Fixture that provides commonly used test data.
    """
    return {
        "valid_activity": "Chess Club",
        "valid_email": "newstudent@mergington.edu",
        "existing_email_in_chess": "michael@mergington.edu",
        "invalid_activity": "NonExistentActivity",
    }
