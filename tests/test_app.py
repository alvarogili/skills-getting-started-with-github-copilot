"""
Backend tests for Mergington High School Activities API.
Uses Arrange-Act-Assert (AAA) pattern for clear test structure.
"""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint."""
    
    def test_root_redirects_to_static_page(self, client):
        """
        Test that the root endpoint redirects to the static HTML page.
        
        Arrange: TestClient is ready
        Act: GET request to /
        Assert: Status 307 (temporary redirect) and location header points to /static/index.html
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivitiesEndpoint:
    """Tests for GET /activities endpoint."""
    
    def test_get_all_activities_returns_success(self, client):
        """
        Test that retrieving activities returns status 200 with all activities.
        
        Arrange: TestClient with reset activities
        Act: GET request to /activities
        Assert: Status 200, response is dict with 9 activities
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert isinstance(activities_data, dict)
        assert len(activities_data) == 9
    
    def test_activities_contain_required_fields(self, client):
        """
        Test that each activity has all required fields.
        
        Arrange: TestClient with reset activities
        Act: GET request to /activities, extract first activity
        Assert: All required fields present (description, schedule, max_participants, participants)
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        first_activity = activities_data[list(activities_data.keys())[0]]
        
        # Assert
        assert "description" in first_activity
        assert "schedule" in first_activity
        assert "max_participants" in first_activity
        assert "participants" in first_activity
        assert isinstance(first_activity["participants"], list)
    
    def test_activities_have_correct_participant_data(self, client):
        """
        Test that specific activities contain expected participant data.
        
        Arrange: TestClient with reset activities (Chess Club has 2 participants)
        Act: GET request to /activities, extract Chess Club
        Assert: Chess Club has 2 participants (michael@mergington.edu, daniel@mergington.edu)
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        chess_club = activities_data["Chess Club"]
        
        # Assert
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_successful_signup_adds_participant(self, client, test_data):
        """
        Test that a new student can successfully sign up for an activity.
        
        Arrange: Valid activity name (Chess Club), valid new email (newstudent@mergington.edu)
        Act: POST request to /activities/Chess%20Club/signup?email=newstudent@mergington.edu
        Assert: Status 200, response contains success message, participant added to activity
        """
        # Arrange
        activity = test_data["valid_activity"]
        email = test_data["valid_email"]
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity in result["message"]
    
    def test_duplicate_signup_rejected(self, client, test_data):
        """
        Test that a student cannot sign up twice for the same activity.
        
        Arrange: Student already in Chess Club (michael@mergington.edu)
        Act: POST request to sign up the same student again
        Assert: Status 400, error message indicates already signed up
        """
        # Arrange
        activity = test_data["valid_activity"]  # Chess Club
        email = test_data["existing_email_in_chess"]  # michael@mergington.edu
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "already signed up" in result["detail"].lower()
    
    def test_signup_to_nonexistent_activity_returns_404(self, client, test_data):
        """
        Test that signing up for a non-existent activity returns 404.
        
        Arrange: Invalid activity name (NonExistentActivity)
        Act: POST request to /activities/NonExistentActivity/signup with valid email
        Assert: Status 404, error message indicates activity not found
        """
        # Arrange
        activity = test_data["invalid_activity"]
        email = test_data["valid_email"]
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not found" in result["detail"].lower()
    
    def test_signup_without_email_parameter_returns_error(self, client, test_data):
        """
        Test that signup without email parameter returns validation error.
        
        Arrange: Valid activity but missing email parameter
        Act: POST request to /activities/Chess%20Club/signup (no email param)
        Assert: Status 422 (validation error), error in response
        """
        # Arrange
        activity = test_data["valid_activity"]
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup"
        )
        
        # Assert
        assert response.status_code == 422
    
    def test_signup_with_url_encoded_activity_name(self, client):
        """
        Test that activities with spaces in names can be signed up using URL encoding.
        
        Arrange: Activity name with space (Programming Class)
        Act: POST request with URL-encoded activity name
        Assert: Status 200, signup successful with correctly encoded name
        """
        # Arrange
        activity = "Programming Class"
        email = "newendpoint@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert activity in result["message"]
