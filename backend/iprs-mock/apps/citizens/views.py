from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import Citizen
from .serializers import CitizenSerializer

class CitizenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows citizens to be viewed or searched.
    """
    queryset = Citizen.objects.all().order_by('national_id')
    serializer_class = CitizenSerializer
    permission_classes = [permissions.AllowAny] # Open for dev mock
    filter_backends = [filters.SearchFilter]
    search_fields = ['national_id', 'first_name', 'last_name']
    lookup_field = 'national_id'

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """
        Returns aggregated statistics for analytics consumers (like ID Service).
        """
        # 1. Demographics
        gender_stats = Citizen.objects.values('gender').annotate(count=models.Count('gender'))
        county_stats = Citizen.objects.values('county_of_birth').annotate(count=models.Count('county_of_birth'))
        
        # 2. Trends (Mocking registration date based on DOB for now as reg_date might not exist)
        # In a real system, we'd use registration_date.
        
        return Response({
            "demographics": {
                "gender": {item['gender']: item['count'] for item in gender_stats},
                "county": {item['county_of_birth']: item['count'] for item in county_stats},
            },
            "trends": {
                # Just mocking trend data since we don't have a distinct registration date field confirmed yet
                 "months": ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan"],
                 "registrations": [120, 150, 180, 200, 160, 210] 
            }
        })

    def get_queryset(self):
        queryset = super().get_queryset()
        gender = self.request.query_params.get('gender')
        county = self.request.query_params.get('county')
        
        if gender:
            queryset = queryset.filter(gender=gender)
        if county:
            queryset = queryset.filter(county_of_birth__icontains=county)
            
        return queryset
