"""Test cases for the API."""
from django.conf import settings
from django.test import TransactionTestCase
from django.test.runner import DiscoverRunner
from fastapi.testclient import TestClient
from tripagenda import logger
from tripagenda.asgi import app


reverse = app.router.url_path_for


class TestRunner(DiscoverRunner):
    """TestRunner class."""

    def teardown_databases(self, old_config, **kwargs):
        """Clean up DB connections after tests are run."""
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT
                pg_terminate_backend(pid) FROM pg_stat_activity WHERE
                pid <> pg_backend_pid() AND
                pg_stat_activity.datname =
                  '{settings.DATABASES["default"]["NAME"]}';"""
            )
            print(f"Killed {len(cursor.fetchall())} stale connections.")
        super().teardown_databases(old_config, **kwargs)


class SmokeTests(TransactionTestCase):
    """Smoke tests."""

    def __init__(self, *args, **kwargs):
        """Initialize the test client."""
        super().__init__(*args, **kwargs)
        self.c = TestClient(app)

    def setUp(self):
        """Initialize the test client parameters."""
        self.headers = {"Content-Type": "application/json"}
        self.data = {
            "user_id": "1",
            "ush_id": "1",
            "from_date": "2023-11-02",
            "to_date": "2023-11-05",
        }
        self.query_params = {"ush_id": "1"}

    def test_search_post_404(self):
        """Test search post 404."""
        logger.info("test_search_post_404")
        logger.info(reverse("search-post"))

        response = self.c.post(
            reverse("search-post"),
            headers=self.headers,
            json=self.data,
            params=self.query_params,
        )

        logger.info(response.status_code)
        logger.info(response.json())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Object not found."})
