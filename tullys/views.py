from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import Member
from .models import Shift
from .models import Attachment
from .forms import MemberForm
from .forms import ShiftForm
from .forms import AttachmentForm
import datetime
import os
from datetime import date
from datetime import datetime
import calendar
from .function import input
from django.http import HttpResponse

# Create your views here.
#現在の時刻を取得
now = datetime.now()

#作成するシフトの年月日を設定
if now.month == 12 and now.day >= 15:
    year = now.year + 1
    month = 1
    day = 1
    h = "前半"
    mode = 0
else:
    year = now.year
    if now.day >= 17:
        month = now.month + 1
        day = 1
        h = "前半"
        mode = 0
    else:
        month = now.month
        day = 16
        h = "後半"
        mode = 1

#作成するシフトの日数を設定
if(now.day <= 17):
    n = calendar.monthrange(year, month)[1] - 15
else:
    n = 15

#ここから下は各ページの関数
def home(request):
    return render(request, 'tullys/home.html')

def member_index(request):
    members = Member.objects.all()
    context = {
        'members': members,
        }
    return render(request, 'tullys/member_index.html', context)

def member_new(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            return redirect(member_detail, member_id=member.id)
    else:
        form = MemberForm()
    return render(request, "tullys/member_new.html", {'form': form})

def member_detail(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    context = {
        'member':member,
        }
    return render(request, 'tullys/member_detail.html', context)

def member_edit(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_detail', member_id=member_id)
    else:
        form = MemberForm(instance=member)
    return render(request, 'tullys/member_edit.html', {'form': form})

def member_delete(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    member.delete()
    return render(request, "tullys/complete.html")
    
def shift_index(request):
    members = Member.objects.all()
    shifts = Shift.objects.all().order_by('person', 'day',)
    days = []
    for i in range(n):
        days.append((i+1) + 15*mode)
        
    data = [[''] * (n+1) for i in range(len(members))]
    cnt = 0
    for member in members:
        data[cnt][0] = member
        cnt += 1
    for shift in shifts:
        cnt = 0
        for member in members:
            if shift.person == member:
                data[cnt][shift.day] = str(shift.start_time) + '-' + str(shift.finish_time)
            else:
                cnt += 1
            
    context ={
        'days': days,
        'data': data,
        'month': month,
        'h': h,
        }
    return render(request, 'tullys/shift_index.html', context)

def member_shift(request, member_id):
    shifts = Shift.objects.filter(person=member_id).order_by('person', 'day',)
    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect(member_shift, member_id=member_id)
    else:
        default_data = {'person':member_id}
        form = ShiftForm(default_data)
    context = {
        'form':form,
        'shifts':shifts,
        'month': month,
        'h': h,
        }
    return render(request, "tullys/member_shift.html", context)

def shift_delete(request, member_id):
    shifts = Shift.objects.filter(person=member_id).order_by('person', 'day',)
    checks = request.POST.getlist('checks')
    counter = 1
    for shift in shifts:
        if str(counter) in checks:
            shift.delete()
        counter += 1
    return render(request, "tullys/complete.html")

def shift_input(request):
    members = Member.objects.all()
    shifts = Shift.objects.all().order_by('person', 'day',)
    data = [[''] * (n+1) for i in range(len(members))]
    cnt = 0
    for member in members:
        data[cnt][0] = member
        cnt += 1
    for shift in shifts:
        cnt = 0
        for member in members:
            if shift.person == member:
                data[cnt][shift.day] = str(shift.start_time) + '-' + str(shift.finish_time)
            else:
                cnt += 1
    wb = input(n, data, year, month, day)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % 'shift.xlsx'

    wb.save(response)

    return response

def upload(request):
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            os.remove('media/files/原本.xlsx')
            form.save()
            return render(request, 'tullys/complete.html')
    else:
        form = AttachmentForm()
    return render(request, 'tullys/upload.html', {'form':form})