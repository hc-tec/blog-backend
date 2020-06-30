from rest_framework.views import APIView
from rest_framework.viewsets import generics
from . import models
from .utils import serializer

class CarouselImg(generics.ListAPIView,
                  generics.CreateAPIView):

    queryset = models.CarouselImg.objects.all()
    serializer_class = serializer.CarouselImgSerializer

class CarouselSingleImg(generics.UpdateAPIView,
                        generics.DestroyAPIView):

    queryset = models.CarouselImg.objects.all()
    serializer_class = serializer.CarouselImgSerializer
