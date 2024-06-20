import io
import json
import os

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


def excep(request, id=4):
    try:
        obj = q_book.objects.get(id=1)
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


def assert1(request, id=-1):
    try:
        assert id > 0
    except AssertionError:
        return HttpResponse("the given not sattisfied ")
    return HttpResponse("ok")


def multiple(rquest):
    try:
        y = for_queryset.objects.get(position="junior")
    except MultipleObjectsReturned as e:
        return HttpResponse("error!", e)


def increment(request):
    product.objects.update(amount=F('amount') - 90)
    products = product.objects.all()
    response = [
        {'name': product.product, 'quantity': product.amount}
        for product in products
    ]
    return JsonResponse(response, safe=False)


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
            Value(" needs more chairs.")))
    response_data = [
        {'company': company.name,
         'message': company.message}
        for company in companies]
    return JsonResponse(response_data, safe=False)


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import pcc
from .serializer import querychainingserializer


class query(APIView):
    def get(self, request):
        obj = pcc.objects.all()
        ser = querychainingserializer(obj, many=True)
        return Response(ser.data)


from django.db.models import FloatField

from .models import meta_table
from django.db.models.functions import Cast, Collate


def cast(request):
    s = employee.objects.filter(emp_name=Collate(Value("sachin"), "nocase"))
    return HttpResponse(s)


from django.db.models.functions import Floor, Extract, Ceil, Greatest


def extract(request):
    queryset = meta_table.objects.annotate(
        year=Extract('created_at', 'year'),
        month=Extract('created_at', 'month'),
        day=Extract('created_at', 'day'))

    extracted_data = []
    for obj in queryset:
        extracted_data.append((obj.year, obj.month, obj.day))
    return JsonResponse(extracted_data,safe=False)


from .models import queryfuntion


def ceil(request):
    obj = queryfuntion.objects.annotate(
        x_ceil=Ceil('x'),
        y_ceil=Ceil('y'))
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

from django.db.models import Sum, Avg

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
from .models import Donor, manyto
# obj=manyto.objects.prefetch_related("many").all()
# for i in obj:
#    for donors in manyto.name.all():
#        print(donors)

# obj=constraints.objects.filter(age__gte=30).aggregate(Avg("age"))
# print(obj)
from .models import companys, employess, organization

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
g = [('sachin',), ('shanil',)]
# for i in g:+
#     print(i[0][:3])

# obj=employess.objects.all().values_list('emp_name')
# for i in obj:
#     print(i[0][:3])

from django.db.models.functions import Length
# obj=employee.objects.annotate(length=Length('emp_name')).filter(length=7)
# print(obj)

from django.db.models import FloatField, IntegerField
from django.db.models.functions import Cast, Coalesce
# >>> Author.objects.create(age=25, name="Margaret Smith")
# >>> author = Author.objects.annotate(
# ...     age_as_float=Cast("age", output_field=FloatField()),
# ... ).get()
# >>> print(author.age_as_float)
# obj=constraints.objects.annotate(primary_name=Coalesce('name','age',Value('noname'))).get()
# for i in obj:
#     print(i.primary_name)
from django.db.models import FloatField, IntegerField, CharField
from django.db.models.functions import Cast, Coalesce, Collate, Greatest, JSONObject, Lower, Least, NullIf
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
from django.db.models.functions import Round, Chr, Concat, Left, Length, Lower, Upper, Substr, LPad, Repeat, Replace, \
    Reverse, Right, RPad, Upper
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
obj = organization.objects.filter(companys__company_name='jio cinema').values("org_name", "owner_name", 'org_location',
                                                                              'companys__company_name',
                                                                              'companys__company_owner')
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
    def get(self, request):
        obj = employess.objects.all()
        serial = employeesserializer(obj, many=True)
        return Response(serial.data)


