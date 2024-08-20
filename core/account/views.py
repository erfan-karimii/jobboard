from django.core.mail import send_mail
from django.contrib.auth import login
from django.http import HttpResponse

from rest_framework.parsers import JSONParser
from rest_framework import status , serializers
from rest_framework.views import APIView,Response

from drf_spectacular.utils import extend_schema , OpenApiResponse, OpenApiExample,inline_serializer

from .permissions import IsAuthenticatedCustomer,IsAuthenticatedCompany
from account.serializers import CustomAuthSerializer,CustomerProfileSerializers , CompanyAuthSerializer,CompanyProfileSerializers
from account.models import User,UserProfile,CompanyProfile


class CustomerLoginView(APIView):
    serializer_class = CustomAuthSerializer
    parser_classes = [JSONParser]

    @extend_schema(
        request=CustomAuthSerializer,
        operation_id="login user",
        responses={
            200: OpenApiResponse(
                response=inline_serializer(name='CustomerLoginSerializer',fields={'Accept request':serializers.CharField()}),
                description="A successful response with a message.",
                examples=[
                    OpenApiExample(
                        'default',
                        summary='this is the only expected value',
                        description='if the email send correctly, despite the user is created or not, login url send to user email',
                        value='{"Accept request": "please check your email to proceed"}'
                    ),
                ]
            ),
            400:OpenApiResponse(
                response=CustomAuthSerializer,
                description="A not found response with an error message."
            )
        }
        )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            email = request.data['email']
            admin_email = "admin@admin.com"
            send_mail(
                subject="confirmation email",
                message=f"{serializer.validated_data}",
                from_email=admin_email,
                recipient_list=[email],
                fail_silently=True,
            )
            return Response({"Accept request": "please check your email to proceed"},status=status.HTTP_202_ACCEPTED)

        return Response({"ERROR":"Your Data Is Wrong"},status=status.HTTP_400_BAD_REQUEST)
    

class CustomerProfile(APIView):
    serializer_class = CustomerProfileSerializers
    permission_classes = [IsAuthenticatedCustomer]
    

    def get(self,request):
        # self.serializer_class()
        user=User.objects.get(id=request.user.id)
        profile = UserProfile.objects.get(user=user)
        serializers=self.serializer_class(profile)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def patch(self,request):
        user=User.objects.get(id=request.user.id)
        profile =  UserProfile.objects.filter(user=user).first()
        serializer=self.serializer_class(profile,data=request.data)
        if serializer.is_valid():
            serializer.update(
                instance=profile, validated_data=serializer.validated_data
            )
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CompanyLoginView(APIView):
    serializer_class = CompanyAuthSerializer

    @extend_schema(responses=CompanyAuthSerializer)
    def post(self,request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            email = request.data['email']
            admin_email = "admin@admin.com"
            send_mail(
                subject="Token email",
                message=f"{serializer.validated_data}",
                from_email=admin_email,
                recipient_list=[email],
                fail_silently=True,
            )
            print(serializer.validated_data)
            return Response({"Accept request": "please check your company email to proceed"},status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CompanyProfileView(APIView):
    serializer_class = CompanyProfileSerializers
    permission_classes = [IsAuthenticatedCompany]

    def get(self,request):
        user=User.objects.get(id=request.user.id)
        profile = CompanyProfile.objects.get(user=user)
        serializers=self.serializer_class(profile)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def patch(self,request):
        user = User.objects.get(id=request.user.id)
        profile = CompanyProfile.objects.get(user=user)
        serializers=self.serializer_class(profile,data=request.data,partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.validated_data,status=status.HTTP_200_OK)
        



def login_view(request):
    username = 'b@b.com'
    user = User.objects.get(email=username)
    # logger.warning(user)
    if user is not None:
        login(request,user)
        return HttpResponse('s')
    return HttpResponse('d')