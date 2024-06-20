"""
URL configuration for myproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from myapp import views
from myapp.views import employes,create_employ,employ_update,employ_delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get/', views.getprice),
    path('result/', views.totalprice),
    path('add/',views.add_employ),
    path('view/',views.get_data,name='main'),
    path('choice/',views.choice_form),
    path('delete/<id>',views.delee),
    path('update/<id>',views.update),
    path('time/',views.curent_time),
    # path('staus/',views.status_code),
    # path('myview/',views.exception_error),
    path('search/',views.check),
    path('listview/',employes.as_view(),name='list'),
    path('createview/',create_employ.as_view(),name='create'),
    re_path(r'update/(?P<pk>\d+)/',employ_update.as_view(),name='update'),
    re_path(r'delete/(?P<pk>\d+)/',employ_delete.as_view(),name='delete'),
    path('csv/',views.view2),
    path('pdf/',views.pdf),
    path('sdf/',views.sdf),
    path('q1/',views.query1),
    path('q2/',views.query2),
    path('filter/',views.filter),
    path('order/',views.order),
    path('reverse/',views.reverse),
    path('distinct/',views.distinct),
    path('exclude1/',views.exclude1),
    path('exclude2/',views.exclude2),
    # path('async/',views.asy),
    path('annotate/',views.annotate),
    path('valuee/',views.valuee),
    path('value2/',views.value_list),
    path('first/',views.firstt),
    path('count/',views.count),
    path('sum/',views.sum),
    # path('avg/',views.avg),
    path('max/',views.max),
    path('filtermax/',views.filter_max),
    path('q_find/',views.q_find),
    path('q_find2/',views.q_find2),
    path('excep/',views.excep),
    path('assert/',views.assert1),
    # path('raw/',views.raw),
    path('multiple/',views.multiple),
    path('rest/',include("Restapi.urls")),
    path('increment/',views.increment),
    path('chair/',views.company_messages_view),
    # path('query/', views.query.as_view()),
    path('cast/', views.cast),
    path('extract/', views.extract),
    path('ceil/', views.ceil),
    # path('hmm/', views.queryy.as_view()),
    path('getem/', views.getemploy.as_view()),
    path('postem/', views.postemploy.as_view()),
    path('updateem/<id>', views.updateemploy.as_view()),
    path('deleteem/<id>',views.deleteemploy.as_view()),
    path('newww/',views.serializerqueryAPIVIEW.as_view()),
    path('urlqry/<str:emp_name>/',views.empapi().as_view()),
    path('beck/', views.spor().as_view()),
    path('jk/', views.annotatemethod().as_view()),
    path('task/', views.task.as_view()),
    path('school/',include("school.urls")),


]





















