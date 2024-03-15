from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include('users.urls')),
    path('api/', include(('api.urls', 'api'), namespace='receipt')),
    path('api/auth/', include('djoser.urls.authtoken')),
]