from rest_framework import routers

from universities.views import UniversityViewSet


universities_router = routers.DefaultRouter()
universities_router.register(
    "universities", viewset=UniversityViewSet, basename="universities"
)
