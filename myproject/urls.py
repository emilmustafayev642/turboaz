"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('apex-super-emil/', admin.site.urls),
    path('', include('main.urls')),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/delete/<int:listing_id>/', views.staff_delete_listing, name='staff_delete_listing'),
    path('staff/restore/<int:listing_id>/', views.staff_restore_listing, name='staff_restore_listing'),
    path('staff/verify/<int:listing_id>/', views.staff_verify_listing, name='staff_verify_listing'),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )