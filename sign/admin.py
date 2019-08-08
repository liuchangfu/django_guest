from django.contrib import admin
from sign.models import Event, Guest


# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'start_time']
    list_filter = ['name']
    search_fields = ['status']
    list_display_links = ['name']
    list_per_page = 10

class GuestAdmin(admin.ModelAdmin):
    list_display = ['id', 'realname', 'phone', 'email', 'sign', 'create_time']
    list_filter = ['sign']
    search_fields = ['realname', 'phone']
    list_display_links = ['realname', 'phone']
    list_per_page = 10


admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)

admin.site.site_header = '签到管理系统'
admin.site.site_title = '签到管理系统'
