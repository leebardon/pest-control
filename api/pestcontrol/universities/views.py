from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from api.pestcontrol.universities.serializers import UniversitySerializer
from api.pestcontrol.universities.models import University


class UniversityViewSet(ModelViewSet):
    serializer_class = UniversitySerializer
    queryset = University.objects.all().order_by("-last_update")
    pagination_class = PageNumberPagination

# ap_view decorator means to treat function as post endpoint
@api_view(http_method_names=["POST"])
def send_uni_email(request) -> Response:
    """
        sends email with request payload
        from: me@gmail.com
        to: me@gmail.com
    """
    send_mail(
        subject=request.data.get('subject'),
        message=request.data.get('message'),
        from_email='sillyemail2000@gmail.com',
        recipent_list=['sillyemail2000@gmail.com'],
        fail_silently=False,
    )
    return Response({"status": "success", "info": "email sent"}, status=200)