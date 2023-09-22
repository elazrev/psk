from django.urls import path
from .views import (QuestionnaireListView, 
                    QuestionnaireCreateView, 
                    QuestionnaireDetailView, 
                    QuestionnaireUpdateView,
                    QuestionnaireDeleteView,
                    ObjListView,
                    QuestionCreateView,
                    QuestionUpdateView,
                    ObjDeleteView, 
                    DividerCreateView,
                    TitleCreateView, 
                    ExplanationCreateView,
                    HintCreateView,
                    AnswerCreateView,
                    FullTaskListView,
                    FullTaskDetailView,
                    FullTaskCreateView,
                    FullTaskUpdateView,
                    FullAnswerCreateView,
                    FullAnswerUpdateView)  # Add the AnswerCreateView here

app_name = 'surveys'

urlpatterns = [
    path('', QuestionnaireListView.as_view(), name='questionnaire_list'),
    path('create/', QuestionnaireCreateView.as_view(), name='questionnaire_create'),
    path('<int:pk>/', QuestionnaireDetailView.as_view(), name='questionnaire_detail'),
    path('<int:pk>/update/', QuestionnaireUpdateView.as_view(), name='questionnaire_update'),
    path('<int:pk>/delete/', QuestionnaireDeleteView.as_view(), name='questionnaire_delete'),
    path('<int:questionnaire_id>/content/', ObjListView.as_view(), name='obj_list'),
    path('<int:questionnaire_id>/new_question/', QuestionCreateView.as_view(), name='new_question'),
    path('<int:questionnaire_id>/update/<int:pk>/', QuestionUpdateView.as_view(), name='question_update'),
    path('<int:questionnaire_id>/delete/<int:pk>/', ObjDeleteView.as_view(), name='object_delete'),
    path('<int:questionnaire_id>/new_divider/', DividerCreateView.as_view(), name='new_divider'),
    path('<int:questionnaire_id>/new_title/', TitleCreateView.as_view(), name='new_title'),
    path('<int:questionnaire_id>/new_explanation/', ExplanationCreateView.as_view(), name='new_explanation'),
    path('<int:questionnaire_id>/new_hint/', HintCreateView.as_view(), name='new_hint'),
    path('<int:questionnaire_id>/answer/', AnswerCreateView.as_view(), name='answer_create'),  # Add this line for the AnswerCreateView
    
    # New structure:

    path('fulltask/', FullTaskListView.as_view(), name='task_list'),
    path('fulltask/<int:pk>/', FullTaskDetailView.as_view(), name='task_detail'),
    path('fulltask/create/', FullTaskCreateView.as_view(), name='task_create'),
    path('fulltask/update/<int:pk>/', FullTaskUpdateView.as_view(), name='task_update'),
    path('fullanswer/create/', FullAnswerCreateView.as_view(), name='fullanswer_create'),
    path('fullanswer/update/<int:pk>/', FullAnswerUpdateView.as_view(), name='fullanswer_update'),
]

    

