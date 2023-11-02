# TODO: not working yet, will fix later
from django.conf import settings
from django.test import TransactionTestCase
from django.test.runner import DiscoverRunner
from fastapi.testclient import TestClient

from .models import User
from tripagenda.asgi import app


# A convenient helper for getting URL paths by name.
reverse = app.router.url_path_for


class TestRunner(DiscoverRunner):
    def teardown_databases(self, old_config, **kwargs):
        # This is necessary because either FastAPI/Starlette or Django's
        # ORM isn't cleaning up the connections after it's done with
        # them.
        # The query below kills all database connections before
        # dropping the database.
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Warning: Naming this `self.client` leads Django to overwrite it
        # with its own test client.
        self.c = TestClient(app)

    def setUp(self):
        self.headers = {"Content-Type": "application/json"}
        self.data = {
            "user_id": "1",
            "ush_id": "1",
            "from_date":"2023-11-02",
            "to_date":"2023-11-05"
        }
        # add query paramater ush_id = 1
        self.query_params = {
            "ush_id": "1"
        }

    def test_search_post_404(self):
        response = self.c.post(reverse("search-post"), headers=self.headers, data=self.data, params=self.query_params)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Object not found."})
