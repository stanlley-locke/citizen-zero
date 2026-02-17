from rest_framework.views import APIView
from rest_framework.response import Response
from .apps import ConfigStore

class ConfigView(APIView):
    def get(self, request):
        """Get full configuration"""
        data = ConfigStore.load()
        return Response(data)

    def post(self, request):
        """Update configuration"""
        current = ConfigStore.load()
        updates = request.data
        
        # Deep update simple implementation
        if 'network' in updates:
            current['network'].update(updates['network'])
        if 'system' in updates:
            current['system'].update(updates['system'])
            
        ConfigStore.save(current)
        return Response({"success": True, "config": current})
