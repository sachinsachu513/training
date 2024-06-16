from django.db import models

# Create your models here.
class School(models.Model):
    name=models.CharField(max_length=15)
    location=models.CharField(max_length=15)
    def __str__(self):
        return self.name

class StudentName(models.Model):
    name=models.CharField(max_length=15)
    age=models.IntegerField()
    gender=models.CharField(max_length=10)
    school=models.ForeignKey(School,on_delete=models.CASCADE)

    def __str__(self):
        return self.name