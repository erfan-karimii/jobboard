import json
from django.urls import reverse
from django.core import mail

from rest_framework.test import APITestCase , APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User,UserProfile , CompanyProfile
from account.serializers import CustomerProfileSerializers


class TestClientLoginView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("account:login-view")
        cls.user_1 = User.objects.create_user(email="test1@gmail.com")
        cls.client = APIClient()
    
    
    def test_right_data(self):
        data = {
            "email" : "test1@gmail.com"
        }
        response = self.client.post(path=self.url,data=data,format="json")
        
        
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(response.status_code,202)
        self.assertEqual(response.data,{"Accept request": "please check your email to proceed"})
        

    def test_right_data_none_existing_user(self):
        data = {
            "email" : "test2@test.com"
        }
        response = self.client.post(path=self.url,data=data,format="json")
        
        
        self.assertEqual(User.objects.count(),2)
        self.assertEqual(response.status_code,202)
        self.assertEqual(response.data,{"Accept request": "please check your email to proceed"})
        
        
    def test_wrong_data(self):
        data = {
            "email" : "test"
        }
        response = self.client.post(path=self.url,data=data,format="json")
        
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,{"ERROR":"Your Data Is Wrong"})


class TestProfileCustomer(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("account:profile")
        cls.client = APIClient()
        
        
        cls.user = User.objects.create_user(email="test1@gmail.com")
        jwt = str(RefreshToken.for_user(cls.user).access_token)
        cls.headers={
            'Content-Type':'application/json',
            'Authorization': f'Bearer {jwt}'
            }


    def test_get_profile_user(self):
        response=self.client.get(path=self.url,headers=self.headers)

        self.assertEqual(response.data,{'fullname': '', 'resume_file': None})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        
    def test_update_profile_by_valid_data(self):
        data = {
            "fullname":"masoud"
        }
        response = self.client.patch(path=self.url,headers=self.headers,data=data,format="json")

        self.assertEqual(response.data,{'fullname': 'masoud', 'resume_file': None})
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


    def test_update_profile_by_unvalid_data(self):
        # TODO :What is Wrong data For Update?
        data = {
            "fullname":True
        }
        response = self.client.patch(path=self.url,headers=self.headers,data=data,format="json")
        
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


class TestCompanyLoginView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("account:company-login")
        cls.client = APIClient()
        
        
        cls.user = User.objects.create_company(email="test1@gmail.com")
        jwt = str(RefreshToken.for_user(cls.user).access_token)
        cls.headers={
            'Content-Type':'application/json',
            'Authorization': f'Bearer {jwt}'
            }
    
    
    def test_right_data(self):
        data = {
            "email" : "test1@gmail.com"
        }
        response = self.client.post(path=self.url,data=data,format="json")
        
        
        self.assertEqual(response.status_code,202)
        self.assertEqual(response.data,{"Accept request": "please check your company email to proceed"})
        self.assertEqual(len(mail.outbox),1)

    
    def test_none_existing_user(self):
        data = {
            "email" : "test2@test.com"
        }
        response = self.client.post(path=self.url,data=data,format="json")
        expected_msg = 'Your Company Email Doesn\'t exist.\nFor more informations , please contact supports.'
        self.assertEqual(response.status_code,400)
        self.assertEqual(expected_msg,response.data['non_field_errors'][0])
        self.assertEqual(len(mail.outbox),0)
    
    
    def test_wrong_data(self):
        data = {
            "email" : "test"
        }
        response = self.client.post(path=self.url,data=data,format="json")
        
        self.assertEqual(response.status_code,400)
        self.assertEqual('Enter a valid email address.',response.data['email'][0])
        self.assertEqual(len(mail.outbox),0)


class TestProfileCustomer(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("account:company-profile")
        cls.client = APIClient()
        
        
        cls.company = User.objects.create_company(email="test1@gmail.com")
        jwt = str(RefreshToken.for_user(cls.company).access_token)
        cls.headers={
            'Content-Type':'application/json',
            'Authorization': f'Bearer {jwt}'
            }


    def test_get_profile_user(self):
        response=self.client.get(path=self.url,headers=self.headers)

        expected_result = {"name" : "" ,"logo" : None ,"info" : "" ,"employee_number" : 0,}
        self.assertEqual(response.data,expected_result)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        
    def test_update_profile_by_valid_data(self):
        data = {
            'name' : 'erfan',
            'info' : 'erfan info',
            'employee_number' : 100,
        }
        response = self.client.patch(path=self.url,headers=self.headers,data=data,format="json")
        self.assertEqual(response.data,data)
        self.assertEqual(response.status_code,200)
        


    def test_update_profile_by_unvalid_data(self):
        data = {
            'test':'test'
        }
        response = self.client.patch(path=self.url,headers=self.headers,data=data,format="json")
        
        self.assertEqual(response.data,{})
        self.assertEqual(response.status_code,200)
        