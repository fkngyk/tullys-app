from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Member(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    password =  models.IntegerField()
    def __str__(self):
        return str(self.name)

class Shift(models.Model):
    person = models.ForeignKey(Member,on_delete=models.CASCADE)
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    start_time = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    finish_time = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(24)])

class Attachment(models.Model):
    files = models.FileField(upload_to = 'files')