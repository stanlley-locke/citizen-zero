from ..models import DigitalID
from django.utils import timezone
import datetime

class IssuanceService:
    @staticmethod
    @staticmethod
    def issue_id(citizen_id, doc_type='NATIONAL_ID'):
        # 1. Check if ID already exists
        existing_id = DigitalID.objects.filter(citizen_id=citizen_id, document_type=doc_type, status='ACTIVE').first()
        if existing_id:
             return {
                'status': 'exists',
                'citizen_id': citizen_id,
                'message': f'Active {doc_type} already exists',
                'document_number': existing_id.national_id
            }

        # 2. Persist new Digital ID
        # Generate a mock unique ID number based on type
        import random
        if doc_type == 'NATIONAL_ID':
            doc_number = f"ID-{citizen_id}" # Or random
        elif doc_type == 'PASSPORT':
            doc_number = f"A{random.randint(1000000, 9999999)}"
        elif doc_type == 'DRIVING_LICENSE':
            doc_number = f"DL-{random.randint(1000000, 9999999)}"
        else:
            doc_number = f"DOC-{random.randint(1000, 9999)}"

        # Mocking cryptographic keys for now
        new_id = DigitalID.objects.create(
            citizen_id=citizen_id,
            national_id=doc_number,
            document_type=doc_type,
            expiry_date=timezone.now() + datetime.timedelta(days=365*10), # 10 years
            public_key="mock_pub_key_12345",
            doc_type="org.iso.18013.5.1.mDL", # Technical standard
            status='ACTIVE'
        )

        return {
            'status': 'issued',
            'citizen_id': citizen_id,
            'document_type': doc_type,
            'document_number': new_id.national_id,
            'message': f'{doc_type} issued and persisted successfully'
        }
