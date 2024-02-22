from django.shortcuts import render
from django.http.response import HttpResponse
from datetime import datetime
# Create your views here.
def index_template(request):
    myapp_data = {
    'app': 'Django',
    'num': range(10),
    'is_weekday': True,
    'now_date': datetime.now()
    }
    return render(request, 'index.html', myapp_data)