from django.urls import path

from .views import highlight

urlpatterns = [
    path('', highlight, name='highlighter'),
]
