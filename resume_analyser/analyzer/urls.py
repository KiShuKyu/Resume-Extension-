from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('', views.home, name='home'),
    path('analyze/', views.analyze_resume, name='analyze'),
    # path('upload/', views.upload_resume, name='upload_resume'),
]
