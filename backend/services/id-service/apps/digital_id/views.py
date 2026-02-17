from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .models import DigitalID, IssuanceRequest
from .serializers import DigitalIDSerializer, IssuanceRequestSerializer
from .services.pdf_service import PDFService
import requests

# Mock IPRS URL - In prod, this would be in settings
IPRS_URL = "http://localhost:8005/api/v1/citizens/"

def health_check(request):
    return JsonResponse({"status": "ok", "service": "id-service"})

from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator

class DigitalIDViewSet(viewsets.ModelViewSet):
    queryset = DigitalID.objects.all()
    serializer_class = DigitalIDSerializer

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Returns stats for the dashboard in the format expected by Overview.jsx.
        Fetches real Citizen count from IPRS.
        """
        # 1. Local ID Stats
        total_ids = DigitalID.objects.count()
        pending = IssuanceRequest.objects.filter(status='PENDING').count()
        
        # 2. Fetch Citizen Stats from IPRS
        iprs_stats = {}
        try:
            # Call the new analytics endpoint
            response = requests.get(f"{IPRS_URL}analytics/")
            if response.status_code == 200:
                iprs_stats = response.json()
        except Exception as e:
            print(f"Error fetching IPRS stats: {e}")

        # Extract IPRS data or use fallbacks
        total_citizens = iprs_stats.get('demographics', {}).get('gender', {})
        # Sum of all gender counts = total citizens
        total_citizens_count = sum(total_citizens.values()) if total_citizens else 0

        # Trends
        trends = iprs_stats.get('trends', {
            "months": ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan"],
            "registrations": [0, 0, 0, 0, 0, 0]
        })

        # Demographics - County
        county_data = iprs_stats.get('demographics', {}).get('county', {})
        demo_labels = list(county_data.keys()) if county_data else ["N/A"]
        demo_sizes = list(county_data.values()) if county_data else [0]
        
        # Limit demographics to top 5 for UI cleanliness
        if len(demo_labels) > 5:
            sorted_demos = sorted(zip(demo_labels, demo_sizes), key=lambda x: x[1], reverse=True)[:5]
            demo_labels, demo_sizes = zip(*sorted_demos)

        return Response({
            "kpi": {
                "total_citizens": total_citizens_count if total_citizens_count > 0 else total_ids,
                "ids_issued": total_ids,
                "pending_reviews": pending
            },
            "trends": trends,
            "demographics": {
                "labels": demo_labels,
                "sizes": demo_sizes
            }
        })

class IssuanceRequestViewSet(viewsets.ModelViewSet):
    queryset = IssuanceRequest.objects.all()
    serializer_class = IssuanceRequestSerializer

class DocumentViewSet(viewsets.ViewSet):
    """
    ViewSet for generating and retrieving Identity Documents.
    """
    
    @method_decorator(xframe_options_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def _fetch_citizen_data(self, citizen_id):
        if not citizen_id:
            return None
        try:
            # Connect to IPRS Mock Service to get real-time data
            response = requests.get(f"{IPRS_URL}{citizen_id}/")
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return None

    def _generate_response(self, pdf_bytes, filename, download=False):
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        disposition = 'attachment' if download else 'inline'
        response['Content-Disposition'] = f'{disposition}; filename="{filename}"'
        # Crucial for iframe embedding in the dashboard
        response['X-Frame-Options'] = 'ALLOWALL'
        return response

    @action(detail=False, methods=['get'], url_path='preview')
    def preview(self, request):
        doc_type = request.query_params.get('type')
        citizen_id = request.query_params.get('citizen_id')
        
        citizen_data = self._fetch_citizen_data(citizen_id)
        if not citizen_data:
             return Response({"error": "Citizen not found"}, status=status.HTTP_404_NOT_FOUND)

        if doc_type == 'national_id':
             pdf = PDFService.generate_national_id(citizen_data)
             return self._generate_response(pdf, f"id_{citizen_id}.pdf")
        elif doc_type == 'passport':
             pdf = PDFService.generate_passport(citizen_data)
             return self._generate_response(pdf, f"passport_{citizen_id}.pdf")
        elif doc_type == 'birth_certificate':
             pdf = PDFService.generate_birth_certificate(citizen_data)
             return self._generate_response(pdf, f"birth_cert_{citizen_id}.pdf")
        
        return Response({"error": "Invalid document type"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='download')
    def download(self, request):
        doc_type = request.query_params.get('type')
        citizen_id = request.query_params.get('citizen_id')

        citizen_data = self._fetch_citizen_data(citizen_id)
        if not citizen_data:
             return Response({"error": "Citizen not found"}, status=status.HTTP_404_NOT_FOUND)

        if doc_type == 'national_id':
             pdf = PDFService.generate_national_id(citizen_data)
             return self._generate_response(pdf, f"id_{citizen_id}.pdf", download=True)
        elif doc_type == 'passport':
             pdf = PDFService.generate_passport(citizen_data)
             return self._generate_response(pdf, f"passport_{citizen_id}.pdf", download=True)
        elif doc_type == 'birth_certificate':
             pdf = PDFService.generate_birth_certificate(citizen_data)
             return self._generate_response(pdf, f"birth_cert_{citizen_id}.pdf", download=True)

        return Response({"error": "Invalid document type"}, status=status.HTTP_400_BAD_REQUEST)

class CitizenProxyViewSet(viewsets.ViewSet):
    """
    Proxy ViewSet to forward requests to IPRS.
    This ensures endpoints like /api/v1/citizens/ work on port 8001 as well.
    """
    def list(self, request):
        try:
            resp = requests.get(IPRS_URL, params=request.query_params)
            return Response(resp.json(), status=resp.status_code)
        except:
            return Response({"error": "IPRS Service Down"}, status=503)

    def retrieve(self, request, pk=None):
        try:
            resp = requests.get(f"{IPRS_URL}{pk}/")
            return Response(resp.json(), status=resp.status_code)
        except:
            return Response({"error": "IPRS Service Down"}, status=503)
