from django.urls import path
from . import views


app_name = "load_test" 

urlpatterns = [
    path('login/',views.TestLoadCustomerLoginView.as_view(),name='loadtest_login'),
]