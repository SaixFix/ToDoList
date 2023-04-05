from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from todolist import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('oauth/', include('social_django.urls', namespace="social")),
    path('goals/', include('goals.urls')),

]

if settings.DEBUG:
    urlpatterns += [
        path('', include('rest_framework.urls')),
    ]
