from django.urls import reverse
from rest_framework.test import APITestCase , APIClient
from account.models import User,UserProfile
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
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
        profile=UserProfile.objects.get(user=self.user)
        serializer = CustomerProfileSerializers(profile)

        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        
    def test_update_profile_by_valid_data(self):
        data = {
            "fullname":"masoud"
        }
        response = self.client.patch(path=self.url,headers=self.headers,data=data,format="json")
        profile=UserProfile.objects.get(user=self.user)
        serializer = CustomerProfileSerializers(profile,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(
            instance=profile,validated_data=serializer.validated_data
        )
        self.assertEqual(response.data,serializer.data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_update_profile_by_unvalid_data(self):
        # TODO :What is Wrong data For Update?
        pass