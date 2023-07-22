from django.urls import path
from . import views

app_name = 'questionnaires'

urlpatterns = [
    path('', views.QuestionnaireListView.as_view(), name='questionnaire_list'),
    path('<int:pk>/', views.QuestionnaireDetailView.as_view(), name='questionnaire_detail'),
    path('create/', views.QuestionnaireCreateView.as_view(), name='questionnaire_create'),
    path('create/success/', views.create_questionnaire_success, name='questionnaire-create-success'),
    path('interviewers/', views.InterviewerListView.as_view(), name='interviewer_list'),
    path('interviewers/<int:pk>/', views.InterviewerDetailView.as_view(), name='interviewer_detail'),
    # Add more URLs as needed
]
