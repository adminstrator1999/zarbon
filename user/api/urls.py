from django.urls import path
from .views import CustomAuthToken, UserRegistrationView, SaleAgentList, UserList, UserDetail

app_name = "user"
urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name="login"),
    path('register/', UserRegistrationView.as_view(), name="registration"),
    path('agent-list/', SaleAgentList.as_view(), name="agent-list"),
    path('user-list/', UserList.as_view(), name="user-list"),
    path('user-detail/<int:pk>/', UserDetail.as_view(), name="user-detail")
]
