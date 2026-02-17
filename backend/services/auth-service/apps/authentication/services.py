import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class IPRSService:
    @staticmethod
    def verify_citizen(national_id):
        """
        Verifies if a citizen exists in the IPRS (Mock) service.
        Returns citizen data if found, otherwise None or raises exception.
        """
        base_url = settings.MOCK_IPRS_BASE_URL
        # Ensure no trailing slash issues
        if base_url.endswith('/'):
            base_url = base_url[:-1]
            
        url = f"{base_url}/citizens/{national_id}/"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                # Log error in production
                print(f"IPRS Error: {response.status_code} - {response.text}")
                return None
        except requests.RequestException as e:
            print(f"IPRS Connection Error: {e}")
            raise AuthenticationFailed("Unable to connect to Identity Service")
