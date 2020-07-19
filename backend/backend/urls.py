
# backend/urls.py

from django.contrib import admin
from django.urls import path, include   , re_path               # add this
from rest_framework import routers                    # add this
from todo import views                            # add this
from aaa_services.views import home

router = routers.DefaultRouter()                      # add this
router.register(r'todos', views.TodoView, 'todo')     # add this
        
urlpatterns = [
    path('admin/', admin.site.urls),           
    path('api/', include(router.urls)),
    path('' , views.home , name="init"),
    path('dev/', home),
]