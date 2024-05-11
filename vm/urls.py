from django.contrib import admin
from django.urls import path, include
from api import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.no_end_point),
    path('api/', include('api.urls')),
]
