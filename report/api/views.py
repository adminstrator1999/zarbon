from django.db.models import Q
from django.http import Http404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta, datetime
from django.utils import timezone

from order.models import BuyOrder, BuyOrderPayment, SellOrder
from provider.models import Provider
from client.models import Client
from report.models import SaleAgentReport, Profit
from user.models import User
from warehouse.models import Warehouse
from order.api.serializers import BuyOrderGetSerializer, BuyOrderPaymentGetSerializer, SellOrderGetSerializer, \
    SellOrderPayment, SellOrderPaymentGetSerializer, SellOrderSerializer
from report.api.serializers import ProviderDebtSerializer, ClientDebtSerializer, AgentClientDebtSerializer, \
    DirectorWarehouseSerializer, SaleAgentReportSerializer, SaleAgentReportGetSerializer
from expense_discount.models import Expense


def string_to_date(date):
    if date:
        format = "%Y-%m-%d"
        return datetime.strptime(date, format)
    else:
        pass


def get_search_query(request):
    param = request.query_params
    term = param.get("term", False)
    return term


def get_dates(request):
    param = request.query_params
    start_date = string_to_date(param.get("start_date", False)) or (timezone.now() - timedelta(days=7)).replace(
        tzinfo=None)
    end_date = string_to_date(param.get("end_date", False)) or (timezone.now()).replace(tzinfo=None)
    return start_date, end_date


class BuyOrderDebtList(APIView):

    def get(self, request):
        bought_products = BuyOrder.objects.all()
        orders_list = []
        for bought_product in bought_products:
            if bought_product.debt >= 0.00:
                buy_order_serializer = BuyOrderGetSerializer(bought_product)
                buy_order_payments = BuyOrderPayment.objects.filter(buy_order=bought_product.id)
                payments_serializer = BuyOrderPaymentGetSerializer(buy_order_payments, many=True)
                buy_order = {
                    "buy_order": buy_order_serializer.data,
                    "payments": payments_serializer.data
                }
                orders_list.append(buy_order)
        return Response(orders_list, status=status.HTTP_200_OK)


def filter_provider_orders(provider): return BuyOrder.objects.filter(provider=provider.id)


def filter_client_orders(client): return SellOrder.objects.filter(client=client.id, status="delivered")


def filter_all_providers(agent_id): return Provider.objects.all().order_by("-id")


def filter_all_clients(agent_id): return Client.objects.all().order_by("-id")


def filter_agent_clients(agent_id): return Client.objects.filter(sale_agent=agent_id)


def filtered_objects(supplier_objects, supplier_serializer, function, supplier, request, agent_id=None):
    param = request.GET.get('filter', 'all')
    providers = supplier_objects(agent_id=agent_id)
    final_providers = []
    for provider in providers:
        provider_orders = function(provider)
        total_debt = 0
        for provider_order in provider_orders:
            total_debt += provider_order.debt
        serializer = supplier_serializer(provider)
        final_provider_data = {
            supplier: serializer.data,
            "total_debt": total_debt
        }
        final_providers.append(final_provider_data)
    data = []
    for final_provider in final_providers:

        if param == "debt" and final_provider["total_debt"] > 0.00:
            data.append(final_provider)
        elif param == "no_debt" and final_provider["total_debt"] == 0.00:
            data.append(final_provider)
        elif param == "all":
            data.append(final_provider)

    return data


class ProviderDebtList(APIView):

    def get(self, request):
        data = filtered_objects(supplier_objects=filter_all_providers, function=filter_provider_orders,
                                supplier="provider", supplier_serializer=ProviderDebtSerializer,
                                request=request)

        return Response(data, status=status.HTTP_200_OK)


class ProviderDebtRetrieve(APIView):

    def get_object(self, pk):
        try:
            return Provider.objects.get(pk=pk)
        except Provider.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        provider = self.get_object(pk)
        bought_products = BuyOrder.objects.filter(provider=provider.id)
        orders_list = []
        for bought_product in bought_products:
            if bought_product.debt > 0.00:
                buy_order_serializer = BuyOrderGetSerializer(bought_product)
                buy_order_payments = BuyOrderPayment.objects.filter(buy_order=bought_product.id)
                payments_serializer = BuyOrderPaymentGetSerializer(buy_order_payments, many=True)
                buy_order = {
                    "buy_order": buy_order_serializer.data,
                    "payments": payments_serializer.data
                }
                orders_list.append(buy_order)
        return Response(orders_list, status=status.HTTP_200_OK)


class ClientDebtList(APIView):

    def get(self, request):
        data = filtered_objects(supplier_objects=filter_all_clients, function=filter_client_orders,
                                supplier="client", supplier_serializer=ClientDebtSerializer,
                                request=request)
        return Response(data, status=status.HTTP_200_OK)


