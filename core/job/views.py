from rest_framework.views import APIView
from .models import Job
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response




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
        