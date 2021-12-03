from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
import json
from datetime import date

from ..models import Poll, Answer
from .serializers import PollSerializer, QuestionSerializer, OptionSerializer, UserOptionSerializer

class PollListView(generics.ListAPIView):
    today = date.today()
    queryset = Poll.objects.filter(is_active=True,created_at__lte=today,finished_at__gt=today)
    serializer_class = PollSerializer

class PollDetailView(APIView):
    serializer_class = QuestionSerializer
    def get(self, request,pk):
        today = date.today()
        poll = Poll.objects.get(id=pk)
        if poll.created_at > today or poll.finished_at < today:
            raise Poll.DoesNotExist()

        result = PollSerializer(poll).data
        result['questions'] = []
        for question in poll.questions.all():
            questionDict = QuestionSerializer(question).data
            if question.hasChoice:
                questionDict['options'] = UserOptionSerializer(question.options.all(), many=True).data
            result['questions'].append(questionDict)

        return Response(result)

    def post(self,request,pk):
        today = date.today()
        poll = Poll.objects.get(id=pk)
        if poll.created_at > today or poll.finished_at < today:
            raise Poll.DoesNotExist()

        if not 'user_id' in request.data:
            raise Exception('user_id is missing')
        if not type(request.data['user_id']) is int:
            raise Exception('Invalid userId')
        if not 'answers' in request.data:
            raise Exception('answers are missing')
        if not type(request.data['answers']) is dict:
            raise Exception('Invalid answers')

        user_id = request.data['user_id']
        answer_dict = request.data['answers']


        def makeAnswer(question):
            if not str(question.id) in answer_dict:
                raise Exception('Answer to question %d is missing' % question.id)

            answerData = answer_dict[str(question.id)]
            answer = Answer(
                question=question,
                question_type=question.type,
                question_text=question.text,
                user_id=user_id,
                poll=poll)

            invalidAnswerException = Exception('Invalid answer to question %d' % question.id)
            invalidIndexException = Exception('Invalid option index in answer to question %d' % question.id)
            if question.type == 'TEXT':
                if not type(answerData) is str:
                    raise invalidAnswerException
                answer.text_answer = answerData

            if question.type == 'CHOICE':
                if not type(answerData) is int:
                    raise invalidAnswerException
                foundOption = question.options.filter(index=answerData).first()
                if foundOption:
                    answer.text_answer = foundOption.text
                else:
                    raise invalidIndexException

            if question.type == 'MULTIPLE_CHOICE':
                if not type(answerData) is list:
                    raise invalidAnswerException
                optionList = question.options.all()
                resultList = []
                for index in answerData:
                    foundOption = next((o for o in optionList if o.index == index), None)
                    if foundOption:
                        resultList.append(foundOption.text)
                    else:
                        raise invalidIndexException
                answer.answerText = json.dumps(resultList)

            return answer

        answerList = [makeAnswer(question) for question in poll.questions.all()]
        if len(answerList) != poll.questions.count():
            raise Exception('Not enough answers')

        for answer in answerList:
            answer.save()

        return Response('Accepted')

class UserPolls(APIView):
    def get(self, request, id):
        #polls = Answer.poll.filter(user_id=id)
        result = []

        for answer in Answer.objects.filter(user_id=id):
            answer_text = answer.text_answer
            result.append(
                {
                    'question':{
                        'id':answer.question_id,
                        'type':answer.question.type,
                        'text':answer.question.text
                    },
                    'answer':answer_text
                }
            )

        return Response(result)





