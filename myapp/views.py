import io

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .models import employee
from .forms import myform, iris, views_form

import csv


# Create your views here.
def getprice(request):
    return render(request, 'get_price.html')


def totalprice(request):
    lap = int(request.GET["laptop"])
    mouse = int(request.GET["mouse"])
    hard = int(request.GET["hard"])
    total = lap + mouse + hard
    return render(request, "result.html", context={"total": total})


def add_employ(request):
    if request.method == 'POST':
        if request.POST.get('emp_no') and request.POST.get('emp_name') and request.POST.get('emp_adress'):
            emp = employee()
            emp.emp_no = request.POST.get('emp_no')
            emp.emp_name = request.POST.get('emp_name')
            emp.emp_adress = request.POST.get('emp_adress')
            emp.save()
            return HttpResponse(""" added sucessfully <a href='/view'>clickhere<h1>     """)
    else:
        form = myform()
        return render(request, "employ/add_employ.html", context={"form": form})


def get_data(request):
    emp1 = employee.objects.all()
    return render(request, "employ/get_employ.html", context={'emp1': emp1})


def delee(request, id):
    emp2 = employee.objects.get(id=id)
    emp2.delete()
    return redirect('/view')


def update(request, id):
    emp = employee.objects.get(id=id)
    if request.method == 'POST':
        form = myform(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            return HttpResponse('''<h1> updated! <a href='/view'>clickhere<h1>''')
    return render(request, 'employ/update.html', context={'emp': emp})


def choice_form(request):
    form1 = iris()
    if request.method == 'POST':
        form = iris(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(" your answer was recorded click here to view ")
    else:
        return render(request, "choice/pers.html", context={'form': form1})


from django.http import HttpResponse, HttpResponseNotFound
import datetime


def curent_time(request):
    now = datetime.datetime.now()
    html = "<html><body>  the current date is %s <body></html>" % now
    return HttpResponse(html)


def status_code(request):
    return HttpResponse(status=200)
    # return HttpResponseNotFound("<h1>Page not found</h1>")


from django.core.exceptions import PermissionDenied, MultipleObjectsReturned, ViewDoesNotExist


def check(request):
    form = myform()
    if request.method == 'POST':
        if request.POST.get('username'):
            emp = employee()

            username = request.POST.get('username').lower()
            user = employee.objects.filter(emp_name=username).first()
            if user is not None:
                return HttpResponse("user in database", status=200)
            else:
                raise PermissionDenied
    else:
        form = views_form()
        return render(request, "search.html", context={"form": form})


from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import employee


class employes(ListView):
    model = employee
    context_object_name = 'emp1'
    template_name = 'employ/get_employ.html'


class create_employ(CreateView):
    model = employee
    fields = ['emp_no', 'emp_name', 'emp_adress']
    success_url = reverse_lazy('main')
    template_name = 'employ/add_employ.html'


class employ_update(UpdateView):
    model = employee
    context_object_name = 'emp'
    template_name = 'employ/update.html'
    fields = ['emp_no', 'emp_name', 'emp_adress']
    success_url = reverse_lazy('main')


class employ_delete(DeleteView):
    model = employee
    context_object_name = 'emp'
    template_name = 'employ/class_delete.html'
    success_url = reverse_lazy('main')


def view2(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="sample.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["TEAMS", "green11", "pcc", "challengers", "firebirds"])
    writer.writerow(["Captains", "dastgir", "sathish", "venket", "vinoth"])

    return response


from reportlab.pdfgen import canvas
from django.http import FileResponse


def pdf(request):
    Buffer = io.BytesIO()
    p = canvas.Canvas(Buffer)
    p.drawString(100, 100, "hellow world")
    p.showPage()
    p.save()
    Buffer.seek(0)
    return FileResponse(Buffer, as_attachment=True, filename="hello.pdf")


def sdf(request):
    employ = [e.emp_name for e in employee.objects.all()]
    respond = ','.join(employ)
    return HttpResponse(respond)


import pickle


def query1(request):
    qs = employee.objects.values_list("emp_name", "emp_adress")
    return HttpResponse(qs)


def query2(request):
    myq = employee.objects.all()
    myq.query = pickle.loads(pickle.dumps(myq.query))
    return HttpResponse(myq.query)


from .models import for_queryset
from django.http import JsonResponse


def filter(request):
    data = for_queryset.objects.filter(date__year=2024).order_by("name")
    response_text = ', '.join([f"{i.name}" for i in data])
    return JsonResponse(response_text, safe=False)


def order(request):
    data = for_queryset.objects.order_by('-name')
    response_text = ', '.join([f"{i.name}" for i in data])
    return JsonResponse(response_text, safe=False)


def reverse(request):
    data = list(for_queryset.objects.order_by('-id')[:5])
    data.reverse()
    response_text = ','.join([f"{i.name}" for i in data])
    return JsonResponse(response_text, safe=False)


def distinct(request):
    data = for_queryset.objects.all().order_by('name').distinct('name')
    response_text = ','.join([f"{i.name}" for i in data])
    # response_text=[item['name'] for item in data]
    # return HttpResponse(response_text)
    return JsonResponse(response_text, safe=False)


def exclude1(request):
    emp = for_queryset.objects.exclude(date=datetime.date(2024, 5, 29), position='junior')
    # select where not date and junior=======definition for exclude
    response_text = ','.join([f"{i.name}" for i in emp])
    return JsonResponse(response_text, safe=False)


def exclude2(request):
    emp = for_queryset.objects.exclude(date=datetime.date(2024, 5, 29)).exclude(position='junior')
    # select where not date or junior=======definition for exclude
    response_text = ','.join([f"{i.name}" for i in emp])
    return JsonResponse(response_text, safe=False)


from .models import author
from django.db.models import Count, Max, DecimalField

from django.db.models import Count, F, Value

def annotate(request):
    authors = author.objects.annotate(book_count=Count(F('books')))
    response_data = [
        {'author': author.name, 'book_count': author.book_count}
        for author in authors
    ]
    return JsonResponse(response_data, safe=False)


def valuee(request):
    authors = author.objects.values()
    return HttpResponse(authors)


def value_list(request):
    authors = employee.objects.values_list('emp_name', 'emp_adress')
    author_list = (authors)
    return HttpResponse(author_list)


def firstt(request):
    authors = author.objects.all().order_by('name').first()
    if author:
        response = {'id': authors.id, "name": authors.name}
    else:
        pass

    return JsonResponse(response, safe=False)


from .models import product
from django.db.models import Sum, Avg, Max, Min


def count(request):
    prod = product.objects.count()
    return HttpResponse(prod)


def sum(request):
    prod = product.objects.aggregate(prod=Sum('amount'))
    return JsonResponse(prod)


def avg(request):
    prod = product.objects.aggregate(prod=Avg('amount'))
    return JsonResponse(prod)


def max(request):
    prod = product.objects.aggregate(prod=Max('amount'))
    return JsonResponse(prod)


def filter_max(request):
    max_amount = product.objects.aggregate(max_amount=Max('amount'))['max_amount']
    max_prod = product.objects.filter(amount=max_amount)
    response = [{"prod.id": prod.id, "prod_name": prod.product, "amount": prod.amount} for prod in max_prod]
    return HttpResponse(response)


from django.db.models import Q
from .models import q_book


def q_find(request):
    book = q_book.objects.filter(Q(author='s') | Q(date=2024))
    # select * from books where author='s' or date=2024
    return HttpResponse(book)


def q_find2(request):
    book = q_book.objects.filter(Q(author="shakesphere") & (Q(date=2021) | Q(date=2023)))
    # select * from books where author='shakesphere'& (date=2021 or date =2023)
    return HttpResponse(book)
from django.http import HttpResponse, Http404
from django.shortcuts import render

import logging
def excep(request ,id=4):
    try:
     obj=q_book.objects.get(id=1)
    except q_book.DoesNotExist:
        raise Http404("Book does not exist")
    # except Exception as e:
    #     return HttpResponse("an error occured",status=500)
    except ValueError:
        return HttpResponse(" a value that given wrong")
    except TypeError:
        return HttpResponse("id value not given")
    except MultipleObjectsReturned:
        return HttpResponse("multiple object returned")
    # try:
    #  obj=q_book.objects.get(id=id)
    #  summary1=q_book.summary
    # except AttributeError:
    #     return HttpResponse("attribute error")

    return HttpResponse("book is avaialabale")

def assert1(request,id=-1):
    try:
        assert id>0
    except AssertionError:
        return HttpResponse("the given not sattisfied ")
    return HttpResponse("ok")

def multiple(rquest):
    try:
     y=for_queryset.objects.get(position="junior")
    except MultipleObjectsReturned as e:
     return HttpResponse("error!",e)



def increment(request):
    product.objects.update(amount=F('amount')-90)
    products=product.objects.all()
    response=[
            {'name': product.product, 'quantity': product.amount}
            for product in products
        ]
    return JsonResponse(response,safe=False)


from django.http import JsonResponse
from django.db.models import F, Value
from django.db.models.functions import Concat, ExtractYear, ExtractQuarter, ExtractWeek, ExtractMinute, Now, Trunc, MD5, \
    NthValue, Rank
from .models import Company


def company_messages_view(request):
    companies = Company.objects.annotate(
        message=Concat(
            Value("Company: "),
            F('name'),
            Value(" needs more chairs.")) )
    response_data = [
        { 'company': company.name,
            'message': company.message}
        for company in companies]
    return JsonResponse(response_data, safe=False)

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import pcc
from .serializer import querychainingserializer

class query(APIView):
    def get(self,request):
        obj=pcc.objects.all()
        ser=querychainingserializer(obj,many=True)
        return Response(ser.data)

from django.db.models import FloatField

from .models import meta_table
from django.db.models.functions import Cast,Collate
def cast(request):
    s=employee.objects.filter(emp_name=Collate(Value("sachin"), "nocase"))
    return HttpResponse(s)
from django.db.models.functions import Floor,Extract,Ceil,Greatest

def extract(request):
    queryset = meta_table.objects.annotate(
    year=Extract('created_at', 'year'),
    month=Extract('created_at', 'month'),
    day=Extract('created_at', 'day'))

    extracted_data = []
    for obj in queryset:
        extracted_data.append((obj.year, obj.month, obj.day))
    return JsonResponse(extracted_data, safe=False)

from .models import queryfuntion
def ceil(request):

    obj = queryfuntion.objects.annotate(
        x_ceil=Ceil('x'),
        y_ceil=Ceil('y') )
    extracted_data = []
    for d in obj:
        extracted_data.append({'x_ceil': d.x_ceil, 'y_ceil': d.y_ceil})
    return JsonResponse(extracted_data, safe=False)

# # authors = author.objects.annotate(book_count=Count('books'))
# # response_data = [
# #     {'author': author.name, 'book_count': author.book_count}
# #     for author in authors
# # ]
# # print(response_data)
# # data = for_queryset.objects.order_by('-name')
# # print(data)
# # reverse1=for_queryset.objects.reverse()
# # print(reverse1)
# # i=product.objects.order_by('amount').distinct('amount')
# # print(i)
# products=product.objects.defer("amount")
# for product in products:
#     print(product.amount)
# print(meta_table.objects.dates("created_at","year"))
# # print(meta_table.objects.none())
# data=author.objects.values_list()
# y=for_queryset.objects.all()
# print(y)

# g=author.objects.annotate(count=Count('books'))
# response=[
#     {"author":author.name,"book_count":author.count}
#     for author in g
# ]
# print(response)
from django.db.models.query import EmptyQuerySet
# print(author.objects.values_list())
# print(for_queryset.objects.dates("date","month"))
# # isinstance(author.objects.none(),EmptyQuerySet)
# o=author.objects.count()
# # print(o)
from .models import constraints
# obj=constraints.objects.filter(age=18).count()
# print(obj)


# obj=constraints.objects.all().order_by('-company_id')
# # obj.reverse()
# print(obj)

# obj1=constraints.objects.values('name')
# obj2=constraints.objects.values('salary')
# obj3=obj1.union(obj2)
# # print(obj3)
# for i in obj3:
#     print(i)
from .models import Book

# obj=Book.objects.select_related('author')
# for book in obj:
#     print(f'{book.title},{book.author.name}')
# from .models import student
# students_with_grades = student.objects.prefetch_related('grade_set')
#
# for student in students_with_grades:
#     print(f'Student: {student.name}')
#     print('Grades:')
#     for grade in student.grade_set.all():
#         print(f'{grade.subject}: {grade.score}')
#     print('\n')
# from .models import Booke
# total_pages = Booke.objects.extra(
#     select={
#         "total_pages": "SELECT SUM(pages) FROM myapp_edition WHERE myapp_edition.book_id = myapp_booke.id"
#     }
# )
# for book in total_pages:
#     print(f'Book: {book.title}, Total Pages: {book.total_pages}')
# query="Select * from author Where name=%s"
# obj=author.objects.raw(query,['sachin'])
# print(obj)

# Define the raw SQL query
# Define the raw SQL query with a placeholder for the product name
# from .models import product
# query = "SELECT * FROM myapp_product WHERE product = %s"
#

# products = product.objects.raw(query, ['jeans'])
#
# for product in products:
#     print(product.product, product.amount)
# obj=product.objects.get(id=1)
# print(obj)

# obj=product.objects.create(product="trouser",amount=250)
# obj.save(force_insert=True)
# obj=product.objects.get_or_create(
#     product='charger',
#     amount='250'
# )
# obj=product.objects.update_or_create(
#     product='jeans',
#     amount=250,
#     defaults={"product": "Bob"}
#
# )
# product.objects.bulk_create(
#     [
#      product(product="sathish",
#              amount=200),
#      product(product="mathew",amount=299)
#
#     ]
#
# )
# product.objects.bulk_update(
#
# [
#      product(product="pcc",
#              amount=200),
#      product(product="avinash",amount=299)
#
#     ]
# )
#
#
# pro=product.objects.count()
# print(pro)

# id_list=[1,2,3]
# obj=product.objects.in_bulk(id_list)
# print(obj)

from django.db.models import Sum,Avg

# obj=q_book.objects.latest("date")
# print(obj)
# obj=product.objects.aggregate(Avg("amount"))
# print(obj)


# y=product.objects.filter(product="formal").explain()
# print(y)
# if y.exists():
#     print('aaaaaaaaaaaa')
# check=product.objects.get(product="jeans")
#
# all=product.objects.all()
# if all.contains(check):
#  print("avaialble")
# y=product.objects.get(product__iexact="MAthew")
# # # y=product.objects.get(id=1)
# print(y)
# z=product.objects.get(product__contains="MaThew")
# print(z)
# from.models import Donor
# donors=Donor.objects.filter(name__endswith="N")
#
# for donor in donors:
#     print(donor.name)
# start_date=datetime.date(2020,1,2)
# end_date=datetime.date(2024,2,5)
# obj=for_queryset.objects.filter(date__range=(start_date,end_date))
# print(obj)
#
# obj=queryfuntion.objects.annotate(totalprice=F("x")+F('y'))
#
# for i in obj:
#     print(i.totalprice)

# obj=queryfuntion.objects.aggregate(y=Max('x'))
# total=obj['y']
# print(total)
# from .models import pcc
# obj=pcc.objects.filter(youngest_player_team__young_player__player="sachin")
# print(obj)
# f=product.objects.filter(Q(product="pcc"))
# print(f)
#
# book = q_book.objects.filter(Q(author='s') | Q(date=2024))

# obj=product.objects.exclude(product="name")
# print(obj)

# authors = author.objects.annotate(book_count=Count('books'))
# response_data = [
# ]
#     {'author': author.name, 'book_count': author.book_count}
#     for author in authors

# obj=product.objects.annotate(name=sum("amount"))
# y=obj['name']
# print(y)
# obj=product.objects.aggregate(sum=Sum("amount"))
# y=obj['sum']
# print(y)
from .models import Donor,manyto
# obj=manyto.objects.prefetch_related("many").all()
# for i in obj:
#    for donors in manyto.name.all():
#        print(donors)

# obj=constraints.objects.filter(age__gte=30).aggregate(Avg("age"))
# print(obj)
from .models import companys,employess,organization
# g=companys.objects.annotate(salary=Max('employess__emp_salary'))
# response=[
#     {"company":com.company_name,"salary":com.salary}
#     for com in g
# ]
# print(response)
# # u=employess.objects.aggregate(Sum('emp_salary'))
# # print(u)
#
# # obj=product.objects.aggregate(Avg("amount"))
# # print(obj)
#
# #
# # obj=employess.objects.aggregate(minimum=Min('emp_salary'))['minimum']
# # obj2=employess.objects.all().filter(emp_salary=obj)
# # print(obj2)
#
#
# obj=employess.objects.filter(emp_adress='hyderbad').values_list('emp_adress')
# print(obj)
#
#
# obj2=employess.objects.all().filter(emp_adress__contains=obj).values()
# print(obj2)
# from .serializer import employeesserializer
#
# class queryy(APIView):
#     def get(self,request):
#      obj=employess.objects.all()
#      ser=employeesserializer(obj,many=True)
#      return Response(ser.data)
#
#
# d=companys.objects.annotate(sum=Min("employess__emp_salary"))
# response=[
#
#     {"company name":i.company_name,"total":i.sum}
#     for i in d
# ]
# print(response)
#
# obj=employess.objects.aggregate(s=Min("emp_salary"))['s']
# print(obj)
# obj2=employess.objects.filter(emp_salary=obj).values()
# print(obj2)
#

# obj1=companys.objects.annotate(no_of_employ=Count("employess__emp_no"))
# response=[
#     {"company_name":i.company_name,"company count":i.no_of_employ}
#     for i in obj1
#
# ]
# print(response)
# obj1=companys.objects.values_list("company_name").annotate(Count("employess__emp_no"))
# print(obj1)
g=[('sachin',),('shanil',)]
# for i in g:+
#     print(i[0][:3])

# obj=employess.objects.all().values_list('emp_name')
# for i in obj:
#     print(i[0][:3])

from django.db.models.functions import Length
# obj=employee.objects.annotate(length=Length('emp_name')).filter(length=7)
# print(obj)

from django.db.models import FloatField ,IntegerField
from django.db.models.functions import Cast,Coalesce
# >>> Author.objects.create(age=25, name="Margaret Smith")
# >>> author = Author.objects.annotate(
# ...     age_as_float=Cast("age", output_field=FloatField()),
# ... ).get()
# >>> print(author.age_as_float)
# obj=constraints.objects.annotate(primary_name=Coalesce('name','age',Value('noname'))).get()
# for i in obj:
#     print(i.primary_name)
from django.db.models import FloatField,IntegerField,CharField
from django.db.models.functions import Cast,Coalesce,Collate,Greatest,JSONObject,Lower,Least,NullIf
from .models import function
# obj=function.objects.annotate(age_as=Cast("age",output_field=FloatField())).get(id=1)
# print(obj.age_as)
# function.objects.create(name="shanmugam",goes_by="shantan")
# objects = function.objects.annotate(
#     hid=Coalesce(
#         Cast('alias', output_field=CharField()),
#         Cast('age', output_field=CharField()),
#         Cast('name', output_field=CharField())))
# for i in objects:
#     print(i.hid)
# obj=function.objects.filter(name=Collate(Value("sYedIrfan"),"nocase"))
#
# print(obj)

# obj=function.objects.annotate(ho=Coalesce('alias','name','goes_by'))
# print(obj)
from .models import great
# obj=great.objects.annotate(ufg=Greatest("age","weight"))
#
# for obj in obj:
#     print(f"Greatest value for {obj.name}: {obj.ufg}")

# obj=great.objects.annotate(json_obj=JSONObject(name=Lower('name'),age=("age"),height=("height"),weight=("weight")))
# for i in obj:
#  print(i.json_obj)
# obj1=great.objects.annotate(least=Least("age","height","weight"))
# for i in obj1:
#     print(i.least)
# obj2=great.objects.annotate(null=NullIf("weight","height"))
# for i in obj2:
#     print(i.null)
from django.db.models.functions import Round,Chr,Concat,Left,Length,Lower,Upper,Substr,LPad,Repeat,Replace,Reverse,Right,RPad,Upper
# obj=queryfuntion.objects.annotate(x_round=Round('y'))
# for i in obj:
#     print(i.x_round)
# y=function.objects.filter(name__startswith=Chr(ord("S")))
# print(y)

# obj=function.objects.annotate(fun=Concat("name","goes_by"))
# print(obj)
# for i in obj:
#     print(i.fun)

# obj=function.objects.annotate(dfg=Left("name",3))
# for i in obj:
#     print(i.dfg)
# obj=function.objects.annotate(len=Length("name"))
# for i in obj:
#     print(i.len)
from django.db.models.functions import FirstValue
# obj=function.objects.annotate(king=FirstValue("name"))
# print(obj)
# function.objects.create(name='sa',age=15)
# obj=function.objects.annotate(jun=LPad("name",8,Value("abc"))).values_list('jun')
# print(obj)

# obj=function.objects.update(name=Repeat(F('name'),3))
# print(obj)
# function.objects.update(name=Replace('name',Value('sivadasan'),Value('unni')))
# g=function.objects.annotate(ghi=Replace('name',Value('unni'),Value('sivadasan'))).values_list('ghi')
# print(g)
# g=function.objects.annotate(fgh=Reverse('name')).values_list()
# print(g)
# obj=function.objects.annotate(gin=Right('name',2)).values_list()
# print(obj)
# obj=function.objects.annotate(hij=RPad("name",15,Value('abc'))).values_list('hij')
# print(obj)
# obj=function.objects.annotate(names=Substr("name",2,5)).values_list("names")
# print(obj)
# function.objects.create(name=' dinesh ')
# o=function.objects.all()
# print(o)
# function.objects.trim
# obj=function.objects.annotate(yes=Upper('name')).values_list('yes')
# print(obj)
# from django.db.models.functions import NthValue
# from .models import rank
# student=rank.objects.order_by('student')
# print(student)

# u=companys.objects.values_list("company_name").annotate(maxi=Count('employess__emp_name'))
# print(u)

# g=companys.objects.annotate(salary=Sum('employess__emp_salary')).values("company_name","salary")
# print(g)
# from django.db.models import Subquery,OuterRef
# company_name_subquery = Subquery(companys.objects.filter(pk=OuterRef('pk')).values('company_name'))
# org_name_subquery = Subquery(organization.objects.filter(pk=OuterRef('pk')).values('org_name'))
#
# result = employess.objects.annotate(
#     company_name=company_name_subquery,
#     org_name=org_name_subquery
# ).values_list('emp_no', 'emp_name', 'company_name', 'org_name')
# print(result)

#
# obj=companys.objects.filter(employess__emp_salary__lt=15000).values_list('company_name','employess__emp_name')
# print(obj)


# obj=companys.objects.annotate(max=Max('employess__emp_salary')).values_list("company_name","max")
# print(obj)
# obj=companys.objects.filter(company_name="super market").aggregate(minimum=Min('employess__emp_salary'))['minimum']
# obj1=employess.objects.filter(emp_salary=obj).values_list()
# print(obj1)
# employes greater than 5000 in supwer markeyt
#
# obj=companys.objects.filter(employess__emp_salary__gte=50000).values("employess__emp_name")
# print(obj)
# obj=employess.objects.filter(emp_salary__gte=5000,companys__company_name='super market').values_list()

# employees = companys.objects.filter(employess__emp_salary__gte=10500,company_name='super market').annotate(cun=Count('employess')).values_list("cun")
# print(employees)
# obj=employess.objects.filter(emp_salary__gte=12000,emp_company_name__company_name='super market').values_list()
# print(obj)
# employ=companys.objects.filter(Q(employess__emp_salary__gte=8500) & Q(company_name='super market')).values_list("employess__emp_name")
# print(employ)
# obj=companys.objects.annotate(y=Min('employess__emp_salary')).values_list("company_name",'y')
# print(obj)
# obj=organization.objects.annotate(y=F("companys__company_name")).values_list()
# print(obj)
# g=employess.objects.filter(emp_salary__lt=10000).values_list()
# print(g)
#
# obj=organization.objects.filter(companys__company_name='jio cinema').values("org_name","owner_name",'org_location','companys__company_name','companys__company_owner')
# print(obj)

# obj=employess.objects.get(emp_adress='ghjkl')
from .models import rank
# obj=rank.objects.create(student='vavachi',score=45)
# obj=rank.objects.exclude(student='sachin')
# print(obj)
# obj=rank.objects.filter(id=1).values()
# print(obj)
# entry=rank.objects.all()[5:10].values()
# print(entry)
# obj=rank.objects.get(student__exact='sachin')
# # print(obj)
# obj=rank.objects.filter(student__iendswith='N').values_list()
# print(obj)
from .models import fields


# start_date = datetime.date(2023, 5, 5)
# end_date = datetime.date(2025, 12, 1)
# u=fields.objects.filter(date__range=(start_date, end_date))
# print(u)
# from .models import Comment,Post
from django.db.models import OuterRef, Subquery
# newest = Comment.objects.filter(post=OuterRef("id")).order_by("-created_at")
# p=Post.objects.annotate(newest_commenter_email=Subquery(newest.values("email"))).values_list()
# print(p)

# company_name_subquery = Subquery(companys.objects.filter(pk=OuterRef('pk')).values('company_name'))
# org_name_subquery = Subquery(organization.objects.filter(pk=OuterRef('pk')).values('org_name'))

# company_name1=(organization.objects.filter(pk=OuterRef('pk'))).values('org_name')
# p=companys.objects.annotate(count=Subquery(company_name1.values('companys__company_name'))).values_list()
# print(p)

# sub query example1
# newest=companys.objects.filter(company_org_name=OuterRef("pk")).order_by("-id")
# df=organization.objects.annotate(newest_company=Subquery(newest.values("company_name")[:1])).values_list()
# print(df)
# obj=companys.objects.annotate(y=Count('employess__emp_salary')).values_list("company_name",'y')
# obj=organization.objects.filter(companys__company_name='jio cinema').values("org_name","owner_name",'org_location','companys__company_name','companys__company_owner')

# obj=organization.objects.annotate(company_owned=Count('companys__company_name')).values()
# print(obj)
# to find total number of employess in each organization
# company_employ_count=companys.objects.filter(company_org_name=OuterRef("pk")).annotate(empcount=Count('employess')).values('empcount')
# organizatione=organization.objects.annotate(org_name=Subquery(company_employ_count.values('empcount'))).values("org_name","org_namef")
# print(organizatione)
# obj=companys.objects.select_related().all()
# for i in obj:
#     print(i.company_org_name)
#
# obj=companys.objects.annotate(average=Avg('employess__emp_salary')).values_list()
# print(obj)
# obj=organization.objects.filter(companys__company_name="jio cinema").values_list('org_name','owner_name','companys__company_name','companys__company_owner')
# print(obj)
from .serializer import employeesserializer

class getemploy(APIView):
    def get(self,request):
        obj=employess.objects.all()
        serial=employeesserializer(obj,many=True)
        return Response(serial.data)
class postemploy(APIView):
    def post(self,request):
        obj=employeesserializer(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response(obj.data,status=status.HTTP_201_CREATED)

class updateemploy(APIView):
    def put(self,request,id):
        obj=employess.objects.get(id=id)
        obje=employeesserializer(obj,data=request.data)
        if obje.is_valid():
            obje.save()
            return Response(obje.data,status=status.HTTP_202_ACCEPTED)

class deleteemploy(APIView):
    def delete(self,request,id):
        obj=employess.objects.get(id=id)
        obje=employeesserializer(obj,data=request.data)
        obj.delete()
        return Response(obje.error_messages,status=status.HTTP_204_NO_CONTENT)

class serializerqueryAPIVIEW(APIView):
    def get(self,request):
        obj=employess.objects.annotate(entries=F('emp_salary')).filter(entries__gt=10000)
        serializer=employeesserializer(obj,many=True)
        return Response(serializer.data)



# obj=employess.objects.annotate(entries=F('emp_salary')).filter(entries__gt=10000).values('emp_name','emp_salary')
# print(obj)
#
# companies_count = companys.objects.alias(employee_count=Count('employess')).values_list()
# print(companies_count)
# organizations_count = organization.objects.alias(
#     total_employees=Sum(
#         F('companies_count')))
# print(organizations_count)
# company_count=companys.objects.alias(total_count=Count(employess)).filter(total_count__gte=1)
# for i in company_count:
#     print(f"company_name{i,company_count}:{i.total_count}")
#
# obj=companys.objects.annotate(count=Count('employess__emp_name')).values_list()
# print(obj)
# obj=companys.objects.alias(some=Count('employess__emp_name')).filter(some__lt=8)
# for i in obj:
#     print(f'{i.company_name}')
# obj=organization.objects.alias(something=Count('companys__company_name')).filter(something__gt=2)
# print(obj)
#
# obj=employess.objects.alias(salarycount=F("emp_salary")).filter(salarycount__lt=1000)
# for o in obj:
#     print(f"company_name:{o.emp_name},{o.salarycount}")
#
# obj=companys.objects.annotate(salaryavg=Avg("employess__emp_salary")).values('company_name','salaryavg')
# print(obj)
# obj=employess.objects.annotate(some=F('emp_name')).values_list('emp_name','emp_company_name__company_name')
# print(obj)

# for i in obj:
#     print(
#        f'emp_name:{i.emp_name},'
#        f'company_name:{i.emp_company_name},'
#        f'company_name:{i.emp_company_name.company_branch},'
#        f'salary_:{i.emp_salary},'
#        f'org_location:{i.emp_company_name.company_org_name.org_location}'
#     )

# obj=employess.objects.filter(emp_name='prem',emp_company_name__company_name='super market').values_list().iterator(chunk_size=60)
# print(obj)
#
#
#
# for i in obj:
#     print(i)


# y=employess.objects.annotate(something=Cast('emp_salary',output_field=FloatField())).values_list('something')
# print(y)
# y=employess.objects.annotate(some=Coalesce('emp_name','emp_adress')).values_list()
# print(y)

# y=employess.objects.filter(emp_name=Collate(Value('vaVacHI'),'nocase'))
# print(y)

# y=queryfuntion.objects.annotate(some=Greatest('x','y')).values()
# print(y)

# s=employess.objects.annotate(dig=JSONObject(
#
# name=Lower("emp_name"),
# salary=('emp_salary'),
# company=('emp_company_name__company_name'),
# )).values('dig')
# print(s)
# s=queryfuntion.objects.annotate(fgh=Least('x','y')).values()
# print(s)
# fg=employess.objects.annotate(some=NullIf('emp_name','emp_adress')).values('some')
# print(fg)
from .models import Post


# y=Post.objects.annotate(year=ExtractQuarter('date_field')).values('year')
# y=Post.objects.annotate(year=ExtractWeek('date_field')).values('year')
# print(y)
# y=Post.objects.annotate(year=ExtractMinute('date_field')).values('year')
# print(y)
# y=Post.objects.filter(date_field__lt=Now())
# print(y)
from django.db.models import Count, DateTimeField,DateField
from datetime import datetime
from django.db.models.functions import LPad
from django.db.models.functions import LPad
# y=Post.objects.annotate(start=Trunc('date_field','day',output_field=DateField())).filter(start=datetime(2022,6,1)).values_list('start')
# print(y)
# y=queryfuntion.objects.annotate(fg=Round('x')).values('fg')
# print(y)
# import random
# y=random.random()
# print()
# y=employess.objects.filter(emp_name__startswith=Chr(ord('S')))
# print(y)
# y=employess.objects.annotate(dfg=Concat('emp_name','emp_company_name__company_name')).values('dfg')
# print(y)
# y= employess.objects.annotate(man=LPad('emp_name',10,Value('abc'))).values_list('man')
# print(y)
# obj=employess.objects.annotate(fgf=MD5('emp_name')).values()
# print(obj)
# obj=employess.objects.annotate(something=Substr('emp_name',1,5)).values('something')
# print(obj)
from django.db.models import Window
from django.db.models.functions import DenseRank
# obj=employess.objects.annotate(some=Cast('emp_salary',output_field=FloatField())).values('some')
# print(obj)

# obj=function.objects.annotate(some=Coalesce('goes_by','alias')).values_list('some',flat=True)
# print(obj)
# obj=Post.objects.annotate(some=Trunc('date_field','day',output_field=DateField())).filter(some__gt=datetime(2020,6,1)).values_list('some')
# print(obj)
# obj=employess.objects.annotate(some=NullIf('emp_name','emp_adress')).values('some')
# print(obj)
# obj=employess.objects.annotate(something=Window(expression=DenseRank()),order_by=F('emp_salary').asc()).order_by('emp_salary').values()
# print(obj)

# nth_salary = employess.objects.annotate(
#     nth_salary=NthValue('emp_salary', nth=3, output_field=DecimalField())
# ).order_by('nth_salary').values_list('nth_salary', flat=True).first()
#
# obj=employess.objects.annotate(rank=Rank(order_by=['-emp_salary'],partion_by=['employ_company_name'])).order_by('emp_name','-emp_salary')
# print(obj)
# obj=employess.objects.update(emp_name=Replace('emp_name',Value('sasi'),Value('sri')))
# print(obj)
# obj=employess.objects.annotate(name=Reverse('emp_name',)).values('name')
# print(obj)

class empapi(APIView):
 def get(self,request,emp_name):
     try:
      obj=employess.objects.get(emp_name=emp_name)
     except employess.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
     serializer=employeesserializer(obj)
     return Response(serializer.data)


















