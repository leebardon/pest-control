from rest_framework import serializers
from universities.models import University


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ("id", "name", "status", "application_link", "last_update", "notes")
