from django.urls import path
from . import views

urlpatterns = [
    path('carousel/', views.CarouselImg.as_view()),
    path('carousel/<int:pk>/', views.CarouselSingleImg.as_view()),
]
