
        

import pytest
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

def test_eye_is_detected_as_open():
    """
    Feeds the backend wide-open eye coordinates.
    The backend should calculate a high EAR and return eyeclosed: False.
    """
    with client.websocket_connect("/ws") as websocket:
        # Mock coordinates mimicking a wide-open eye (high vertical distance)
        mock_data = {
            "left": [
                {"x": 0.612, "y": 0.421, "z": -0.015},
                {"x": 0.628, "y": 0.408, "z": -0.018},
                {"x": 0.645, "y": 0.409, "z": -0.017},
                {"x": 0.658, "y": 0.423, "z": -0.012},
                {"x": 0.644, "y": 0.434, "z": -0.013},
                {"x": 0.627, "y": 0.435, "z": -0.014},
            ],
            "right": [
                {"x": 0.388, "y": 0.422, "z": -0.015},
                {"x": 0.372, "y": 0.409, "z": -0.018},
                {"x": 0.355, "y": 0.408, "z": -0.017},
                {"x": 0.342, "y": 0.424, "z": -0.012},
                {"x": 0.356, "y": 0.435, "z": -0.013},
                {"x": 0.373, "y": 0.434, "z": -0.014},
            ],
        }

        websocket.send_json(mock_data)
        response = websocket.receive_json()

        assert response["eyeclosed"] is False


