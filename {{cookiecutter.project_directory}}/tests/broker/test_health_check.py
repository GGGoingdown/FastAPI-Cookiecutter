import pytest
from app.broker import tasks


@pytest.mark.task
def test_health_check_task(app):
    result = tasks.health_check.delay().get()
    assert result == {"detail": "health"}, f"Error response: {result}"
