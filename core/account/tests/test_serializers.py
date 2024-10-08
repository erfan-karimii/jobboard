from rest_framework.test import APITestCase
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from account.serializers import CustomAuthSerializer

class TestCustomAuthSerializer(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create_user(email="test1@test.com")
    
    def test_wrong_email(self):
        sample_email = 'test'
        
        serializer = CustomAuthSerializer(data={"email":sample_email})
        
        self.assertEqual(User.objects.count(),1)
        self.assertFalse(serializer.is_valid(raise_exception=False))
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
    
    # def test_right_existing_user_email(self):
    #     sample_email = "test1@test.com"
        
    #     serializer = CustomAuthSerializer(data={"email":sample_email})
        
    #     self.assertEqual(User.objects.count(),1)
    #     self.assertTrue(serializer.is_valid(raise_exception=False))
    #     refresh = RefreshToken.for_user(self.user_1)
    #     print(serializer.validated_data['refresh'])
    #     print(str(refresh))
    #     # self.assertEqual(serializer.validated_data['access'],str(refresh.access_token))
    
    # def test_right_existing_email(self):
    #     sample_email = "test2@test.com"
        
    #     serializer = CustomAuthSerializer(data={"email":sample_email})
        
    #     self.assertTrue(serializer.is_valid(raise_exception=False))
    #     self.assertEqual(User.objects.count(),2)
    #     refresh = RefreshToken.for_user(self.user_1)
    #     self.assertEqual(serializer.validated_data['access'],str(refresh.access_token))
    

   