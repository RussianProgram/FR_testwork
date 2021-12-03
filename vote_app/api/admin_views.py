from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.exceptions import ParseError
from rest_framework import status

from django.http import Http404
from datetime import date

from ..models import Poll, Question, Option, questionTypeValidator
from .serializers import PollSerializer, QuestionSerializer, OptionSerializer, UserOptionSerializer



class AdminPollMixin(APIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

class AdminQuestionMixin(APIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]



class AdminPollListView(AdminPollMixin,generics.ListAPIView):
    pass

class AdminPollDetailView(AdminPollMixin, generics.UpdateAPIView,generics.DestroyAPIView):
    def get(self, request, pk):
        try:
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

        except Poll.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.name = request.data['name']
        instance.description = request.data['description']
        #instance.created_at = request.data['created_at']
        instance.finished_at = request.data['finished_at']
        instance.save()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class AdminCreatePollView(AdminPollMixin):
    def post(self,request,*args,**kwargs):
        poll_serializer = PollSerializer(data=request.data)
        data = {}
        if poll_serializer.is_valid():
            poll_serializer.save()
            data['response'] = True

            return Response(data,status.HTTP_200_OK)

        else:
            data = poll_serializer.errors
            return Response(data)

class AdminQuestionDetailView(AdminQuestionMixin,generics.UpdateAPIView,generics.DestroyAPIView):
    def get(self,request,p_pk,pk):
        question = Question.objects.get(id=pk)
        result = QuestionSerializer(question).data
        if question.hasChoice:
            result['options'] = OptionSerializer(question.options.all(),many=True)
        return Response(result)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.text = request.data['text']
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)




class AdminQuestionCreateView(AdminQuestionMixin, generics.CreateAPIView):
    def post(self, request,pk):
        poll = Poll.objects.get(id=pk)
        qs = QuestionSerializer(data=request.data)
        qs.is_valid(raise_exception=True)
        pd = dict(qs.validated_data)
        pd['poll'] = poll
        newQuestion = Question(**pd)
        newQuestion.save()







