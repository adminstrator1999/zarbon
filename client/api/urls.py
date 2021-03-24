from django.urls import path

from client.api.views import ClientList, ClientDetail, AgentClientReportList, AgentClientReportDetail

app_name = "client"
urlpatterns = [
    path('client-list/', ClientList.as_view(), name="client-list"),
    path('client-detail/<int:pk>/', ClientDetail.as_view(), name="client-detail"),
    path('agent-client-report/', AgentClientReportList.as_view(), name="agent-client-report"),
    path('agent-client-report-detail/<int:pk>/', AgentClientReportDetail.as_view(), name="agent-client-report-detail")
]
