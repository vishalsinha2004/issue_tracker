from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import transaction
from django.utils import timezone
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField

import csv, io

from .models import Issue, Comment, Label, IssueLabel, IssueHistory
from .filters import IssueFilter
from .pagination import IssuePagination
from .serializers import (
    IssueSerializer,
    IssueUpdateSerializer,
    CommentSerializer,
    BulkStatusItemSerializer,
    IssueHistorySerializer,
    CSVImportSerializer
)


class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all().order_by('-created_at')
    serializer_class = IssueSerializer
    pagination_class = IssuePagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = IssueFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'resolved_at', 'status']


    def perform_create(self, serializer):
        issue = serializer.save()
        IssueHistory.objects.create(
            issue=issue,
            event_type='created',
            description='Issue was created'
        )

    def partial_update(self, request, *args, **kwargs):
        issue = self.get_object()
        old_status = issue.status
        old_assignee = issue.assignee

        serializer = IssueUpdateSerializer(issue, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if old_status != issue.status:
            IssueHistory.objects.create(
                issue=issue,
                event_type='status_changed',
                description=f"Status changed from {old_status} to {issue.status}"
            )

        if old_assignee != issue.assignee:
            IssueHistory.objects.create(
                issue=issue,
                event_type='assignee_changed',
                description='Assignee changed'
            )

        return Response(IssueSerializer(issue).data)

    
    @action(detail=True, methods=['post'])
    def comments(self, request, pk=None):
        issue = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(issue=issue)

        IssueHistory.objects.create(
            issue=issue,
            event_type='comment_added',
            description='Comment added'
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def labels(self, request, pk=None):
        issue = self.get_object()
        labels = request.data.get('labels', [])

        with transaction.atomic():
            IssueLabel.objects.filter(issue=issue).delete()
            for name in labels:
                label, _ = Label.objects.get_or_create(name=name)
                IssueLabel.objects.create(issue=issue, label=label)

        IssueHistory.objects.create(
            issue=issue,
            event_type='labels_updated',
            description='Labels updated'
        )
        return Response({"message": "Labels updated successfully"})

    
    @action(detail=False, methods=['post'])
    def bulk_status(self, request):
        serializer = BulkStatusItemSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            for item in serializer.validated_data:
                issue = Issue.objects.select_for_update().get(id=item['issue_id'])
                issue.status = item['status']
                if item['status'] == 'closed':
                    issue.resolved_at = timezone.now()
                issue.save()

        return Response({"message": "Bulk status update successful"})


    @action(
        detail=False,
        methods=['post'],
        serializer_class=CSVImportSerializer,
        parser_classes=[MultiPartParser, FormParser],
    )
    def import_csv(self, request):
        serializer = CSVImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data['file']
        reader = csv.DictReader(io.StringIO(file.read().decode('utf-8')))

        created, failed = 0, []

        for index, row in enumerate(reader, start=1):
            try:
                Issue.objects.create(
                    title=row['title'],
                    description=row['description'],
                    status=row.get('status', 'open')
                )
                created += 1
            except Exception as e:
                failed.append({"row": index, "error": str(e)})

        return Response({
            "total": created + len(failed),
            "created": created,
            "failed": failed
        }, status=status.HTTP_201_CREATED)

    
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        history = self.get_object().history.order_by('created_at')
        return Response(IssueHistorySerializer(history, many=True).data)


class TopAssigneesReport(APIView):
    def get(self, request):
        return Response(
            Issue.objects.filter(assignee__isnull=False)
            .values(assignee_id=F('assignee__id'), assignee_name=F('assignee__name'))
            .annotate(total_issues=Count('id'))
            .order_by('-total_issues')
        )




class AverageResolutionTimeReport(APIView):
    def get(self, request):
        data = Issue.objects.filter(resolved_at__isnull=False).annotate(
            resolution_time=ExpressionWrapper(
                F('resolved_at') - F('created_at'),
                output_field=DurationField()
            )
        ).aggregate(avg_resolution_time=Avg('resolution_time'))

        return Response(data)
