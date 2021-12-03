from django.contrib import admin
from django.urls import path,include

from .admin_views import AdminPollListView,AdminPollDetailView,AdminCreatePollView,AdminQuestionCreateView,AdminQuestionDetailView
from .user_views import PollListView,PollDetailView,UserPolls

urlpatterns = [
    path('polls/',PollListView.as_view()),
    path('polls/<int:pk>',PollDetailView.as_view()),
    path('user_polls/<int:id>',UserPolls.as_view()),
    path('admin/',include([
        path('polls', AdminPollListView.as_view()),
        path('polls/<int:pk>', AdminPollDetailView.as_view()),
        path('polls/create', AdminCreatePollView.as_view()),
        path('polls/<int:pk>/questions',AdminQuestionCreateView.as_view()),
        path('polls/<int:p_pk>/questions/<int:pk>',AdminQuestionDetailView.as_view())
    ]))
]