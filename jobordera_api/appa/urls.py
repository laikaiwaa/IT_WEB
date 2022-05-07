"""django2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
import random
from django.contrib import admin
from django.urls import path
import appa.views as views
from django.conf.urls.static import static
from django.conf  import settings

adminr=random.randint(0,9)
urlpatterns = [
    path('', views.login),
    path('admin/', views.admin),
    path('usehistory/', views.usehistory),
    path('user/',views.user),
    path('xuser/',views.xuser),
    path('liekiewaa/',views.jb),
    path('qr/',views.qr),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
