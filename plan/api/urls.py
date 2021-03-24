from django.urls import path
from plan.api.views import PlanItemList, PlanItemCreate, PlanList, AgentPlanList, PlanDetail, AgentPlanDetail

app_name = "plan"
urlpatterns = [
    path('plan-list/', PlanList.as_view(), name="plan-list"),
    path('plan-item-list/<int:plan_id>/<int:agent_id>/', PlanItemList.as_view(), name="plan-item-list"),
    path('plan-item-create/', PlanItemCreate.as_view(), name="plan-item-create"),
    path('agent-plan-list/', AgentPlanList.as_view(), name="agent-plan-list"),
    path('plan-detail/<int:agent_id>/', PlanDetail.as_view(), name="plan-detail"),
    path('agent-plan-detail/<int:agent_id>/', AgentPlanDetail.as_view(), name="agent-plan-detail"),
]
