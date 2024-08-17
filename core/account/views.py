from django.core.mail import send_mail
from rest_framework.parsers import JSONParser
from .permissions import IsAuthenticatedCustomer
from rest_framework import status , serializers
from rest_framework.views import APIView,Response

from drf_spectacular.utils import extend_schema , OpenApiResponse, OpenApiExample,inline_serializer

from account.serializers import CustomAuthSerializer,CustomerProfileSerializers
from account.models import User,UserProfile

from django.contrib.auth import login
from django.http import HttpResponse

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
        return Response(serializers.data)
    
    def post(self,request):
        user=User.objects.get(id=request.user.id)
        
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            x = UserProfile.objects.filter(user=user).update(fullname=serializer.validated_data['fullname'],resume_file=serializer.validated_data.get('resume_file',None))
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





# class CompanyLogin(APIView):
#     serializer_class = CompanyAuthSerializer

#     @extend_schema(responses=CompanyAuthSerializer)
#     def post(self,request):
#         serializer = self.serializer_class(
#             data=request.data, context={"request": request}
#         )
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         email = serializer.validated_data["email"]
#         token, _ = Token.objects.get_or_create(user=user)
        
#         host_name = request.get_host()
#         admin_email = "admin@admin.com"
#         send_mail(
#             subject="confirmation email",
#             message=f"token:{token}",
#             from_email=admin_email,
#             recipient_list=[email],
#             fail_silently=True,
#         )

#         return Response({"Accept request": "please check your email to proceed"},status=status.HTTP_202_ACCEPTED)



def login_view(request):
    username = 'b@b.com'
    user = User.objects.get(email=username)
    # logger.warning(user)
    if user is not None:
        login(request,user)
        return HttpResponse('s')
    return HttpResponse('d')