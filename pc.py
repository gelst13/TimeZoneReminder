"""
+ change Contact model: set zone_name to nullable=True

- clean tzr_utils:
    -- make current existing functions smaller and clearer
    -- delete functionality for CLI interface

+ change tzr_utils to work with Olsen tz names Asia/Almaty

+ add user's time zone to profile

+ correct how "author's" image is displayed in post_detail.html

+ use users's local tz in timop
+ change local tz for anonymous user:
because in Django utility cannot grab local time correctly

x display offset correctly as +00:30 or -02:30
+ or save offset correctly as string

- after register -> login -> profile
now after login -> timop
register -> blog

+ KeyError at /timop/
'local_offset' for anonimoususer without session from timez

+ show user's contacts only

- TypeError at /timop/
'NoneType' object is not subscriptable for logged in user with empty offset field

ideas:
- add comments to posts from logged-in users
"""


o = '-02'
# tz_ = datetime.timezone(datetime.timedelta(hours=float(tz_data)))
# 'in format '+hh' of '-hhmm' (e.g. +02 or -0230)
if len(o) == 5:
    hours, minutes = o[:3], o[3:]
else:
    hours = o
    minutes = '00'
# print(hours, minutes)

# in format "+hh" or "-hhmm" (e.g."-01" or "+0230")
