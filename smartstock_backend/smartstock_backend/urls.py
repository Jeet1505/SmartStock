"""
URL configuration for smartstock_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: HttpResponse("""
        <html>
            <head>
                <title>SmartStock</title>
            </head>
            <body style="background-color: #f5f7fa; text-align: center; padding-top: 100px; font-family: Arial, sans-serif;">
                <h1 style="color: #333;">🚀 Welcome to <span style="color: #007bff;">SmartStock API</span> 👋</h1>
                <p style="font-size: 18px; color: #666;">Your gateway to smart stock screening and analysis.</p>
            </body>
        </html>
    """)),
    path('api/', include('authapp.urls')),  # adjust if your app has a different name
]
