from django.urls import path
from .views import (
    QuestionnaireListView,
    QuestionnaireCreateView,
    QuestionnaireDetailView, 
    QuestionnaireUpdateView, 
    QuestionnaireDeleteView,
    QuestionSetCreateView,
    QuestionSetUpdateView,
    QuestionSetDeleteView,
    QuestionCreateView,
    QuestionUpdateView,
    QuestionDeleteView,
                   )

app_name = 'surveys'  # הצהרת שם עם פרק כדי לאפשר ניתובים מפותחים

urlpatterns = [
    path('', QuestionnaireListView.as_view(), name='questionnaire_list'),
    path('questionnaire/new/', QuestionnaireCreateView.as_view(), name='questionnaire_create'),
    path('questionnaire/<int:pk>/', QuestionnaireDetailView.as_view(), name='questionnaire_detail'),
    path('questionnaire/<int:pk>/update/', QuestionnaireUpdateView.as_view(), name='questionnaire_update'),
    path('questionnaire/<int:pk>/delete/', QuestionnaireDeleteView.as_view(), name='questionnaire_delete'),
    path('questionnaire/<int:questionnaire_pk>/questionset/new/', QuestionSetCreateView.as_view(), name='questionset_create'),
    path('questionnaire/<int:questionnaire_pk>/questionset/<int:pk>/update/', QuestionSetUpdateView.as_view(), name='questionset_update'),
    path('questionset/<int:pk>/delete/', QuestionSetDeleteView.as_view(), name='questionset_delete'),
    path('questionset/<int:questionnaire_pk>/question/<int:question_set_pk>/new/', QuestionCreateView.as_view(), name='question_create'),
    path('questionset/<int:questionnaire_pk>/question/<int:question_set_pk>/update/<int:pk>/', QuestionUpdateView.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
]
