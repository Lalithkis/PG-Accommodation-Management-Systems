import os
import django
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hostel_project.settings")
django.setup()

User = get_user_model()

# Get credentials from environment variables
username = os.environ.get('SUPERUSER_NAME')
email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('SUPERUSER_PASSWORD')

if username and password:
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}")
        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            print("Superuser created successfully!")
        except Exception as e:
            print(f"Error creating superuser: {e}")
    else:
        print(f"Superuser {username} already exists. Skipping creation.")
else:
    print("Environment variables SUPERUSER_NAME and SUPERUSER_PASSWORD not found. Skipping superuser creation.")
