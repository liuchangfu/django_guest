from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest


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
                msg = '登录成功！！'
                return render(request, 'event_manage.html', locals())
            else:
                msg = '用户名或密码错误！！'
                return render(request, 'index.html', locals())
    else:
        return render(request, 'index.html', locals())


@login_required
def event_manage(request):
    events = Event.objects.all()
    username = request.session.get('username', '')
    return render(request, 'event_manage.html', locals())
