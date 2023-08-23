from django.shortcuts import render
from django.http import HttpResponse


def timop(request):
    return HttpResponse('<h1>TIME operations</h1>')
