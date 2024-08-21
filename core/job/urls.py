from django.urls import path , include
from . import views


app_name = "job" 

user_urlpatterns = [
    path('',views.ShowJobs.as_view(),name='jobs'),
    path('<int:pk>/',views.ShowDetailJob.as_view(),name='job-detail'),
    # path('profile/',views.CustomerProfile.as_view(),name='profile'),
]

company_urlpatterns = [
    # path('login/',views.CompanyLoginView.as_view(),name='company-login'),
    # path('profile/',views.CompanyProfileView.as_view(),name='company-profile')
]


urlpatterns = [
    path('user/',include(user_urlpatterns)),
    path('company/',include(company_urlpatterns)),
]