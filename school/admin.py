from django.contrib import admin

# Register your models here.
from . models import School,StudentName
admin.site.register(School)
admin.site.register(StudentName)