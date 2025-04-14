from django.shortcuts import render
from django.http import HttpRequest

def test_api_home(request: HttpRequest):
    return render(request, 'test_api/home.html')
