from django.contrib import admin

from universities.models import University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass
