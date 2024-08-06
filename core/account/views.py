from django.shortcuts import render
from rest_framework.views import APIView,Response
import random



class HelloWorld(APIView):
    def get(self,request):
        return Response({
            "key":"Hello World"
        })
        
    def post(self,request):
        number=random.randint(100,100000000)
        return Response({
            "Key":number
        })