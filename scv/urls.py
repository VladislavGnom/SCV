from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('user_app.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('authapp.urls')),
    path('teachers/', include('teacher_app.urls')),
    path('test_api/', include('test_api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, 
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, 
                      document_root=settings.STATIC_ROOT)
