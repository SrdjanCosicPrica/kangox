from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ht/', include('health_check.urls')),
    path('ping/', lambda x: HttpResponse('pong')),
]
