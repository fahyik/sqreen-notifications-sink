import json
import mock
import pytest

from sqreen_sink import create_app
from sqreen_sink.config import TestingConfig


# Fixture to create an app object for testing purpose
@pytest.fixture
def app():
    test_app = create_app(config=TestingConfig)
    yield test_app


# Fixture to get the test client from an app
@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def mock_webhook_request():

    mock_data = """[
        {
            "application_id": "5bc77cc99ea9ae0015e2b2c0",
            "application_name": "sqreen_sink",
            "date_occurred": "2018-10-20T20:51:07.971000+00:00",
            "environment": "development",
            "event_category": "http_error",
            "event_kind": "bot_scanning",
            "humanized_description": "Potential Automated Vulnerability discovery from 127.0.0.1",
            "id": "5bcb953c20814e0007869b4f",
            "ips": [
                {
                    "address": "127.0.0.1",
                    "date_resolved": "2018-10-20T20:51:08.275000+00:00",
                    "is_tor": false
                }
            ],
            "risk": 50,
            "sqreen_payload_type": "security_event",
            "url": "https://my.sqreen.io/application/246801fd6d1d4f80a3aac3c42908c5c549de8eb541404d52ab3b2b2327cf2a57/events/5bcb953c20814e0007869b4f"
        }
    ]"""  # noqa

    return mock.Mock(
        get_data=mock.Mock(return_value=mock_data.encode('utf-8')),
        get_json=mock.Mock(return_value=json.loads(mock_data))
    )
