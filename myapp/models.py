from django.db import models

# Create your models here.
class employee(models.Model):
    emp_no=models.IntegerField()
    emp_name=models.CharField(max_length=10)
    emp_adress=models.CharField(max_length=10)
    def __str__(self):
        return self.emp_name

class Musician(models.Model):
    first_name=models.CharField(max_length=15)
    Last_name=models.CharField(max_length=15)
    instrument=models.CharField(max_length=10)
    def __str__(self):
        return self.first_name

class artist1(models.Model):
    artist=models.ForeignKey(Musician,on_delete=models.CASCADE)
    name=models.CharField(max_length=10)
    num=models.IntegerField()
    def __str__(self):
        return self.name

class teacher(models.Model):
    teacher_name=models.CharField(max_length=15)
    course=models.CharField(max_length=20)
    def __str__(self):
        return self.teacher_name

class staff(models.Model):
    class_name=models.IntegerField()
    staff_name=models.ForeignKey(teacher,on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return str(self.class_name)

class Person(models.Model):
    SHIRT_SIZES={
        "S":'small',
        "M":'medium',
        "l":'large'
    }
    Name=models.CharField(max_length=10)
    size=models.CharField(max_length=1,choices=SHIRT_SIZES)
    def __str__(self):
        return self.Name

class fields(models.Model):
    Auto_field=models.AutoField(primary_key=True)
    Online=models.BooleanField()
    date=models.DateField()
    foreign_key=models.ForeignKey(Person,on_delete=models.CASCADE)
    file=models.FileField()
#
# class publisher(models.Model):
#     name=models.CharField(max_length=10)
#     adress=models.CharField(max_length=20)
#     city=models.CharField(max_length=10)
#     country=models.CharField(max_length=10)
#     class Meta:
#         ordering=["-name"]
#
#     def __str__(self):
#         return self.name()
#
# class author(models.Model):
#     name=models.CharField(max_length=10)
#     email=models.EmailField()

class for_queryset(models.Model):
    emp_id=models.IntegerField()
    name=models.CharField(max_length=10)
    position=models.CharField(max_length=10)
    date=models.DateField()
    def __str__(self):
        return self.name

class author(models.Model):
    name=models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Book(models.Model):
    title=models.CharField(max_length=10)
    author=models.ForeignKey(author,related_name='books',on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class product(models.Model):
    product=models.CharField(max_length=10)
    amount=models.IntegerField()
    def __str__(self):
        return self.product


class q_book(models.Model):
    title=models.CharField(max_length=20)
    author=models.CharField(max_length=20)
    date=models.IntegerField()


    def __str__(self):
        return self.author


class meta_table(models.Model):
    name=models.CharField(max_length=15)
    price=models.IntegerField()
    created_at=models.DateTimeField(auto_now=True)
    class Meta:
        db_table='Meta'
        ordering=['-price']
        verbose_name='Meta'
        verbose_name_plural='Metas'
        unique_together=('name','created_at')

class radio_button(models.Model):
         Choices=(
             ("M","Male"),
             ("f","FEMale"),

         )
         name=models.CharField(max_length=15)
         radio_button=models.CharField(max_length=10,choices=Choices)


class Company(models.Model):
    name = models.CharField(max_length=100)
    num_employees = models.IntegerField()
    num_chairs = models.IntegerField()
    def __str__(self):
        return self.name

from django.db.models import CheckConstraint,Q

class constraints(models.Model):
    company_id=models.IntegerField(unique=True)
    name=models.CharField(max_length=15,primary_key=True)
    age=models.IntegerField()
    num=models.IntegerField(null=True)
    description=models.CharField(max_length=15,blank=True)
    salary=models.IntegerField(default=10000)
    class Meta:
        constraints = [
            CheckConstraint(check=Q(age__gte=18), name='age_gte_18')
        ]

# class poet(models.Model):
#     name= models.CharField(max_length=100)
#     date_of_birth= models.DateField()
#
#     def __str__(self):
#         return self.name
#
# class Biography(models.Model):
#     author= models.OneToOneField(poet, on_delete=models.CASCADE)
#     bio_text= models.TextField()
#     website= models.URLField(blank=True)
#
#     def __str__(self):
#         return f"Biography of {self.author.name}"


class spartan(models.Model):
    player=models.CharField(max_length=10)
    def __str__(self):
        return self.player


class green11(models.Model):
    captain=models.CharField(max_length=15,default="das"
                                                   "tgir")
    senior=models.CharField(max_length=15,default="tannu")
    young_player=models.ForeignKey(spartan,on_delete=models.CASCADE)
    def __str__(self):
        return self.captain
class pcc(models.Model):
    captain=models.CharField(max_length=15,default="sathish")
    youngest_player_team=models.ForeignKey(green11,on_delete=models.CASCADE)

    def __str__(self):
        return self.captain



class queryfuntion(models.Model):
    x=models.DecimalField(max_digits=10,decimal_places=2)
    y=models.DecimalField(max_digits=10,decimal_places=2)


class student(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.FloatField()
    def __str__(self):
        return str(self.student)


class Booke(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Edition(models.Model):
    book = models.ForeignKey(Booke, related_name='editions', on_delete=models.CASCADE)
    pages = models.PositiveIntegerField()
    def __str__(self):
        return str(self.book)


class Donor(models.Model):
    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3)
    amount = models.IntegerField()

    def __str__(self):
        return self.name

class manyto(models.Model):
    many=models.ManyToManyField(Donor)
    accept=models.CharField(max_length=15)
    def __str__(self):
        return str(self.many)


class  organization(models.Model):
    org_name=models.CharField(max_length=15)
    owner_name=models.CharField(max_length=15)
    org_location=models.CharField(max_length=15)

    def __str__(self):
        return self.org_name

class companys(models.Model):
    company_name=models.CharField(max_length=15)
    company_org_name=models.ForeignKey(organization,on_delete=models.CASCADE)
    company_branch=models.CharField(max_length=15)
    company_owner=models.CharField(max_length=15)

    def __str__(self):
        return self.company_name



class employess(models.Model):
    emp_no=models.CharField(max_length=15)
    emp_name=models.CharField(max_length=15)
    emp_adress=models.CharField(max_length=15)
    emp_company_name=models.ForeignKey(companys,on_delete=models.CASCADE)
    emp_salary=models.IntegerField(default=10000)

    def __str__(self):
        return self.emp_name


class function(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    alias = models.CharField(max_length=50, null=True, blank=True)
    goes_by = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name

class great(models.Model):
    name=models.CharField(max_length=15)
    age=models.IntegerField()
    height=models.IntegerField()
    weight=models.IntegerField()
    def __str__(self):
        return self.name


class rank(models.Model):
    student=models.CharField(max_length=15)
    score=models.IntegerField()

    def __str__(self):
        return self.student



class for_model(models.Model):
    model=models.CharField(max_length=15)
    name=models.ForeignKey(great,on_delete=models.PROTECT)
    nothing=models.ForeignKey(rank,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.model

class Post(models.Model):
    title=models.CharField(max_length=15)
    content=models.CharField(max_length=15)
    date_field=models.DateTimeField()
    def __str__(self):
        return self.title


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    email=models.EmailField()
    content=models.TextField()
    created_at=models.DateTimeField()
    def __str__(self):
        return self.email


























