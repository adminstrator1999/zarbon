from django.urls import path
from product.api import views

app_name = "product"
urlpatterns = [
    path('product-list-no-pagination', views.ProductListNoPagination.as_view(), name="product-list-no-pagination"),
    path('product-list/', views.ProductList.as_view(), name="product-list"),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name="product-detail"),
    path('category-list/', views.CategoryList.as_view(), name="category-list"),
    path('category-detail/<int:pk>/', views.CategoryDetail.as_view(), name="category-detail"),
    path('category-product/<int:category_id>/', views.CategoryProductList.as_view(), name="category-product")
]
