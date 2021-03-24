from rest_framework.permissions import BasePermission, SAFE_METHODS


# defining custom permissions according to the role of the user
class IsCEO(BasePermission):
    message = "You must be CEO of this company"

    def has_permission(self, request, view):
        if request.method in list(SAFE_METHODS):
            return request.user.role == "CEO"


class IsDirector(BasePermission):
    message = "You must be the Director of this company"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == "director"


class IsCommodityAccountant(BasePermission):
    message = "You must be the Commodity Accountant of this company"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == "commodity_accountant"


class IsAccountant(BasePermission):
    message = "You must be the Accountant of this company"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == "accountant"


class IsCashier(BasePermission):
    message = "You must be the Cashier of this company"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == "cashier"


class IsAgent(BasePermission):
    message = "You must be the Agent of this company"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == "agent"
