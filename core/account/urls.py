from django.urls import path , include
from . import views


app_name = "account" 

user_urlpatterns = [
    path('login/',views.CustomerLoginView.as_view(),name='login-view'),
    path('flog/',views.login_view,name='flog'),
    path('profile/',views.CustomerProfile.as_view(),name='profile'),
]

company_urlpatterns = [
    path('login/',views.CompanyLoginView.as_view(),name='company-login'),
]


urlpatterns = [
    path('user/',include(user_urlpatterns)),
    path('company/',include(company_urlpatterns)),
]