class postemploy(APIView):
    def post(self, request):
        obj = employeesserializer(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response(obj.data, status=status.HTTP_201_CREATED)


class updateemploy(APIView):
    def put(self, request, id):
        obj = employess.objects.get(id=id)
        obje = employeesserializer(obj, data=request.data)
        if obje.is_valid():
            obje.save()
            return Response(obje.data, status=status.HTTP_202_ACCEPTED)


class deleteemploy(APIView):
    def delete(self, request, id):
        obj = employess.objects.get(id=id)
        obje = employeesserializer(obj, data=request.data)
        obj.delete()
        return Response(obje.error_messages, status=status.HTTP_204_NO_CONTENT)


class serializerqueryAPIVIEW(APIView):
    def get(self, request):
        obj = employess.objects.annotate(entries=F('emp_salary')).filter(entries__gt=10000)
        serializer = employeesserializer(obj, many=True)
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
from django.db.models import Count, DateTimeField, DateField
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
    def get(self, request, emp_name):
        try:
            obj = employess.objects.get(emp_name=emp_name)
        except employess.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = employeesserializer(obj)
        return Response(serializer.data)


# obj=employess.objects.annotate(something=F('emp_salary')).order_by('-emp_salary').values_list('emp_name','emp_salary')[:5]
# print(obj)
# obj=employess.objects.annotate(jkm=F('emp_name')).order_by('emp_name').values_list('emp_name')
# print(obj)
# obj=organization.objects.filter(companys__company_name='goodday').values_list("org_name","org_location","companys__company_owner","companys__company_name")
# print(obj)
obj = companys.objects.filter(company_name='jio cinema').select_related('company_org_name').annotate(
    some=Max("employess__emp_salary")).values_list("some",flat=True)
print(obj)

from .serializer import somethingserializer

from django.core.serializers.json import DjangoJSONEncoder
class spor(APIView):
    def post(self, request):

        if request.method == "POST":
            obj = companys.objects.all().select_related('company_org_name').annotate(
                maximum=Max("employess__emp_salary")).values("company_name","company_org_name__org_name","company_org_name__owner_name","maximum")


            response=[
                { "company_name":i["company_name"],
                "org_name":i["company_org_name__org_name"],
                "owner_name":i["company_org_name__owner_name"],
                "maximum":i["maximum"],
                  }
                for i in obj
            ]
            return Response(response)


class annotatemethod (APIView):
    def post(self,request):
        if request.method=="POST":
            obj = companys.objects.annotate(some=Min('employess__emp_salary')).values("company_name", "some")
            response=[
               {
                "company_name":i["company_name"],
                "salary":i["some"]

               }
                   for i in obj

           ]
            return Response(response)


g=companys.objects.annotate(salary=Sum('employess__emp_salary')).values("company_name","salary")
print(g)
#
# obj = companys.objects.annotate(some=Min('employess__emp_salary')).values("company_name", "some")
# print(obj)
# salaries = employess.objects.values_list('emp_salary',flat=True)
# print(salaries)
#
# obj=employess.objects.annotate(some=Min('emp_salary')).values("emp_company_name__company_name","some")
# print(obj)
from .serializer import taskserializer
from django.db import IntegrityError

import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


from .common import file_upload,get_file_source


def custom_error_response(status_code,message,error=True):
    response = {
        "status_code":status_code,
        "message": f"{message}",
        "error": error
    }
    return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def custom_error_response(message, status_code=404, error=True):
    response = {
        "status_code": status_code,
        "message": message,
        "error": error
    }
    return Response(response, status=status_code)

class task(APIView):

    def post(self, request):
        if request.method == "POST":
            action = request.data.get("action")
            if action == 'view employess':
                try:
                    company_id = request.data["company_id"]
                    company = companys.objects.get(id=company_id)
                except companys.DoesNotExist:
                    return custom_error_response(message="Company does not exist", status_code=404)



                employees = employess.objects.filter(emp_company_name=company).values(
                    'id', 'emp_no', 'emp_name', 'emp_adress', 'emp_salary','imageb64'
                )

                response = []

                for emp in employees:
                    file_data = {
                        "P40_File_Source": "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",
                        "P40_File_Name": emp['emp_name'],
                        "P40_File_Format": "jpg",
                    }
                    uploaded_path = file_upload(organization_id=company_id, file_data=file_data,update=True)

                    y = get_file_source(uploaded_path)


                    emp_data = {
                        "emp_no": emp['emp_no'],
                        "emp_name": emp['emp_name'],
                        "emp_adress": emp['emp_adress'],
                        "emp_salary": emp['emp_salary'],
                        "emp_image": y,
                    }
                    response.append(emp_data)
                return Response(response, status=status.HTTP_200_OK)


            elif action=='create':
                emp_no=request.data["emp_no"]

                try:
                    emp_names=request.data["emp_name"]
                    emp_company=request.data["company_id"]
                    emp_salary=request.data["emp_salary"]
                    adress=request.data["emp_adress"]
                    obj=companys.objects.get(id=emp_company)
                except companys.DoesNotExist:
                    return custom_error_response(message="company does not exist",status_code=404)


                try:
                 employess.objects.create(emp_no=emp_no,emp_name=emp_names,emp_company_name=obj,emp_salary=emp_salary,emp_adress=adress)
                except IntegrityError as e:
                    return custom_error_response(message="Integrity error ",status_code=406)


                return custom_error_response(message="emp added sucessfully",status_code=201,error=False)



            elif action=='Delete':
                try:
                    emp_no=request.data["emp_id"]
                    obj=employess.objects.get(id=emp_no)
                    obj.delete()
                    return custom_error_response(message="emp Deleted sucessfully", status_code=200, error=False)

                except employess.DoesNotExist:
                    return custom_error_response(message="employ does not exist",status_code=404)


            elif action=='update':

                emp_id = request.data['emp_id']
                emp_adress=request.data["emp_adress"]
                emp_salary=request.data["emp_salary"]
                emp_no=request.data["emp_no"]

                try:
                    emp_name = request.data['emp_name']
                    obj=employess.objects.get(id=emp_id)
                except employess.DoesNotExist:
                    return Response({'error': 'emp does not exist'}, status=status.HTTP_400_BAD_REQUEST)


                try:
                 employess.objects.filter(id=emp_id).update(emp_name=emp_name,emp_adress=emp_adress,emp_salary=emp_salary,emp_no=emp_no)
                except IntegrityError:
                    return custom_error_response(message="employ no already exist ",status_code=404)
                return custom_error_response(message="emp updated sucessfully",status_code=200,error=False)


# obj=companys.objects.filter(id=1).values('employess__emp_name',"employess__emp_adress","employess__emp_name")
# print(obj)

from PIL import Image
im=Image.open("files/8/yuvi.jpeg")
im.save("files/compress/yuvicompress.jpeg",format="JPEG",quality=10)




# def encode_img():
#     with open("files/compress/yuvicompress.jpeg", "rb") as f:
#         data = f.read()
#         encode_data=base64.b64encode(data).decode('utf-8')
#         return encode_data
#
# y=encode_img()
# # print(y)
#
# def compress():
#     im=Image.open("files/8/virat.jpeg")
#     im.save("files/compress/viratcompress.jpeg",format="JPEG",quality=40)
#     with open("files/compress/viratcompress.jpeg","rb") as f:
#         data=f.read()
#         encode_data=base64.b64encode(data).decode('utf-8')
#         return encode_data
#
# y=compress()
# print(y)




# compressing image and compressing image to bas64
from PIL import Image
def compress_and_encode(image_path,output_path,format="JPEG",quality=40):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im=Image.open(image_path)
    im.save(output_path,format=format,quality=quality)
    with open(output_path,"rb") as f:
        data=f.read()
        encode_data=base64.b64encode(data).decode('utf-8')
        return encode_data

image_path="files/8/yuvi.jpeg"
output_path="files/8/compressen/yuvinewcompress.jpeg"
y=compress_and_encode(image_path,output_path)
# print(y)


import base64
import gzip
from io import BytesIO
def compress_bas64(base64_image):
    decode_data=base64.b64decode(base64_image)

    buffer = BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb") as compressGzip:
        compressGzip.write(decode_data)

    compressed_data = buffer.getvalue()

    compressed_base64_data = base64.b64encode(compressed_data).decode('utf-8')

    return compressed_base64_data


def decompress_base64_image(compressed_base64_image):
    # Decode the base64 compressed image
    compressed_data = base64.b64decode(compressed_base64_image)
    # Decompress the gzip data
    buffer = BytesIO(compressed_data)
    with gzip.GzipFile(fileobj=buffer, mode='rb') as decompressGzip:
        original_data = decompressGzip.read()

    # Encode the decompressed data back to base64
    original_base64_data = base64.b64encode(original_data).decode('utf-8')

    return original_base64_data


base64_image="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"

y=compress_bas64(base64_image)

x=decompress_base64_image(y)
print(x)


























