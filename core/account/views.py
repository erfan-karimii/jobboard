from django.core.mail import send_mail
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework.views import APIView,Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema

from account.serializers import CustomAuthSerializer

class CustomerLoginView(ObtainAuthToken):
    serializer_class = CustomAuthSerializer
    parser_classes = [JSONParser]

    @extend_schema(responses=CustomAuthSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        email = serializer.validated_data["email"]
        token, _ = Token.objects.get_or_create(user=user)
        
        host_name = request.get_host()
        admin_email = "admin@admin.com"
        send_mail(
            subject="confirmation email",
            message=f"http://{host_name}/confirmation/{email}/{token}/",
            from_email=admin_email,
            recipient_list=[email],
            fail_silently=True,
        )

        return Response({"Accept request": "please check your email to proceed"},status=status.HTTP_202_ACCEPTED)