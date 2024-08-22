from rest_framework import serializers
from .models import Job


class CreateJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title','category','province','salary','info','status']
        