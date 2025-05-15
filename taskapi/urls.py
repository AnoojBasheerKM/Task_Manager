from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from taskapi import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('task-list/',views.TaskListView.as_view(), name='task-list'),
    path('task-update/<int:pk>/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task-completion-report/', views.TaskCompletionReportView.as_view(), name='task-completion-report'),
]
