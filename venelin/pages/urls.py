from django.urls import path

from .views import flatpage

urlpatterns = [
    path('<path:url>', flatpage),
    path('', flatpage, kwargs={'url': '/'}, name='home'),
]
