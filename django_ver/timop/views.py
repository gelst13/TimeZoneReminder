from django.shortcuts import render, redirect
from .utils import TimeKeeper
from .forms import TimopForm1, TimopForm2
import requests


def timez(request):
    if request.user.is_authenticated:
        # return redirect('timop-about')
        return redirect('timop-timop')
    else:
        print(request.user.is_authenticated)
        form = TimopForm2()
        context = {'form': form}
        if request.method == 'POST':
            request.session['local_offset'] = request.POST.get('local_offset')
            print(request.session['local_offset'])
            return redirect('timop-timop')
        return render(request, 'timop/timez.html', context)


def timop(request):
    if request.user.is_authenticated:
        local_offset = request.user.profile.offset
        print(f'{request.user.username}` offset {local_offset}')
    else:
        local_offset = request.session['local_offset']
        print(f"AnonymousUser, your offset {local_offset}")
    form = TimopForm1()
    context = {'form': form,
               'local_offset': local_offset}

    if request.method == 'POST':
        form = TimopForm1(request.POST)
        if request.POST.get('current_time'):
            data = request.POST.get('current_time')
            result = TimeKeeper.time_operation_1(data)
            context = {'result0': result,
                       'form': form,
                       'local_offset': local_offset}
        elif request.POST.get('calculate_time'):
            data = request.POST.get('calculate_time').split(':')
            result = TimeKeeper.time_operation_0(data, local_offset)
            context = {'result1': result,
                       'form': form,
                       'local_offset': local_offset}
        elif request.POST.get('convert_local_time'):
            # time_operation_2a(time_, tz_from, tz_to, from_local)
            time, tz_to = request.POST.get('convert_local_time').split(';')
            result = TimeKeeper.time_operation_2a(time, local_offset, tz_to, 'y')
            context = {'result2': result,
                       'form': form,
                       'local_offset': local_offset}
        elif request.POST.get('convert_other_time'):
            time, tz_from = request.POST.get('convert_other_time').split(';')
            result = TimeKeeper.time_operation_2a(time, tz_from, local_offset, 'n')
            print(result)
            context = {'result3': result,
                       'form': form,
                       'local_offset': local_offset}

        return render(request, 'timop/timop.html', context=context)

    return render(request, 'timop/timop.html', context=context)


def about(request):
    return render(request, 'timop/about.html', {'title': 'About'})
