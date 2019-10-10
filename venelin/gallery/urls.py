from django.urls import path

from .views import galleries, gallery, galleries_json, gallery_json

app_name = 'gallery'
urlpatterns = [
    path('', galleries, name='index'),
    path('index.json', galleries_json, name='index.json'),
    path('<slug>/', gallery, name='gallery'),
    path('<slug>.json', gallery_json, name='gallery.json'),
]
