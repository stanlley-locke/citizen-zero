from django.urls import path
from .views import MatchFaceView, LivenessView, TaskStatusView

urlpatterns = [
    path('match-face/', MatchFaceView.as_view(), name='match_face'),
    path('liveness/', LivenessView.as_view(), name='liveness'),
    path('tasks/<str:task_id>/', TaskStatusView.as_view(), name='task_status'),
]
