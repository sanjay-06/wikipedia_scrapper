from django.urls import path
from django.views import View
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('',TemplateView.as_view(template_name = 'index.html')),
    path('search', views.search, name="search")
]