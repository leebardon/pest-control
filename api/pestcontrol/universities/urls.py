from rest_framework import routers

from .views import UniversityViewSet


universities_router = routers.DefaultRouter()
universities_router.register(
    "universities", viewset=UniversityViewSet, basename="universities"
)
