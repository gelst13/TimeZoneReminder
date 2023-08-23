###Usage:


###History:
22/08/2023 started django version.. and couldn't do anything
because right after installing Django I got error 
_No Django settings specified
You must either define the environment variable DJANGO_SETTINGS_MODULE 
or call settings.configure() before accessing settings_

23/08/2023
~/PycharmProjects/TimeZ$ python -m django --version
4.2.4
~/PycharmProjects/TimeZ$ django-admin
...
Note that only Django core commands are listed as 
settings are not properly configured 
(error: Requested setting INSTALLED_APPS, but settings are not 
configured. You must either define the environment variable 
DJANGO_SETTINGS_MODULE or call settings.configure() 
before accessing settings.).

~/PycharmProjects/TimeZ$ django-admin startproject django_ver

after that - the same error

~/PycharmProjects/TimeZ$ cd django_ver
~/PycharmProjects/TimeZ/django_ver$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
August 23, 2023 - 09:59:11
Django version 4.2.4, using settings 'django_ver.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

