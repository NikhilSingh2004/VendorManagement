from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def HomePage(request : HttpRequest) -> HttpResponse:
    return HttpResponse("This is The Home Page")