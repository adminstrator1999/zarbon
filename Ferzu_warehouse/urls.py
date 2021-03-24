"""Ferzu_warehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/product/', include('product.api.urls')),
    path('api/provider/', include('provider.api.urls')),
    path('api/client/', include('client.api.urls')),
    path('api/order/', include('order.api.urls')),
    path('api/report/', include('report.api.urls')),
    path('api/user/', include('user.api.urls')),
    path('api/expense_discount/', include('expense_discount.api.urls')),
    path('api/plan/', include('plan.api.urls')),
    path('api/salary/', include('salary.api.urls')),
    path('api/warehouse/', include('warehouse.api.urls')),
    path('docs/', include_docs_urls(title='FerzuAPi')),
    path('schema/', get_schema_view(
        title="APIs",
        description="API for FERZU warehouse",
    ), name="openapi-schema")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
               static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

