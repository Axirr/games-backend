from django.contrib import admin
from django.urls import include, path

urlpatterns = [
            path('', include('hello_world.urls')),
                path('admin/', admin.site.urls),
                ]
