from django.urls import path

from expense_discount.api.views import DiscountList, AndroidDiscountList, AndroidDiscountProducts, ExpenseList,\
     ExpenseDetail, DiscountDetail

app_name = "expense_discount"
urlpatterns = [
    path('discount/', DiscountList.as_view(), name="discount"),
    path('discount-detail/<int:pk>/', DiscountDetail.as_view(), name="discount-detail"),
    path('agent-discount-list/', AndroidDiscountList.as_view(), name='agent-discount-list'),
    path('discount-products/<int:discount_id>/', AndroidDiscountProducts.as_view(), name='discount-products'),
    path('expense-list/', ExpenseList.as_view(), name="expense-list"),
    path('expense-detail/<int:pk>/', ExpenseDetail.as_view(), name="expense-detail")
]
