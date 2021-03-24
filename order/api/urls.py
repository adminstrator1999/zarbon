from django.urls import path
from order.api.views import BuyOrderList, BuyOrderDetail, SellOrderList, SellOrderDetail, BuyOrderPaymentList, \
    BuyOrderPaymentDetail, SellOrderPaymentList, SellOrderPaymentDetail, ProviderFailedProductList, \
    ClientFailedProductList, AgentSellOrder, BuyOrderGroupedList, BuyOrderDateGroupedList, SellOrderGroupedList, \
    SellOrderDateGroupedList, GetBuyOrderPaymentList, ProfitReport, ProfitGroupReport, DailyProfit, ClientSellOrderList, \
    ClientFailedProductDetail, ProviderFailedProductDetail

app_name = 'order'
urlpatterns = [
    path("buy-order-list/", BuyOrderList.as_view(), name="buy-order-create"),
    path("buy-order-group-list/", BuyOrderGroupedList.as_view(), name="buy-order-group-list"),
    path("buy-order-date-grouped-list/", BuyOrderDateGroupedList.as_view(), name="buy-order-date-grouped-list"),
    path("sell-order-group-list/", SellOrderGroupedList.as_view(), name="sell-order-date-list"),
    path("sell-order-date-grouped-list/", SellOrderDateGroupedList.as_view(), name="sell-order-date-grouped-list"),
    path("buy-order-payment/", BuyOrderPaymentList.as_view(), name="buy-order-payment"),
    path("buy-order-payment-detail/", BuyOrderPaymentDetail.as_view(), name="buy-order-payment-detail"),
    path("buy-order-detail/<int:pk>/", BuyOrderDetail.as_view(), name="buy-order-detail"),
    path("sell-order-list/", SellOrderList.as_view(), name="sell-order-list"),
    path("sell-order-detail/<int:pk>/", SellOrderDetail.as_view(), name="sell-order-detail"),
    path("sell-order-payment/", SellOrderPaymentList.as_view(), name="sell-order-payment"),
    path("sell-order-payment-detail/<int:pk>/", SellOrderPaymentDetail.as_view(), name="sell-order-payment-detail"),
    path("provider-failed-product-list/", ProviderFailedProductList.as_view(), name="provider-failed-product-list"),
    path("provider-failed-product-detail/<int:pk>/", ProviderFailedProductDetail.as_view(), name="provider-failed-product-detail"),
    path("client-failed-product-list/", ClientFailedProductList.as_view(), name="client-failed-product-list"),
    path("client-failed-product-detail/<int:pk>/", ClientFailedProductDetail.as_view(),
         name="client-failed-product-detail"),
    path("agent-order-list/<int:agent_id>/", AgentSellOrder.as_view(), name="agent-order-list"),
    path("get-buy-order-payment-list/<int:order_id>/", GetBuyOrderPaymentList.as_view(),
         name="get-buy-order-payment-list"),
    path("profit-report/", ProfitReport.as_view(), name="profit-report"),
    path("grouped-profit-report/", ProfitGroupReport.as_view(), name="grouped-profit-report"),
    path("daily-profit/", DailyProfit.as_view(), name="daily-profit"),
    path("client-sell-order-list/<int:client_id>/", ClientSellOrderList.as_view(), name="client-sell-order-list"),

]

