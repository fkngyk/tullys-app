from django import forms
from .models import Member
from .models import Shift

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('id','name','password')
        labels = {
            'id':'ID',
            'name':'名前',
            'password':'パスワード'
        }
        
class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ('person','day','start_time','finish_time')
        labels = {
            'person':'名前',
            'day':'日にち',
            'start_time':'開始時刻',
            'finish_time':'終了時刻'
        }