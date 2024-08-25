from django.urls import path
from . import views


app_name = "load_test" 

urlpatterns = [
    path('login/',views.TestLoadCustomerLoginView.as_view(),name='loadtest_login'),
    path('p_update/',views.TestLoadProfileView.as_view(),name='loadtest_profile_update'),
    path('company_profile/',views.TestLoadCompanyProfile.as_view(),name='CompanyProfile'),
    path('makecompany/',views.MakeCompany.as_view(),name='comp')
]