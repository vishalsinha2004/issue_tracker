from rest_framework import serializers
from .models import Issue, Comment, Label, IssueHistory
from apps.users.serializers import UserSerializer


# 🔹 CSV Import Serializer
class CSVImportSerializer(serializers.Serializer):
    file = serializers.FileField()


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author', 'body', 'created_at']
        read_only_fields = ['created_at']

    def validate_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment body cannot be empty.")
        return value


class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    labels = LabelSerializer(many=True, read_only=True)
    assignee_details = UserSerializer(source='assignee', read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'status',
            'assignee',
            'assignee_details',
            'version',
            'created_at',
            'resolved_at',
            'comments',
            'labels',
        ]
        read_only_fields = ['version', 'created_at']


class IssueUpdateSerializer(serializers.ModelSerializer):
    client_version = serializers.IntegerField(write_only=True)

    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'assignee', 'client_version']

    def validate(self, data):
        if data['client_version'] != self.instance.version:
            raise serializers.ValidationError("Version conflict detected.")
        return data

    def update(self, instance, validated_data):
        validated_data.pop('client_version')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.version += 1
        instance.save()
        return instance


class BulkStatusItemSerializer(serializers.Serializer):
    issue_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Issue.STATUS_CHOICES)


class IssueHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueHistory
        fields = ['event_type', 'description', 'created_at']
