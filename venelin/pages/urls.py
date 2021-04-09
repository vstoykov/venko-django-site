from django.urls import path
from django.contrib.flatpages.views import flatpage

urlpatterns = [
    path('<path:url>', flatpage),
    path('', flatpage, kwargs={'url': '/'}, name='home'),
]
