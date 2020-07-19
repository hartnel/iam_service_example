from django.shortcuts import render
# todo/views.py

from django.shortcuts import render
from rest_framework import viewsets          # add this
from .serializers import TodoSerializer      # add this
from .models import Todo                     # add this
        
class TodoView(viewsets.ModelViewSet):       # add this
  serializer_class = TodoSerializer          # add this
  queryset = Todo.objects.all()              # add this


def home(request):
  context = {
  'service' : "Todo App" ,
  'username' : request.GET.get("username" , "None"),
  'token' : request.GET.get("init" , "None")
  }
  return render(request , template_name= 'todo/base.html' , context=context)