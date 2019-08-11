from django.shortcuts import render
from sign.models import Event, Guest
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def add_event(request):
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')

    # 判断eid,name,limit,address,status,start_time等字段不能为空
    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'msg': 'parameter error'})

    # 判断id是否存在
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'msg': 'event id already exists'})

    # 判断发布会名称是否存在
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'msg': 'event name is already exists'})

    if status == '':
        status = 1

    # 写入数据库时，判断start_time格式是否正确
    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error.It myst be in YYYY-MM-DD HH:MM:SS format'
        return JsonResponse({'status': 10024, 'msg': error})
    return JsonResponse({'status': 200, 'msg': 'add event success'})


def add_guest(request):
    pass


def get_event_list(request):
    pass


def get_guest_list(request):
    pass


def user_sign(request):
    pass
