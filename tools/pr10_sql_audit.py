"""Фактические SQL-запросы через панель Debug Toolbar (только DEBUG)."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moodtracker.settings")
os.environ["DJANGO_DEBUG"] = "1"

import django  # noqa: E402

django.setup()

from django.test import Client  # noqa: E402
from debug_toolbar.toolbar import DebugToolbar  # noqa: E402

collected = []


def remember(sender, toolbar, **kwargs):
    collected.append(toolbar)


DebugToolbar._created.connect(remember)
client = Client(REMOTE_ADDR="127.0.0.1")
for url in ("/entries/?sort=score&page=1", "/entries/1/",
            "/entries/statistics/"):
    response = client.get(url)
    assert response.status_code == 200
    assert b"djDebug" in response.content
    toolbar = collected[-1]
    stats = toolbar.get_panel_by_id("SQLPanel").get_stats()
    print(f"\n{url} — SQL: {len(stats['queries'])}")
    for query in stats["queries"]:
        print(query["raw_sql"])
