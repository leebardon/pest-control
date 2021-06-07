from django.contrib import admin

from api.pestcontrol.universities.models import University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass
