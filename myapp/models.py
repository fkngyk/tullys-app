from django.db import models

# Create your models here.
def add_shift(person,date,time):
        if len(date) != len(time):
            print('エラー：入力されたデータの個数が異なります。')
        else:
            for i in range(len(date)):
                x = [date[i],time[i][0],time[i][1]]
                person.shift.append(x)
        
class Person(models.Model):
    last_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=10)
    shift = []