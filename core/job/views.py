from rest_framework import status
from rest_framework.views import APIView , Response
from drf_spectacular.utils import extend_schema 

from account.permissions import IsAuthenticatedCompany
from account.models import CompanyProfile
from .models import Job
from .serializers import CreateJobSerializer


class CreateJobView(APIView):
    permission_classes = [IsAuthenticatedCompany]
    serializer_class = CreateJobSerializer
    
    @extend_schema(request=CreateJobSerializer)
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_profile = CompanyProfile.objects.get(user=request.user)
        serializer.save(company=company_profile)
        return Response({'detail':'job created successfully'},status=status.HTTP_200_OK)