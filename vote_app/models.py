from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User


def questionTypeValidator(value):
    if not value in ['TEXT', 'CHOICE', 'MULTIPLE_CHOICE']:
        raise ValidationError('Invalid question type')

CHOICES = ['CHOICE','MULTIPLE_CHOICE']

class Poll(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateField()
    finished_at = models.DateField()
    is_active = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'

class Question(models.Model):
    poll = models.ForeignKey(Poll,
                             on_delete=models.CASCADE,
                             related_name='questions')
    text = models.CharField(max_length=150)
    type = models.CharField(max_length=20, validators=[questionTypeValidator])

    @property
    def hasChoice(self):
        return self.type in CHOICES

    def __str__(self):
        return f'{self.poll} {self.text}'


class Option(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='options')
    option_id = models.PositiveIntegerField()
    text = models.CharField(max_length=100)



class Answer(models.Model):
    user_id = models.IntegerField(db_index=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, validators=[questionTypeValidator])
    question_text = models.CharField(max_length=150)
    text_answer = models.CharField(max_length=150)








