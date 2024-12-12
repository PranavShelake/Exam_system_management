from django.urls import path
from .views import ems
app_name = 'ems'
urlpatterns = [
    path('', ems, name='ems'),
]
