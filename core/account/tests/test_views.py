from django.urls import reverse
from rest_framework.test import APITestCase , APIClient
from account.models import User


class TestClientLoginView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("account:login-view")
        cls.user_1 = User.objects.create_user(email="test1@test.com")
        cls.client = APIClient()
    
    
    def test_right_data(self):
        data = {
            "email" : "test1@test.com"
        }
        
        response = self.client.post(path=self.url,data=data)
        
        
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(response.status_code,202)
        self.assertEqual(response.data,{"Accept request": "please check your email to proceed"})
        

    def test_right_data_none_existing_user(self):
        data = {
            "email" : "test2@test.com"
        }
        
        response = self.client.post(path=self.url,data=data)
        
        
        self.assertEqual(User.objects.count(),2)
        self.assertEqual(response.status_code,202)
        self.assertEqual(response.data,{"Accept request": "please check your email to proceed"})
        
        
    def test_wrong_data(self):
        data = {
            "email" : "test"
        }
        
        response = self.client.post(path=self.url,data=data)
        
        
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.data.get("email")[0],"Enter a valid email address.")
        