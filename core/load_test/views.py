from django.core.mail import send_mail
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework.views import APIView,Response

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
    