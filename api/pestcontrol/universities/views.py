from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from universities.serializers import UniversitySerializer
from universities.models import University


class UniversityViewSet(ModelViewSet):
    serializer_class = UniversitySerializer
    queryset = University.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination
