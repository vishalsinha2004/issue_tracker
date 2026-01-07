from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    IssueViewSet,
    TopAssigneesReport,
    AverageResolutionTimeReport
)

router = DefaultRouter()
router.register('issues', IssueViewSet, basename='issues')

urlpatterns = [
    path('reports/top-assignees/', TopAssigneesReport.as_view()),
    path('reports/latency/', AverageResolutionTimeReport.as_view()),
]

urlpatterns += router.urls
