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
                question_data = QuestionSerializer(question).data

                if question.hasChoice:
                    question_data['options'] = UserOptionSerializer(question.options.all(), many=True).data
                result['questions'].append(question_data)

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

    def destroy(self, request, *args, **kwargs):
        return Response('Poll deleted')

class AdminCreatePollView(AdminPollMixin, generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        poll_serializer = PollSerializer(data=request.data)
        poll_serializer.is_valid(raise_exception=True)
        poll_data = poll_serializer.validated_data
        new_poll = Poll(**poll_data)
        new_poll.save()
        return Response('Poll Created')



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

    def destroy(self, request, *args, **kwargs):
        return Response('Question deleted')




class AdminQuestionCreateView(AdminQuestionMixin, generics.CreateAPIView):
    def create(self, request,pk):
        poll = Poll.objects.get(id=pk)
        qs = QuestionSerializer(data=request.data)
        qs.is_valid(raise_exception=True)
        pd = dict(qs.validated_data)
        pd['poll'] = poll
        new_question = Question(**pd)

        require_choices = new_question.hasChoice
        new_choices_list = []
        if require_choices:
            if not 'choices' in request.data:
                raise Exception('choices are missing')
            if type(request.data['choices']) != list or len(request.data['choices']) < 2:
                raise Exception('Invalid choices')

            index = 1
            for option_text in request.data['choices']:
                new_choices_list.append(Option(
                    text=option_text,
                    index=index
                ))
                index += 1

        new_question.save()
        if require_choices:
            for new_choice in new_choices_list:
                new_choice.question = new_choice
                new_choice.save()

        result = QuestionSerializer(new_question).data
        if require_choices:
            result['choices'] = [OptionSerializer(choice).data for choice in new_choices_list]

        return Response(result)






