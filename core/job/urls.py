from django.urls import path , include
from . import views


app_name = "job" 

user_urlpatterns = [
    path('',views.ShowJobs.as_view(),name='jobs'),
    path('<int:pk>/',views.ShowDetailJob.as_view(),name='job-detail'),
    # path('profile/',views.CustomerProfile.as_view(),name='profile'),
    path('send_job/',views.SendJob.as_view(),name='sendjob'),
]

company_urlpatterns = [
    path('job/',views.CreateJobView.as_view(),name='company-create-job'),
    path('job/<int:id>/',views.CompanyJobDetail.as_view(),name='company-detail-job'),
    path('seejob/',views.CompanySeeJob.as_view(),name='seejob'),
    path('seejob/<int:pk>/',views.CompanyFindSeeker.as_view(),name='seeDetailJob'),
]


urlpatterns = [
    path('user/',include(user_urlpatterns)),
    path('company/',include(company_urlpatterns)),
]