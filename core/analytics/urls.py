from django.urls import path 
from . import views


app_name = "analytics" 


urlpatterns = [
    path('job/',views.CompanyJobAnalytics.as_view(),name=''),
]