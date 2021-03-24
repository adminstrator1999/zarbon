from django.urls import path

from salary.api.views import SalaryList, SalaryDetail, AgentFlexibleSalary, FixedSalaryList, FixedSalaryDetail, \
    SalaryNotGivenUser


app_name = "salary"
urlpatterns = [
    path('fixed-salary-list/', FixedSalaryList.as_view(), name="fixed-salary-list"),
    path('fixed-salary-detail/<int:pk>/', FixedSalaryDetail.as_view(), name="fixed-salary-detail"),
    path('salary-list/', SalaryList.as_view(), name="salary-list"),
    path('salary-detail/<int:pk>/', SalaryDetail.as_view(), name="salary-detail"),
    path('agent-flexible-salary/<int:agent_id>/', AgentFlexibleSalary.as_view(), name="agent-flexible-salary"),
    path('salary-not-given-list/', SalaryNotGivenUser.as_view(), name="salary-not-given-list")
]
