from django.http import HttpResponse
from django.urls import path

def home(request):
    return HttpResponse("Hello from Django inside Docker!")

urlpatterns = [
    path("", home),
]