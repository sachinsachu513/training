from django.db import models

# Create your models here.
class register(models.Model):
    user=models.CharField(max_length=15)
    email=models.EmailField()
    password=models.CharField(max_length=10)

    def __str__(self):
        return self.user


class combine(models.Model):
    f_name=models.CharField(max_length=15)
    l_name=models.CharField(max_length=20)
    email_id=models.EmailField()
    password=models.CharField(max_length=12)
    created_at=models.DateTimeField(auto_now=True)


    class Meta:
        ordering=['created_at']

    def __str__(self):
        return str(self.created_at)

class user(models.Model):
    name=models.CharField(max_length=10)
    email=models.EmailField()
    def __str__(self):
        return str(self.name)


class profile(models.Model):
    account_name=models.CharField(max_length=10)
    user=models.ManyToManyField(user)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.account_name)


class snippet(models.Model):
    username=models.CharField(max_length=10)
    mail=models.EmailField()
    password=models.CharField(max_length=10)

    def __str__(self):
        return self.username

class miscellance(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    destinantion=models.CharField(max_length=10)
    joined=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.joined)


class Hiddenfield(models.Model):
    name=models.CharField(max_length=100)
    hidden=models.CharField(max_length=100)
    def __str__(self):
        return self.name



class user_new(models.Model):
    user_name=models.CharField(max_length=20)
    age=models.IntegerField()
    email=models.EmailField(default=None)
    date_joined=models.DateField()

    def __str__(self):
        return self.user_name



class schoolname(models.Model):
    school_name=models.CharField(max_length=20)
    school_location=models.CharField(max_length=20)
    def __str__(self):
        return self.school_name

class studentdetails(models.Model):
    name=models.CharField(max_length=15)
    age=models.IntegerField()
    student_school=models.ForeignKey(schoolname,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
















































