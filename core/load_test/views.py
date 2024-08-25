from django.core.mail import send_mail
from rest_framework.parsers import JSONParser
import random
from rest_framework import status
from rest_framework.views import APIView,Response
from account.permissions import IsAuthenticatedCustomer
from account.models import User,CompanyProfile
from account.serializers import CompanyAuthSerializer
from drf_spectacular.utils import extend_schema , OpenApiResponse, OpenApiExample,inline_serializer

from .serializers import CustomAuthSerializer


class TestLoadCustomerLoginView(APIView):
    serializer_class = CustomAuthSerializer
    parser_classes = [JSONParser]

    @extend_schema(
        request=CustomAuthSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        # print(request.data)
        if serializer.is_valid():
            email = request.data['email']
            host_name = request.get_host()
            admin_email = "admin@admin.com"
            send_mail(
                subject="confirmation email",
                message=f"{serializer.validated_data}",
                from_email=admin_email,
                recipient_list=[email],
                fail_silently=True,
            )
            return Response(serializer.validated_data,status=status.HTTP_202_ACCEPTED)

        return Response({"ERROR":"Your Data Is Wrong"},status=status.HTTP_400_BAD_REQUEST)

class TestLoadProfileView(APIView):
    serializer_class = CustomAuthSerializer

    def post(self, request, *args, **kwargs):
        id = request.data.get("id")
        user = User.objects.filter(id=id).first()
        if user is None:
            return Response({'access':"notfound"})
        else:
            serializer = CustomAuthSerializer(data={"email":user.email})
                    
            if serializer.is_valid():
                return Response(serializer.validated_data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'access':"notfound"})    
            

class TestLoadCompanyProfile(APIView):
    serializer_class = CustomAuthSerializer

    def post(self, request, *args, **kwargs):
        id =random.randint(1,8229)
        user = CompanyProfile.objects.filter(id=id).first()
        if user is None:
            return Response({'access':"notfound"})
        else:
            serializer = CompanyAuthSerializer(data={"email":user.user.email})
                    
            if serializer.is_valid():
                return Response(serializer.validated_data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'access':"notfound"})
            
from faker import Faker
class MakeCompany(APIView):
    f = Faker()
    def get(self, request, *args, **kwargs):
        for x in range(1,10000):
            r = f"{str(x)}company{str(self.f.email())}"
            User.objects.create_company(email=r)
        return Response("ITS OK")