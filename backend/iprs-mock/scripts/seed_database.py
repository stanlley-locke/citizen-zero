
import os
import sys
import random
import datetime

# Add the project root to sys.path
# Assuming script is in backend/iprs-mock/scripts/
# We want backend/iprs-mock/ in path
current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file))
sys.path.append(project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iprs_mock.settings')
import django
django.setup()

from apps.citizens.models import Citizen

def generate_kenyan_id():
    return str(random.randint(10000000, 99999999))

def generate_phone():
    prefixes = ['070', '071', '072', '079', '075', '076']
    prefix = random.choice(prefixes)
    number = random.randint(100000, 999999)
    return f"{prefix}{number}"

FIRST_NAMES = ['John', 'Jane', 'James', 'Mary', 'Peter', 'Elizabeth', 'Joseph', 'Sarah', 'David', 'Grace', 'Samuel', 'Faith', 'Kevin', 'Esther', 'Brian', 'Mercy', 'George', 'Ann', 'Michael', 'Caroline', 'Kamau', 'Wanjiku', 'Ochieng', 'Atieno', 'Kiprop', 'Chebet', 'Juma', 'Aisha']
LAST_NAMES = ['Mwangi', 'Maina', 'Kamau', 'Njoroge', 'Kimani', 'Otieno', 'Odiwuor', 'Odhiambo', 'Okeyo', 'Kipkorir', 'Kiptoo', 'Kiprotich', 'Cheruiyot', 'Juma', 'Mohamed', 'Ali', 'Abdi', 'Hassan']
COUNTIES = ['047 - Nairobi', '001 - Mombasa', '013 - Kiambu', '032 - Nakuru', '027 - Uasin Gishu', '042 - Kisumu', '037 - Kakamega', '003 - Kilifi']

def seed_citizens(count=10000):
    print(f"Seeding {count} citizens...")
    citizens = []
    
    # Use bulk create for performance
    batch_size = 1000
    
    # Create Specific Test User
    test_citizen, created = Citizen.objects.get_or_create(
        national_id="12345678",
        defaults={
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": datetime.date(1995, 12, 4),
            "gender": "F",
            "place_of_birth": "Nairobi Hospital",
            "county_of_birth": "047 - Nairobi",
            "phone_number": "0700000000"
        }
    )
    if created:
        citizens.append(test_citizen)
        print("Test Citizen (12345678) staged for creation.")

    for i in range(count):
        dob = datetime.date(1960, 1, 1) + datetime.timedelta(days=random.randint(0, 20000))
        # Ensure at least 18
        if dob > datetime.date.today() - datetime.timedelta(days=18*365):
            dob = datetime.date(1990, 1, 1)

        citizen = Citizen(
            national_id=generate_kenyan_id(),
            first_name=random.choice(FIRST_NAMES),
            last_name=random.choice(LAST_NAMES),
            date_of_birth=dob,
            gender=random.choice(['M', 'F']),
            place_of_birth='Hospital',
            county_of_birth=random.choice(COUNTIES),
            phone_number=generate_phone()
        )
        citizens.append(citizen)
        
        if len(citizens) >= batch_size:
            # Handle potential ID collisions by ignoring or retrying, simpler to ignoring conflicts for mock
            Citizen.objects.bulk_create(citizens, ignore_conflicts=True)
            citizens = []
            print(f"Processed {i+1}...")

    if citizens:
        Citizen.objects.bulk_create(citizens, ignore_conflicts=True)
    
    print("Seeding complete.")
    count_actual = Citizen.objects.count()
    print(f"Total citizens in DB: {count_actual}")

if __name__ == "__main__":
    seed_citizens()
