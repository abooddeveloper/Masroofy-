from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('register_login.urls')),
    path('', include('expensesApp.urls')),

    # Added name='home' so redirect('home') and {% url 'home' %} work
    path('home/', home, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
