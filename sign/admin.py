from django.contrib import admin
from sign.models import Event, Guest

# Register your models here.


admin.site.register(Event)
admin.site.register(Guest)

admin.site.site_header = '签到管理系统'
admin.site.site_title = '签到管理系统'
