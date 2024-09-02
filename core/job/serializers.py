from rest_framework import serializers
from .models import Job,JobCategory , JobApply,validate_resume_size
from account.models import CompanyProfile
from account.serializers import CustomerProfileSerializers

class CreateJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title','category','province','salary','info','status']



class ShowJobSerializers(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='job:job-detail', read_only=True)
    company = serializers.CharField(source='company.name')
    class Meta:
        model= Job
        fields = ['title','company','province','url']



class ShowDetailJobSerializer(serializers.ModelSerializer):
    class CompanySerializerListJob(serializers.ModelSerializer):
        class Meta:
            model = CompanyProfile
            exclude = ['id','user']

    class CategorySerializerDetailView(serializers.ModelSerializer):
        class Meta:
            model = JobCategory
            fields = "__all__"
    
    company = CompanySerializerListJob()
    category = CategorySerializerDetailView()
    class Meta:
        model= Job
        exclude = ["id","status","created"]


class SendJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApply
        exclude = ['id','status','created','job_seeker']


class SerializerCompanySeeJob(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='job:seeDetailJob', read_only=True)
    class Meta:
        model = Job
        exclude = ["id","status","created","category","company","updated_at"]

class SerializerSeeJobSeeker(serializers.ModelSerializer):
    job_seeker = CustomerProfileSerializers()
    job = serializers.CharField(source='job.title')
    class Meta:
        model = JobApply
        fields = "__all__"