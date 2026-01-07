from django.db import models
from apps.users.models import User


class Label(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Issue(models.Model):

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    version = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    labels = models.ManyToManyField(
        Label, through='IssueLabel', related_name='issues'
    )

    def __str__(self):
        return self.title


class IssueLabel(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('issue', 'label')


class Comment(models.Model):
    issue = models.ForeignKey(
        Issue, related_name='comments', on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class IssueHistory(models.Model):
    EVENT_CHOICES = [
        ('created', 'Created'),
        ('status_changed', 'Status Changed'),
        ('assignee_changed', 'Assignee Changed'),
        ('comment_added', 'Comment Added'),
        ('labels_updated', 'Labels Updated'),
    ]

    issue = models.ForeignKey(
        Issue,
        related_name='history',
        on_delete=models.CASCADE
    )

    event_type = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES
    )

    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue.title} - {self.event_type}"

