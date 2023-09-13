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
            context = {'result': result,
                       'form': form}
        return render(request,'timop/timop.html', context=context)
    context = {'form': form}
    return render(request, 'timop/timop.html', context=context)


def time_operations(request):
    if request.method == 'POST':
        if request.form.get('time_data_1'):
            data = request.form.get('time_data_1')
            print(data)
            result = TimeKeeper().get_current_time(data)
            return f'current time in {data} time zone: {result}'
        elif request.form.get('time_data_2'):  # format "EST;00:00"
            data = request.form.get('time_data_2').split(';')
            print(data)
            result = TimeKeeper.time_operation_2(data, 'y')
            return result
        elif request.form.get('time_data_3'):  # format "EST;00:00"
            data = request.form.get('time_data_3').split(';')
            print(data)
            result = TimeKeeper.time_operation_2(data, 'n')
            return result

    return render(request, 'timop/time_operations.html')


def about(request):
    return render(request, 'timop/about.html', {'title': 'About'})
