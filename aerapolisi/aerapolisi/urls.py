from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls")),
    path('logpage/', include("logapp.urls")),
    path('shop/', include('shop.urls')),
    path('management/', include('management.urls')),
    path('chat_rooms/', include('chat_rooms.urls')),
    path('transactions/', include('transactions.urls')),
    path('captcha/', include('captcha.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
