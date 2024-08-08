from django.urls import path
from . import views


app_name = "account" 

urlpatterns = [
    path('login/',views.CustomerLoginView.as_view(),name='login-view')
]
