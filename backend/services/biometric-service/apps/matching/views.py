from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import match_face, verify_liveness

class MatchFaceView(APIView):
    def post(self, request):
        citizen_id = request.data.get('citizen_id')
        # In a real app, we'd handle file upload here.
        # For mock, we accept a path or base64 (simulated)
        image_path = request.data.get('image_path', 'temp/face.jpg')
        
        if not citizen_id:
            return Response({'error': 'citizen_id required'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Trigger Async Task
        task = match_face.delay(citizen_id, image_path)
        
        return Response({
            'task_id': task.id,
            'status': 'processing',
            'message': 'Face matching started'
        }, status=status.HTTP_202_ACCEPTED)

class LivenessView(APIView):
    def post(self, request):
        session_id = request.data.get('session_id')
        video_path = request.data.get('video_path', 'temp/liveness.mp4')
        
        # Trigger Async Task
        task = verify_liveness.delay(session_id, video_path)
        
        return Response({
            'task_id': task.id,
            'status': 'processing',
            'message': 'Liveness check started'
        }, status=status.HTTP_202_ACCEPTED)

class TaskStatusView(APIView):
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        return Response({
            'task_id': task_id,
            'status': task_result.status,
            'result': task_result.result if task_result.ready() else None
        })
