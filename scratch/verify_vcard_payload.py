"""Render the public portfolio and confirm the vCard payload fields are present.

Run with:  python manage.py runscript verify_vcard_payload
   or:     python manage.py shell < scratch/verify_vcard_payload.py
"""
import re

from django.test import Client as TestClient

from apps.clients.models import Client

client = Client.objects.filter(is_published=True).first() or Client.objects.first()
print("Client:", client.slug, "| style:", client.portfolio_style)

response = TestClient(SERVER_NAME="localhost").get("/p/" + client.slug + "/")
print("STATUS", response.status_code)

html = response.content.decode()
match = re.search(r'id="client-contact-data"[^>]*>(.*?)</script>', html, re.S)
payload = match.group(1).strip() if match else "NOT FOUND"
print("PAYLOAD", payload)

# Confirm the button markup is present with the vCard wiring.
print("HAS save-contact-btn:", 'id="save-contact-btn"' in html)
print("HAS buildVCard:", "function buildVCard" in html)
print("HAS text/vcard blob:", "text/vcard;charset=utf-8" in html)
