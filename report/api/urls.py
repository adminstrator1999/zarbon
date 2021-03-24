from django.urls import path
from report.api.views import BuyOrderDebtList, ProviderDebtList, ProviderDebtRetrieve, ClientDebtList,\
    ClientDebtRetrieve, AgentClientDebtList, ProfitList, DirectorSellOrderList, DirectorBuyOrderList, \
    SaleAgentReportList, SaleAgentReportDetail, ProfitReport, ClientReport, ClientDateReport, WarehouseList, \
    GivenAgentReportList, ProfitDelete, GroupedAgentReport, GroupedDateAgentReport


app_name = "report"
urlpatterns = [
    path("buy-order-debt-list/", BuyOrderDebtList.as_view(), name="buy-order-debt-list"),
    path("provider-debt-list/", ProviderDebtList.as_view(), name="provider-debt-list"),
    path("provider-debt-retrieve/<int:pk>/", ProviderDebtRetrieve.as_view(), name="provider-debt-retrieve"),
    path("client-debt-list/", ClientDebtList.as_view(), name="client-debt-list"),
    path("client-debt-retrieve/<int:pk>/", ClientDebtRetrieve.as_view(), name="client-debt-retrieve"),
    path("client-debt-list/<int:agent_id>/", AgentClientDebtList.as_view(), name="agent-client-debt-list"),
    path("profit-list/", ProfitList.as_view(), name="profit-list"),
    path("daily-sell-orders/", DirectorSellOrderList.as_view(), name="daily-sell-orders"),
    path("daily-buy-orders/", DirectorBuyOrderList.as_view(), name="daily-buy-orders"),
    path("agent-photo-report/", SaleAgentReportList.as_view(), name="agent-photo-report"),
    path("agent-photo-report-detail/<int:pk>/", SaleAgentReportDetail.as_view(), name="agent-photo-report-detail"),
    path("profit-report/", ProfitReport.as_view(), name="profit-report"),
    path("client-report/", ClientReport.as_view(), name="client-report"),
    path("date-client-report/", ClientDateReport.as_view(), name="date-client-report"),
    path("warehouse-list/", WarehouseList.as_view(), name="warehouse-list"),
    path("sale-agent-report/<int:agent_id>/", GivenAgentReportList.as_view(), name="sale-agent-report"),
    path("profit-delete/<int:pk>/", ProfitDelete.as_view(), name="profit-delete"),
    path("grouped-agent-report/", GroupedAgentReport.as_view(), name="grouped-agent-report"),
    path("grouped-date-agent-report/", GroupedDateAgentReport.as_view(), name="grouped-date-agent-report")
]
