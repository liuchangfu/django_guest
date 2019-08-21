from django.contrib import admin
from sign.models import Event, Guest


# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'limit', 'address', 'status', 'start_time']
    list_filter = ['name', 'address']
    search_fields = ['status']
    list_display_links = ['name']
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    readonly_fields = ['name', 'address', 'limit', 'status', 'start_time']


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
