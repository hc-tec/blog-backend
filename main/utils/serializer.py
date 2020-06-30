from rest_framework import serializers
from ..models import CarouselImg

class CarouselImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarouselImg
        fields = ['id', 'img']
