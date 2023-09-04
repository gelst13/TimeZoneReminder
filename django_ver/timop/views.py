from django.shortcuts import render


def timop(request):
    return render(request, 'timop/timop.html')


def about(request):
    return render(request, 'timop/about.html', {'title': 'About'})
