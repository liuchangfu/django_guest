from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from sign.forms import EventForm, GuestFrom


# Create your views here.


def index(request):
    return render(request, 'index.html', locals())


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(username, password)
        if username == '' and password == '':
            msg = '用户名或密码不能为空!'
            return render(request, 'index.html', locals())
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                # 内置登录方法验证
                auth.login(request, user)
                # 将session 信息记录到浏览器
                request.session['username'] = username
                return HttpResponseRedirect('/event_manage/')
            else:
                msg = '用户名或密码错误！！'
                return render(request, 'index.html', locals())
    else:
        return render(request, 'index.html', locals())


@login_required
def event_manage(request):
    events = Event.objects.all()
    username = request.session.get('username', '')
    paginator = Paginator(events, 10)  # 每页显示10条
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'event_manage.html', locals())


@login_required
def event_serach_name(request):
    username = request.session.get('username', '')
    event_serach_name = request.GET.get('name', '')
    print(event_serach_name)
    events = Event.objects.filter(name__contains=event_serach_name)
    print(events)
    if len(events) == 0:
        msg = '你查询的发布会记录不存在。'
        return render(request, 'event_manage.html', locals())
    return render(request, 'event_manage.html', locals())


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')


@login_required
def guest_manage(request):
    guests = Guest.objects.all()
    username = request.session.get('username', '')
    paginator = Paginator(guests, 10)  # 每页显示10条
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', locals())


@login_required
def guest_serach_name(request):
    username = request.session.get('username', '')
    guest_serach_name = request.GET.get('name', '')
    print(guest_serach_name)
    guests = Guest.objects.filter(realname__contains=guest_serach_name)
    print(guests)
    if len(guests) == 0:
        msg = '你查询的嘉宾记录不存在。'
        return render(request, 'guest_manage.html', locals())
    return render(request, 'guest_manage.html', locals())


@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html', locals())


@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest = Guest.objects.filter(event_id=event_id)
    phone = request.POST.get('phone', '')

    result1 = Guest.objects.filter(phone=phone)
    if not result1:
        msg = '手机号码错误，请重新输入。'
        return render(request, 'sign_index.html', locals())

    result2 = Guest.objects.filter(phone=phone, event_id=event_id)
    if not result2:
        msg = '发布会id错误或手机号错误！！！'
        return render(request, 'sign_index.html', locals())

    if event.status == False:
        msg = '发布会状态不正确，无法签到！'
        return render(request, 'sign_index.html', locals())

    result3 = Guest.objects.get(phone=phone, event_id=event_id)
    if result3.sign:
        msg = '该用户已经签到，请勿重复签到！！'
        return render(request, 'sign_index.html', locals())
    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
        msg = '签到成功！！'
        sign_data = 0
        sign_data = str(int(sign_data) + 1)
        return render(request, 'sign_index.html', locals())


@login_required
def add_event(request):
    username = request.session.get('username', '')
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            limit = form.cleaned_data['limit']
            start_time = form.cleaned_data['start_time']
            status = form.cleaned_data['status']
            if status is True:
                status = 1
            else:
                status = 0
            # 保存表单数据
            form = Event.objects.create(name=name, address=address, limit=limit, start_time=start_time, status=status)
            msg = '添加发布会成功！'
            return HttpResponseRedirect('/event_manage/')
    else:
        form = EventForm()
    return render(request, 'add_event.html', locals())


@login_required
def add_guest(request):
    username = request.session.get('username', '')
    if request.method == 'POST':
        form = GuestFrom(request.POST)
        if form.is_valid():
            event = form.cleaned_data['event']
            realname = form.cleaned_data['realname']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            sign = form.cleaned_data['sign']
            if sign is True:
                sign = 1
            else:
                sign = 0
            # 保存表单数据
            form = Guest.objects.create(event=event, realname=realname, phone=phone, email=email, sign=sign)
            return HttpResponseRedirect('/guest_manage/')
    else:
        form = GuestFrom()
    return render(request, 'add_guest.html', locals())
