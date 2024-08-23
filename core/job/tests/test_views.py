import json
from django.urls import reverse
from django.core import mail

from rest_framework.test import APITestCase , APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User
from job.models import Job , JobCategory

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
        self.assertEqual(response.status_code,200)
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
        self.assertEqual(list(json.loads(response.content).keys()),["title","category","province","salary","info","status"])          
    

