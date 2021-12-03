from rest_framework import serializers
from rest_framework.serializers import ValidationError
from ..models import Question


def validateQuestionType(value):
    if not value in ['TEXT', 'CHOICE', 'MULTIPLE_CHOICE']:
        raise ValidationError('Invalid question type')


class PollSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    created_at = serializers.DateField()
    finished_at = serializers.DateField()


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    type = serializers.CharField(max_length=30, validators=[validateQuestionType])
    text = serializers.CharField(max_length=300)

class OptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    index = serializers.IntegerField(required=False)
    text = serializers.CharField(max_length=100)

class UserOptionSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    text = serializers.CharField(max_length=100)

