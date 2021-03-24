from django.contrib import admin

from client.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "phone_number1", "responsible_agent", "get_sale_agent_name"]

    def get_sale_agent_name(self, obj):
        return obj.sale_agent.last_name


admin.site.register(Client, ClientAdmin)
