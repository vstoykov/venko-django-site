from django.urls import path

from .views import galleries, gallery

app_name = 'gallery'
urlpatterns = [
    path('', galleries, name='index'),
    path('<slug>/', gallery, name='gallery'),
]
