"""
- write tests
- create correct requirements
- build project(documentation, deployment, etc.)

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

+ TypeError at /timop/
'NoneType' object is not subscriptable for logged in user with empty offset field

ideas:
- add comments to posts from logged-in users
"""
# in format "+hh" or "-hhmm" (e.g."-01" or "+0230")
