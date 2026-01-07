import django_filters
from .models import Issue


class IssueFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')
    assignee = django_filters.NumberFilter(field_name='assignee_id')
    label = django_filters.CharFilter(field_name='labels__name')

    created_from = django_filters.DateFilter(
        field_name='created_at', lookup_expr='gte'
    )
    created_to = django_filters.DateFilter(
        field_name='created_at', lookup_expr='lte'
    )

    class Meta:
        model = Issue
        fields = ['status', 'assignee', 'label']
