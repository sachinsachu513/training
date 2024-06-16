from django.urls import path,include
from Restapi import views

urlpatterns = [
    path('get/', views.get_user),
    path('post/', views.post_user),
    path('del/<id>', views.delete_user),
    path('update/<id>', views.update_user),
    path('getpost/',views.getandpost),
    path('all/<id>',views.complete),
    path('method',views.get_account),
    path('detail/<id>',views.account_detail),
    path('class_get/',views.snippet_get.as_view()),
    path('combine/<id>/',views.multiple.as_view()),
    path('genric_create/',views.genric_create.as_view()),
    path('genric_list/',views.snipetlist.as_view()),
    path('genric_listcre/',views.snipet2.as_view()),
    path('genric_del/<int:pk>',views.snipet3.as_view()),
    path('genric_upd/<int:pk>',views.snipet4.as_view()),
    path('genric_retr/<int:pk>',views.snipet5.as_view()),
    path('genric_red/<int:pk>',views.snipet6.as_view()),
    path('genric_upd/<int:pk>',views.snipet7.as_view()),
    path('genric_rupd/<int:pk>',views.snipet8.as_view()),
    path('read/',views.read_only.as_view()),
    path('hget/',views.hidden_get.as_view()),
    path('method2/',views.twomethod.as_view()),
    path('source/',views.source.as_view()),

]