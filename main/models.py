from django.db import models

class CarouselImg(models.Model):

    img = models.CharField(max_length=256)
