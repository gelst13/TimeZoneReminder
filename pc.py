"""
- change Contact model: set zone_name to nullable=True

- clean tzr_utils:
    -- refactor 1st func with offset, 2nd func with zone name
    -- make current existing functions smaller and clearer
    -- delete functionality for CLI interface

- change tzr_utils to work with Olsen tz names Asia/Almaty

+ add user's time zone to profile

- correct how "author's" image is displayed in post_detail.html

- use users's local tz in timop
- change local tz for anonymous user:
because in Django utility cannot grab local time correctly

- display offset correctly as +00:30 or -02:00

ideas:
- add comments to posts from logged-in users
"""