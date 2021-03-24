from django.urls import path

from provider.api.views import ProviderList, ProviderDetail

app_name = "provider"
urlpatterns = [
    path('provider-list/', ProviderList.as_view(), name="provider-list"),
    path('provider-detail/<int:pk>/', ProviderDetail.as_view(), name="provider-detail")
]
