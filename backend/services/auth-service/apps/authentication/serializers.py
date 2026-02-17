from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .services import IPRSService
from django.contrib.auth.models import User

from .models import UserProfile

class LoginSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=20)
    
    def validate(self, attrs):
        national_id = attrs.get('national_id')
        
        # 1. Verify against IPRS
        try:
            citizen_data = IPRSService.verify_citizen(national_id)
        except Exception as e:
            raise serializers.ValidationError(str(e))
            
        if not citizen_data:
            raise serializers.ValidationError("Citizen not found in IPRS registry.")
            
        # 2. Get or Create local User
        user, created = User.objects.get_or_create(username=national_id)
        if created:
            user.set_unusable_password()
            user.save()
            # Ensure profile exists
            UserProfile.objects.create(user=user, role='CITIZEN')
        else:
            # Ensure profile exists for existing users too
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user, role='CITIZEN')
            
        attrs['user'] = user
        attrs['citizen_data'] = citizen_data
        attrs['role'] = user.profile.role
        return attrs

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        # Add custom claims
        token = refresh.access_token
        token['role'] = user.profile.role
        
        return {
            'refresh': str(refresh),
            'access': str(token),
            'role': user.profile.role
        }

class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, write_only=True, default='SYSTEM_ADMIN')
    organization = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login', 'password', 'role', 'organization']
        read_only_fields = ['id', 'last_login']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if hasattr(instance, 'profile'):
            ret['role'] = instance.profile.role
            ret['organization'] = instance.profile.organization
        return ret

    def create(self, validated_data):
        role = validated_data.pop('role', 'SYSTEM_ADMIN')
        organization = validated_data.pop('organization', '')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        
        # Permissions Logic
        # 1. Platform & Registry Access (Admin Dashboard)
        if role in ['SYSTEM_ADMIN', 'ADMIN', 'DATA_COLLECTOR', 'INVESTIGATOR']:
            user.is_staff = True
            user.is_superuser = (role in ['SYSTEM_ADMIN', 'ADMIN']) # Only root admins vary
            
        # 2. Employer Portal Access
        else:
            user.is_staff = False
            user.is_superuser = False
            
        user.save()
        
        # Create Profile
        UserProfile.objects.create(user=user, role=role, organization=organization)
        
        return user
