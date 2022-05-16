from django.http import HttpResponseRedirect
from django.shortcuts import render
from core.search.search import search as scrappersearch

from .forms import NameForm

def search(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        source=form.data['source']
        target=form.data['target']
        list=scrappersearch(source,target)
        list.reverse()
        list.append(target)
        return render(request,"index.html",{"searchurls":list}) 
    else:
        Form = NameForm()
    