class AgentClientDebtList(APIView):

    def get(self, request, agent_id):
        data = filtered_objects(supplier_objects=filter_agent_clients, function=filter_client_orders,
                                supplier="client", supplier_serializer=AgentClientDebtSerializer, request=request,
                                agent_id=agent_id)
        return Response(data, status=status.HTTP_200_OK)


class ClientDebtRetrieve(APIView):

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        client = self.get_object(pk)
        sold_products = SellOrder.objects.filter(client=client.id)
        orders_list = []
        for sold_product in sold_products:
            if sold_product.debt >= 0.00:
                sell_order_serializer = SellOrderGetSerializer(sold_product)
                sell_order_payments = SellOrderPayment.objects.filter(sell_order=sold_product.id)
                payments_serializer = SellOrderPaymentGetSerializer(sell_order_payments, many=True)
                sell_order = {
                    "sell_order": sell_order_serializer.data,
                    "payments": payments_serializer.data
                }
                orders_list.append(sell_order)
        return Response(orders_list, status=status.HTTP_200_OK)


def get_total_profit(start_date, end_date):
    products = Warehouse.objects.all()
    total_profit = 0
    for product in products:
        sell_orders = SellOrder.objects.filter(product=product.product, status="delivered", updated_date__gt=start_date,
                                               updated_date__lt=end_date)
        last_price = product.last_price
        total_income = 0
        total_quantity = 0
        for sell_order in sell_orders:
            total_income += sell_order.quantity * sell_order.price
            total_quantity += sell_order.quantity
        total_outcome = total_quantity * last_price
        total_profit += total_outcome - total_income
    return total_profit


class ProfitList(APIView):

    def get(self, request):
        products_profit = []
        products = Warehouse.objects.all()
        total_profit = 0
        for product in products:
            # TODO we need to add filter with dates
            sell_orders = SellOrder.objects.filter(product=product.product, status="delivered")
            last_price = product.last_price
            total_income = 0
            total_quantity = 0
            for sell_order in sell_orders:
                total_income += sell_order.quantity * sell_order.price
                total_quantity += sell_order.quantity

            total_outcome = total_quantity * last_price
            total_profit += total_outcome-total_income
            data = {
                "name": product.product.name,
                "quantity": total_quantity,
                "rest_product_quantity": product.quantity,
                "profit": total_outcome-total_income
            }
            products_profit.append(data)
        context = {
            "products_profit": products_profit,
            "total_profit": total_profit
        }
        return Response(context, status=status.HTTP_200_OK)


# getting daily orders
def daily_orders(model):
    start_date = timezone.now()-timedelta(days=1)
    end_date = start_date + timedelta(days=1)
    return model.objects.filter(created_date__range=(start_date, end_date)).order_by("-id")


# getting orders with date default is a week from now
def date_orders(model, start_date=timezone.now()-timedelta(days=6),
                end_date=timezone.now()+timedelta(days=1)):
    return model.objects.filter(updated_date__range=(start_date, end_date)).order_by("-id")


