from django.urls import path
from .views import (QuestionnaireListView, 
                    QuestionnaireCreateView, 
                    QuestionnaireDetailView, 
                    QuestionnaireUpdateView,
                    QuestionnaireDeleteView)

app_name = 'surveys'

urlpatterns = [
    path('', QuestionnaireListView.as_view(), name='questionnaire_list'),
    path('create/', QuestionnaireCreateView.as_view(), name='questionnaire_create'),
    path('<int:pk>/', QuestionnaireDetailView.as_view(), name='questionnaire_detail'),
    path('<int:pk>/update/', QuestionnaireUpdateView.as_view(), name='questionnaire_update'),
    path('<int:pk>/delete/', QuestionnaireDeleteView.as_view(), name='questionnaire_delete'),
]