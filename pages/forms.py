from django import forms

class NameForm(forms.Form):
    source = forms.CharField(label='source', max_length=100)
    target = forms.CharField(label='target' , max_length=100)