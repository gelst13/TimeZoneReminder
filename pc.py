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

- display offset correctly as +00:30 or -02:30
- or save offset correctly as string

ideas:
- add comments to posts from logged-in users
"""
import re


o = '-02'
# tz_ = datetime.timezone(datetime.timedelta(hours=float(tz_data)))
# 'in format '+hh' of '-hhmm'
if len(o) == 5:
    hours, minutes = o[:3], o[3:]
else:
    hours = o
    minutes = '00'
print(hours, minutes)

