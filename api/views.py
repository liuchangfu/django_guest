from django.shortcuts import render
from sign.models import Event, Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time


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
        error = 'start_time format error.It must be in YYYY-MM-DD HH:MM:SS format'
        return JsonResponse({'status': 10024, 'msg': error})
    return JsonResponse({'status': 200, 'msg': 'add event success'})


@csrf_exempt
def add_guest(request):
    eid = request.POST.get('eid', '')
    realname = request.POST.get('realname', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')

    # 判断eid,name,limit,address,status,start_time等字段不能为空
    if eid == '' or realname == '' or phone == '':
        return JsonResponse({'status': 10021, 'msg': 'parameter error'})

    # 判断嘉宾所关联的发布会id是否存在
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'msg': 'event id null'})

    # 判断发布会的状态是否为TRUE
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status': 10023, 'msg': 'event status id not available'})

    # 发布会的最大限制人数
    event_limit = Event.objects.get(id=eid).limit
    # 发布会已签到的人数
    guest_limit = Guest.objects.filter(event_id=eid)

    if len(guest_limit) > event_limit:
        return JsonResponse({'status': 10024, 'msg': 'event number is full'})

    # 发布会开始时间
    event_time = Event.objects.get(id=eid).start_time  # datetime.datetime(2019, 8, 12, 11, 44)
    # 截取发布会的日期，格式为%Y-%m-%d
    e_time = str(event_time).split('.')[0]  # ['2019-08-12 11:44:00']
    # 将格式化时间字符串转化成结构化时间
    timeArray = time.strptime(e_time, '%Y-%m-%d %H:%M:%S')
    # 将一个结构化时间转化为时间戳，并转换int型
    e_time = int(time.mktime(timeArray))

    # 返回当前系统时间戳
    now_time = str(time.time())
    n_time = str(now_time).split('.')[0]  # ['1565589798', '5594625']
    n_time = int(n_time)

    if n_time >= e_time:
        return JsonResponse({'status': 10025, 'msg': 'event has started'})

    try:
        Guest.objects.create(realname=realname, phone=int(phone), event_id=int(eid), email=email, sign=0)
    except ValidationError as e:
        return JsonResponse({'status': 10026, 'msg': 'the event guest phone number repeat'})

    return JsonResponse({'status': 200, 'msg': 'add guest success'})


def get_event_list(request):
    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')

    if eid == '' and name == '':
        return JsonResponse({'status': 10021, 'msg': 'parameter error'})

    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'msg': 'query result is empty.'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'msg': 'success', 'data': event})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        print(results)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
                print(datas)
            return JsonResponse({'status': 200, 'msg': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'msg': 'query result is empty.'})


def get_guest_list(request):
    eid = request.GET.get('eid', '')
    phone = request.GET.get('phone', '')

    if eid == '':
        return JsonResponse({'status': 10021, 'msg': 'eid cannot be empty.'})

    if eid != '' and phone == '':
        datas = []
        results = Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                guest = {}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sing'] = r.sign
                datas.append(guest)
                print(datas)
            return JsonResponse({'status': 200, 'msg': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'msg': 'query is empty.'})

    if eid != '' and phone != '':
        guest = {}
        try:
            result = Guest.objects.get(phone=phone, event_id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 10022, 'msg': 'query result is empty.'})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sing'] = result.sign
            print(guest)
            return JsonResponse({'status': 200, 'msg': 'success', 'data': guest})


def user_sign(request):
    pass
