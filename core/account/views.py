from django.core.mail import send_mail
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.views import APIView,Response

from drf_spectacular.utils import extend_schema , OpenApiResponse, OpenApiExample,inline_serializer

from account.serializers import CustomAuthSerializer,CompanyAuthSerializer
from account.serializers import CustomAuthSerializer,CompanyAuthSerializer
from account.models import User

from django.contrib.auth import login
from django.http import HttpResponse

class CustomerLoginView(APIView):
    serializer_class = CustomAuthSerializer
    parser_classes = [JSONParser]

    @extend_schema(
        request=CustomAuthSerializer, 
        responses={
            200: OpenApiResponse(
                response=CustomAuthSerializer,
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