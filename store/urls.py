from django.urls import path
from .views import (
    StoreView,
    FirstImpressionView
    )


app_name = 'store'

urlpatterns = [
    # Store pages
    path('', StoreView.as_view(), name='store-dashboard'),
    
    # Static Tasks Pages
    path('01', FirstImpressionView.as_view(), name='first-impression'),
    

]
