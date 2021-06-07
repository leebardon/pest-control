from rest_framework import routers

from api.pestcontrol.universities.views import UniversityViewSet


universities_router = routers.DefaultRouter()
universities_router.register(
    "universities", viewset=UniversityViewSet, basename="universities"
)