class DirectorSellOrderList(APIView):

    def get(self, request):
        sell_orders = daily_orders(SellOrder)
        serializer = SellOrderGetSerializer(sell_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DirectorBuyOrderList(APIView):

    def get(self, request):
        buy_orders = daily_orders(BuyOrder)
        serializer = BuyOrderGetSerializer(buy_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaleAgentReportList(APIView):

    def get_serializer(self, *args, **kwargs):
        return SaleAgentReportSerializer(*args, **kwargs)

    def get(self, request):
        reports = SaleAgentReport.objects.all().order_by("-id")
        serializer = SaleAgentReportGetSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = SaleAgentReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GivenAgentReportList(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, agent_id):
        reports = SaleAgentReport.objects.filter(sale_agent=agent_id).order_by("-created_date")
        serializer = SaleAgentReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaleAgentReportDetail(APIView):

    def get_serializer(self, *args, **kwargs):
        return SaleAgentReportSerializer(*args, **kwargs)

    def get_object(self, pk):
        try:
            return SaleAgentReport.objects.get(pk=pk)
        except SaleAgentReport.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        agent_report = self.get_object(pk)
        serializer = SaleAgentReportSerializer(agent_report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        agent_report = self.get_object(pk)
        serializer = SaleAgentReportSerializer(agent_report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        agent_report = self.get_object(pk)
        agent_report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfitReport(APIView):

    def get(self, request):
        start_date, end_date = get_dates(request=request)
        total_expense = 0
        total_profit = 0
        expenses = Expense.objects.filter(created_date__range=(start_date, end_date))
        profit_list = Profit.objects.filter(created_date__range=(start_date, end_date))
        for profit in profit_list:
            total_profit += profit.profit
        for expense in expenses:
            total_expense += expense.quantity
        data = {
            "total_profit": total_profit,
            "total_expense": total_expense,
            "net_profit": total_profit-total_expense
        }
        return Response(data, status=status.HTTP_200_OK)


class ClientReport(APIView):

    def get(self, request):
        start_date, end_date = get_dates(request=request)
        days = (end_date - start_date).days
        sell_products = SellOrder.objects.filter(status="delivered", updated_date__range=(start_date, end_date))
        client_list = []
        for sell_product in sell_products:
            if sell_product.client not in client_list:
                client_list.append(sell_product.client)
        data = []
        for client in client_list:
            daily_client_orders = []
            for day in range(days):
                beginning_current_date = start_date + timedelta(days=day)
                ending_current_date = start_date + timedelta(days=day + 1)
                daily_sell_products = sell_products.filter(updated_date__range=(beginning_current_date,
                                                                                ending_current_date),
                                                           client=client)
                total_price = 0
                total_quantity = 0
                for order in daily_sell_products:
                    total_price += order.quantity*order.price
                    total_quantity += order.quantity
                daily_order = {
                    "date": ending_current_date,
                    "total_price": total_price,
                    "total_quantity": total_quantity
                }
                daily_client_orders.append(daily_order)
            ready_data = {
                "client": client.name,
                "product_list": daily_client_orders
            }
            data.append(ready_data)
        return Response(data, status=status.HTTP_200_OK)


class ClientDateReport(APIView):

    def get(self, request):
        start_date, end_date = get_dates(request=request)
        sell_products = SellOrder.objects.filter(status="delivered", updated_date__range=(start_date, end_date))
        client_list = []
        for sell_product in sell_products:
            if sell_product.client not in client_list:
                client_list.append(sell_product.client)

        date_client_orders = []
        for client in client_list:
            client_orders = sell_products.filter(client=client)
            total_price = 0
            total_quantity = 0
            for order in client_orders:
                total_price += order.price * order.quantity
                total_quantity += order.quantity
            client_orders_data = {
                "client": client.name,
                "total_price": total_price,
                "total_quantity": total_quantity
            }
            date_client_orders.append(client_orders_data)
        return Response(date_client_orders, status=status.HTTP_200_OK)


class WarehouseList(APIView):

    def get(self, request):
        term = get_search_query(request)
        items = Warehouse.objects.all().order_by("-updated_date")
        if term:
            items = Warehouse.objects.filter(Q(product__provider__name__icontains=term) |
                                             Q(product__name__icontains=term))
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = DirectorWarehouseSerializer(result_page, many=True)
        paginator_response = paginator.get_paginated_response(result_page).data
        return Response({"count": paginator_response["count"],
                         "next": paginator_response["next"],
                         "previous": paginator_response["previous"],
                         "warehouse_objects": serializer.data}, status=status.HTTP_200_OK)


class ProfitDelete(APIView):

    def delete(self, request, pk):
        profits = Profit.objects.filter(sell_order=pk)
        for profit in profits:
            profit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupedAgentReport(APIView):

    def get(self, request):
        start_date, end_date = get_dates(request=request)
        agents = User.objects.filter(role="agent")
        agent_grouped_list = []
        for agent in agents:
            sell_orders = SellOrder.objects.filter(updated_date__range=(start_date, end_date),
                                                   client__sale_agent=agent, status="delivered")
            total_quantity = 0
            total_price = 0
            for sell_order in sell_orders:
                total_price += sell_order.quantity * sell_order.price
                total_quantity += sell_order.quantity
            data = {
                "agent": agent.first_name + " " + agent.last_name,
                "total_quantity": total_quantity,
                "total_price": total_price
            }
            agent_grouped_list.append(data)
        return Response(agent_grouped_list, status=status.HTTP_200_OK)


class GroupedDateAgentReport(APIView):

    def get(self, request):
        start_date, end_date = get_dates(request=request)
        days = (end_date - start_date).days
        agents = User.objects.filter(role="agent")
        data = []
        for agent in agents:
            sell_products = SellOrder.objects.filter(client__sale_agent=agent, status="delivered")
            daily_agent_orders = []
            for day in range(days):
                beginning_current_date = start_date + timedelta(days=day)
                ending_current_date = start_date + timedelta(days=day + 1)
                daily_sell_products = sell_products.filter(updated_date__range=(beginning_current_date,
                                                                                ending_current_date))
                total_price = 0
                total_quantity = 0
                for order in daily_sell_products:
                    total_price += order.price * order.quantity
                    total_quantity += order.quantity
                agent_order_data = {
                    "date": ending_current_date,
                    "total_price": total_price,
                    "total_quantity": total_quantity
                }
                daily_agent_orders.append(agent_order_data)
            ready_data = {
                "agent": agent.first_name+" "+agent.first_name,
                "product_list": daily_agent_orders
            }
            data.append(ready_data)
        return Response(data, status=status.HTTP_200_OK)
