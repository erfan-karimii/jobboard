from django.shortcuts import get_object_or_404
from rest_framework import status , serializers
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


class ShowJobs(APIView):

    class ShowJobSerializers(serializers.ModelSerializer):
        url = serializers.HyperlinkedIdentityField(view_name='job:job-detail', read_only=True)
        class Meta:
            model= Job
            fields = ['title','company','province','url']

    def get(self,request):
        jobs=Job.objects.filter(status=True)
        serializer=self.ShowJobSerializers(jobs,many=True,context={'request':request})

        return Response(serializer.data)


class ShowDetailJob(APIView):
    class ShowDetailJobSerializer(serializers.ModelSerializer):
        # url = serializers.HyperlinkedIdentityField(view_name='job-detail', read_only=True)
        class Meta:
            model= Job
            fields ="__all__"

    def get(self,request,pk):
        job = get_object_or_404(Job,id=pk,status=True)
        ser = self.ShowDetailJobSerializer(job)
        return Response(ser.data)