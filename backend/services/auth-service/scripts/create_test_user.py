
import os
import sys
import django
from django.contrib.auth import get_user_model
from apps.authentication.models import CitizenProfile

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

User = get_user_model()

def create_test_user():
    national_id = "12345678"
    pin = "1234"
    
    # Check if exists
    if User.objects.filter(username=national_id).exists():
        print(f"User {national_id} already exists.")
        return

    print(f"Creating user {national_id}...")
    user = User.objects.create_user(
        username=national_id,
        password=pin # In real app, PIN might be hashed differently, but using standard auth for now
    )
    
    # Create Profile
    # Assuming CitizenProfile exists and links to User
    try:
        profile = CitizenProfile.objects.create(
            user=user,
            national_id=national_id,
            phone_number="0700000000"
        )
        print("Profile created.")
    except Exception as e:
        print(f"Profile creation skipped or failed: {e}")

    print("User setup complete.")

if __name__ == "__main__":
    create_test_user()
