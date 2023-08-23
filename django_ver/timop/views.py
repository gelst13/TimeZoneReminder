from django.shortcuts import render


def timop(request):
    return render(request, 'timop/timop.html')
