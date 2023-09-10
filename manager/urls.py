from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'manager'

urlpatterns = [
    path('', views.home, name='manager-dashboard'),
    path('invitations/', views.invitations_view, name='invitations-view'),
    path('send-invitation/', views.send_invitation, name='send-invitation'),
    path('invitation-success/', TemplateView.as_view(template_name='manager/invitation_success.html'), name='invitation-success'),
    path('invitations/<int:invitation_id>/delete/', views.delete_invitation, name='delete-invitation'),
    
    #Customers list 
    path('invited_customers/', views.InvitedCustomersListView.as_view(), name='invited_customers_list'),

]
