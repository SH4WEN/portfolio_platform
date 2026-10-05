"""Ad-hoc verification for the 'Save Contact Info' button feature.

Renders the public portfolio page via Django's test client and checks that:
1. The button exists in the header.
2. The json_script contact payload is embedded and valid JSON.
"""
import json
import os
import re
import sys

import django

# Ensure the project root is importable when running from the scratch dir.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings  # noqa: E402  (after django.setup())

settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ["testserver"]

from django.test import Client as TestClient  # noqa: E402

from apps.clients.models import Client  # noqa: E402

client = Client.objects.filter(is_published=True).first() or Client.objects.first()
assert client, "No client found in the database"

tc = TestClient()
resp = tc.get(f"/p/{client.slug}/")
print("status:", resp.status_code)
html = resp.content.decode()

print("button present:", "save-contact-btn" in html)
print("json_script present:", "client-contact-data" in html)

match = re.search(
    r'<script id="client-contact-data"[^>]*>(.*?)</script>', html, re.S
)
assert match, "contact payload script tag not found"
payload = json.loads(match.group(1))
print("payload keys:", sorted(payload.keys()))
print("name:", payload["name"], "| email:", payload["email"], "| phone:", payload["phone"])
print("social link keys:", sorted(payload["social_links"].keys()))
