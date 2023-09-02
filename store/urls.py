from django.urls import path
from .views import (
    StoreView,
    FirstImpressionView,
    TaskOnePart1View,
    TaskOnePart2View,
    )


app_name = 'store'

urlpatterns = [
    # Store pages
    path('', StoreView.as_view(), name='store-dashboard'),
    
    # Static Tasks Pages
    path('01', FirstImpressionView.as_view(), name='first-impression'),
    path('01_form', TaskOnePart1View.as_view(), name='01_form'),
<<<<<<< HEAD
    path('01_form_part_2', TaskOnePart2View.as_view(), name='01_form_part_2'),
=======
    path('01_part_2', TaskOnePart2View.as_view(), name='01_form_part_2'),
>>>>>>> 4ab0501c689aecb09005f96b7d8351333efc3a90


]
