from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])