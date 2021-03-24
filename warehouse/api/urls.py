from django.urls import path

from warehouse.api.views import WarehouseList


app_name = "warehouse"
urlpatterns = [
    path("warehouse-list/", WarehouseList.as_view(), name="warehouse-list")
]
