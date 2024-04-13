import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ats.settings")
django.setup()

from django.contrib.auth.models import User

DEMO_PASSWORD = "django99"

for username in ["peter", "bruce"]:
    user = User.objects.get(username=username)
    user.set_password(DEMO_PASSWORD)
    user.save()
    print(f"User {username} setup with password {DEMO_PASSWORD}")
