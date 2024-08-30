from django.shortcuts import get_object_or_404
from rest_framework import status , serializers
from rest_framework.views import APIView , Response
from drf_spectacular.utils import extend_schema 
from rest_framework.pagination import PageNumberPagination
from account.permissions import IsAuthenticatedCompany
from account.models import CompanyProfile
from .models import Job
from .serializers import CreateJobSerializer,ShowDetailJobSerializer,ShowJobSerializers


class CreateJobView(APIView):
    permission_classes = [IsAuthenticatedCompany]
    serializer_class = CreateJobSerializer
    
    @extend_schema(request=CreateJobSerializer)
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_profile = CompanyProfile.objects.get(user=request.user)
        serializer.save(company=company_profile)
        return Response({'detail':'job created successfully'},status=status.HTTP_201_CREATED)


class CompanyJobDetail(APIView):
    permission_classes = [IsAuthenticatedCompany]
    serializer_class = CreateJobSerializer

    def get(self,request,id):
        job = get_object_or_404(Job,id=id,company=request.user.companyprofile)
        serializer = self.serializer_class(job)
        return Response(serializer.data,status=status.HTTP_200_OK)        
    
    def patch(self,request,id):
        job = get_object_or_404(Job,id=id,company=request.user.companyprofile)
        serializer = self.serializer_class(job,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(job,serializer.validated_data)
        return Response({'detail':'job updated successfully'},status=status.HTTP_200_OK)
          

class ShowJobs(APIView):
    serializer_class = ShowJobSerializers

    def get(self,request):
        jobs=Job.objects.filter(status=True)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(jobs,request)
        serializer=self.serializer_class(page,many=True,context={'request':request})

        return Response(serializer.data,status=status.HTTP_200_OK)


class ShowDetailJob(APIView):
    serializer_class = ShowDetailJobSerializer
    def get(self,request,pk):
        job = get_object_or_404(Job,id=pk,status=True)
        serializer = self.serializer_class(job)
        return Response(serializer.data,status=status.HTTP_200_OK)

