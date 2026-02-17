import os
import django
import sys
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'id_service.settings')
django.setup()

from apps.digital_id.models import DigitalID

def seed_ids():
    print("Seeding Digital IDs...")
    
    citizen_id = "12345678" # Demo User
    
    # Clear old IDs
    DigitalID.objects.all().delete()
    
    # 1. National ID (Maisha Namba)
    DigitalID.objects.create(
        citizen_id=citizen_id,
        doc_type="NATIONAL_ID",
        issuance_date=timezone.now() - timedelta(days=365),
        expiry_date=timezone.now() + timedelta(days=365*9),
        status='ACTIVE',
        details="Citizen Zero Foundational ID"
    )
    
    # 2. Driving License
    DigitalID.objects.create(
        citizen_id=citizen_id,
        doc_type="DRIVING_LICENSE",
        issuance_date=timezone.now() - timedelta(days=100),
        expiry_date=timezone.now() + timedelta(days=200),
        status='ACTIVE',
        details="Class B, C1"
    )

    # 3. KRA PIN
    DigitalID.objects.create(
        citizen_id=citizen_id,
        doc_type="TAX_PIN",
        issuance_date=timezone.now() - timedelta(days=1000),
        expiry_date=timezone.now() + timedelta(days=3000),
        status='ACTIVE', 
        details="A001234567Z"
    )
        
    print(f"Successfully seeded {DigitalID.objects.count()} credentials for user {citizen_id}")

if __name__ == '__main__':
    seed_ids()
