from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework import status , serializers
from rest_framework.views import APIView , Response
from drf_spectacular.utils import extend_schema 
from rest_framework.pagination import LimitOffsetPagination , PageNumberPagination
from account.permissions import IsAuthenticatedCompany,IsAuthenticatedCustomer
from account.models import CompanyProfile,User,UserProfile
from .models import Job,JobApply
from .serializers import CreateJobSerializer,ShowDetailJobSerializer,ShowJobSerializers,SendJobSerializer,SerializerCompanySeeJob,SerializerSeeJobSeeker
from django.db import IntegrityError
from django.core.paginator import Paginator
from .tasks import job_apply_pdf

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
        cache_key = "JobSerializer"
        data = cache.get(cache_key)
        if data is None:
            jobs=Job.objects.filter(status=True).select_related('company').only('title','province','company__name').order_by('-id')
            paginator = LimitOffsetPagination()
            page = paginator.paginate_queryset(jobs,request)
            
            serializer=self.serializer_class(page,many=True,context={'request':request})
            cache.set(cache_key,serializer.data,timeout=600)
            print('new---------------------------------new')

            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(data,status=status.HTTP_200_OK)

class ShowDetailJob(APIView):
    serializer_class = ShowDetailJobSerializer
    def get(self,request,pk):
        job = get_object_or_404(Job,id=pk,status=True)
        serializer = self.serializer_class(job)
        return Response(serializer.data,status=status.HTTP_200_OK)

class SendJob(APIView):
    permission_classes = [IsAuthenticatedCustomer]
    serializer_class = SendJobSerializer
    def post(self,request):
        user = User.objects.get(id=request.user.id)
        profile = UserProfile.objects.get(user=user)
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            JobApply.objects.create(job_seeker=profile,**serializer.validated_data)
            return Response({"detail":"Your Resume Send Successful"})
        except IntegrityError as e:
            return Response({"error":"you already applied for this job."})
        

class CompanySeeJob(APIView):
    serializer_class = SerializerCompanySeeJob
    permission_classes = [IsAuthenticatedCompany]
    def get(self,request):
        user = User.objects.get(id=request.user.id)
        profile = CompanyProfile.objects.get(user=user)
        job = Job.objects.filter(company=profile)
        response=self.serializer_class(job,many=True,context = {'request':request})
        print(user.email)
        return Response(response.data,status=status.HTTP_200_OK)
    
class CompanyFindSeeker(APIView):
    serializer_class = SerializerSeeJobSeeker
    permission_classes = [IsAuthenticatedCompany]
    def get(self,request,pk):
        user = User.objects.get(id=request.user.id)
        profile = CompanyProfile.objects.get(user=user)
        job_seeker = JobApply.objects.filter(job__id=pk,job__company=profile)
        response = self.serializer_class(job_seeker,many=True)
        return Response(response.data)
    

class CreateJobApplyToPdf(APIView):
    permission_classes = [IsAuthenticatedCompany]
    def get(self,request,job_id):
        company_profile = CompanyProfile.objects.get(user=request.user.id)
        j = job_apply_pdf.delay(comp_id=company_profile.id,job_id=job_id)
        return Response({"msg":"We Will send pdf for your Email Soon..."})
        