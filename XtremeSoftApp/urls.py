from django.urls import path
from .views import *

urlpatterns = [
    path('', go_home, name="home"),

]
