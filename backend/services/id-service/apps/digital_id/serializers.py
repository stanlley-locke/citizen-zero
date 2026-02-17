from rest_framework import serializers
from .models import DigitalID, IssuanceRequest

class DigitalIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalID
        fields = '__all__'

class IssuanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuanceRequest
        fields = '__all__'
