from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todolistclassviews.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include("django.contrib.auth.urls"))
]
