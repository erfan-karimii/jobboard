from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.permissions import IsAuthenticatedCompany
from account.models import CompanyProfile
from .tasks import company_analytics
# Create your views here.


class CompanyJobAnalytics(APIView):
    permission_classes = [IsAuthenticatedCompany]

    def get(self,request):
        company_profile = get_object_or_404(CompanyProfile,user=request.user)
        company_analytics.delay(company_profile.id)
        return Response({'detail':'your request accept successfully.'},status=status.HTTP_202_ACCEPTED)

