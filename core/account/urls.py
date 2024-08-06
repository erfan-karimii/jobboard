from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.HelloWorld.as_view(),name='f')
]
