from django import forms
from .models import employee,Person

class myform(forms.ModelForm):
    class Meta:
        model=employee
        fields='__all__'
class iris(forms.ModelForm):
    class Meta:
        model=Person
        fields="__all__"

class views_form(forms.Form):
    username=forms.CharField(max_length=10)

    