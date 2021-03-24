from django.contrib import admin
from order.models import BuyOrder


class BuyOrderAdmin(admin.ModelAdmin):
    list_display = ['get_product_name', 'get_provider_name', 'price', 'quantity']

    def get_product_name(self, obj):
        return obj.product.name

    def get_provider_name(self, obj):
        return obj.provider.name


admin.site.register(BuyOrder, BuyOrderAdmin)
