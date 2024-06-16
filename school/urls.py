from django.urls import path
from school import views


urlpatterns=[
    path('hi/', views.student.as_view()),
]