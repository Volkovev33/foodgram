from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls', 'api'), namespace='receipt')),
    path("api/", include('users.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/docs/download', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'
    ),
]
