import json
from django.urls import reverse
from django.core import mail
from rest_framework.test import APITestCase , APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from model_bakery import baker
from account.models import User , CompanyProfile
from job.models import Job , JobCategory
from rest_framework import status




class TestCreateJobView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("job:company-create-job")
        JobCategory.objects.create(name='test')
        cls.user_1 = User.objects.create_company(email="test1@gmail.com")
        cls.client = APIClient()
        jwt = str(RefreshToken.for_user(cls.user_1).access_token)
        cls.headers={
            'Content-Type':'application/json',
            'Authorization': f'Bearer {jwt}'
            }
    
    
    def test_right_data(self):
        data = {
            "title": "test",
            "category": 1,
            "province": Job.PROVINCE_CHOICES[0][0],
            "salary": 1,
            "info": "test",
            "status": False
        }
        
        response = self.client.post(self.url,data=data,headers=self.headers,format='json')        
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data,{'detail':'job created successfully'})          
    
        
    def test_wrong_data(self):
        data = {
            "title": True,
            "category": 2,
            "province": 'test',
            "salary": 'test',
            "info": True,
            "status": 'test'
        }
        
        response = self.client.post(self.url,data=data,headers=self.headers,format='json')        
        self.assertEqual(response.status_code,400)
        # self.assertEqual(list(json.loads(response.content).keys()),["title","category","province","salary","info","status"])          
        
class ShowJobsTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('job:jobs')
        cls.client = APIClient()
        user = User.objects.create_company(email='comp@gmail.com')
        cls.company_prof = CompanyProfile.objects.get(user=user)
        cat = JobCategory.objects.create(name='developer')

        cls.job1=Job.objects.create(company=cls.company_prof,title='Software Engineer', info='Develop software',province="YZ",salary=12,category=cat, status=True)
        cls.job2=Job.objects.create(company=cls.company_prof,title='Data Scientist', info='Analyze data',province="YZ",category=cat, salary=12,status=True)
        cls.job3=Job.objects.create(company=cls.company_prof,title='System Administrator', info='Manage systems',province="YZ",category=cat,salary=12, status=False)

    def test_get_jobs(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
        self.assertEqual(response.data[0]['title'], self.job1.title)


class DetailJobsTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        user = User.objects.create_company(email='comp@gmail.com')
        cls.company_prof = CompanyProfile.objects.get(user=user)
        cat = JobCategory.objects.create(name='developer')

        cls.job1=Job.objects.create(company=cls.company_prof,title='Software Engineer', info='Develop software',province="YZ",salary=12,category=cat, status=True)
        cls.job2=Job.objects.create(company=cls.company_prof,title='Data Scientist', info='Analyze data',province="YZ",category=cat, salary=12,status=True)
        cls.job3=Job.objects.create(company=cls.company_prof,title='System Administrator', info='Manage systems',province="YZ",category=cat,salary=12, status=False)

    def test_get_jobs(self):
        url = reverse('job:job-detail',args=[self.job1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['info'],self.job1.info)
        self.assertNotEqual(response.data['info'],self.job2.info)
