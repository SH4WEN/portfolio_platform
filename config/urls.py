from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

handler404 = 'config.urls.custom_404'
handler500 = 'config.urls.custom_500'

from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('admin/', admin.site.urls),
    path('dashboard/', include('apps.core.urls', namespace='core')),
    path('dashboard/clients/', include('apps.clients.urls', namespace='clients')),
    path('', include('apps.portfolios.urls', namespace='portfolios')),
    path('', include('apps.media_manager.urls', namespace='media_manager')),
]
