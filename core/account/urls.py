from django.urls import path
from . import views


app_name = "accounts" 

urlpatterns = [
    path('login/',views.CustomerLoginView.as_view(),name='login-view'),
    # path('companylogin/',views.CompanyLogin.as_view(),name='company-login'),
    path('flog/',views.login_view,name='flog'),
]