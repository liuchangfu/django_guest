from django import forms
from django.forms import ModelForm
from sign.models import Event, Guest
from django.utils import timezone

# 发布会表单
class EventForm(forms.Form):
    name = forms.CharField(max_length=100)
    limit = forms.IntegerField()
    status = forms.BooleanField(required=False)
    address = forms.CharField(max_length=100)
    start_time = forms.DateTimeField(initial=timezone.now())


# 添加嘉宾
class GuestFrom(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['event', 'realname', 'phone', 'email', 'sign']
