from django.shortcuts import render, redirect
from .utils import TimeKeeper
from .forms import TimopForm1


# def timop(request):
#     return render(request, 'timop/time_operations.html')
def timop(request):
    form = TimopForm1()
    if request.method == 'POST':
        form = TimopForm1(request.POST)
        if request.POST.get('current_time'):
            data = request.POST.get('current_time')
            print(data)
            result = TimeKeeper().get_current_time(data)
            print(result)
            context = {'result1': result,
                       'form': form}
        elif request.POST.get('convert_local_time'):
            data = request.POST.get('convert_local_time').split(';')
            print(data)
            result = TimeKeeper().time_operation_2(data, 'y')
            print(result)
            context = {'result2': result,
                       'form': form}
        elif request.POST.get('convert_other_time'):
            data = request.POST.get('convert_other_time').split(';')
            print(data)
            result = TimeKeeper().time_operation_2(data, 'n')
            print(result)
            context = {'result3': result,
                       'form': form}

        return render(request, 'timop/timop.html', context=context)

    context = {'form': form}
    return render(request, 'timop/timop.html', context=context)


def about(request):
    return render(request, 'timop/about.html', {'title': 'About'})
