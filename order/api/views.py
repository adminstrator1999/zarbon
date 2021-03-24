from django.db import transaction
from django.db.models import Q
from django.http import Http404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from decimal import Decimal
from django.conf import settings
from datetime import timedelta, datetime
from django.utils import timezone

from client.models import Client
from order.api.serializers import BuyOrderSerializer, BuyOrderGetSerializer, SellOrderSerializer, \
    SellOrderGetSerializer, BuyOrderPaymentSerializer, SellOrderPaymentSerializer, FailedProviderProductSerializer, \
    FailedProviderProductGetSerializer, FailedClientProductSerializer, FailedClientProductGetSerializer, \
    AgentSellOrderSerializer, ClientSellOrderSerializer, SellOrderPaymentGetSerializer, BuyOrderPaymentGetSerializer
from order.models import BuyOrder, SellOrder, BuyOrderPayment, SellOrderPayment, FailedClientProduct, \
    FailedProviderProduct
from plan.models import Plan, AgentPlan, PlanItem
from report.models import Profit
from warehouse.models import Warehouse
from report.api.views import date_orders
from product.models import Product


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


class BuyOrderList(APIView):

    def get_serializer(self, *args, **kwargs):
        return BuyOrderSerializer(*args, **kwargs)

    def get(self, request):
        term = get_search_query(request)
        buy_orders = BuyOrder.objects.all().order_by("-id")
        if term:
            buy_orders = buy_orders.filter(Q(product__name__icontains=term) |
                                           Q(product__provider__name__icontains=term) |
                                           Q(product__category__name__icontains=term))
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(buy_orders, request)
        serializer = BuyOrderGetSerializer(result_page, many=True)
        paginator_response = paginator.get_paginated_response(result_page).data
        return Response({
            "count": paginator_response["count"],
            "next": paginator_response["next"],
            "previous": paginator_response["previous"],
            "buy_order_list": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = BuyOrderSerializer(data=data)
        if serializer.is_valid():
            # updating warehouse accordingly
            product = serializer.validated_data['product']
            warehouse, created = Warehouse.objects.get_or_create(product=product)
            warehouse.quantity += Decimal(serializer.validated_data['quantity'])
            warehouse.last_price = Decimal(serializer.validated_data['price'])
            warehouse.save()
            debt = serializer.validated_data['quantity'] * serializer.validated_data['price']
            serializer.validated_data['debt'] = debt
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_dates(request):
    param = request.query_params
    start_date = string_to_date(param.get("start_date", False)) or (timezone.now() - timedelta(days=7)).replace(
        tzinfo=None)
    end_date = string_to_date(param.get("end_date", False)) or (timezone.now()).replace(tzinfo=None)
    return start_date, end_date


def get_grouped_products(request, model):
    """Grouping buy orders into one product at a time"""
    start_date, end_date = get_dates(request=request)
    days = (end_date - start_date).days
    grouped_orders = []
    products = []
    for daily_order in date_orders(model=model, start_date=start_date, end_date=end_date):
        if daily_order.product not in products:
            products.append(daily_order.product)

    for product in products:
        grouped_product = []

        for day in range(days):
            beginning_current_date = start_date + timedelta(days=day)
            ending_current_date = start_date + timedelta(days=day + 1)
            daily_orders = date_orders(model=model, start_date=beginning_current_date,
                                       end_date=ending_current_date).filter(product=product)
            total_quantity = 0
            total_price = 0
            for daily_order in daily_orders:
                total_quantity += daily_order.quantity
                total_price += daily_order.quantity * daily_order.price
            data = {
                "date": ending_current_date,
                "total_quantity": total_quantity,
                "total_price": total_price,
            }
            grouped_product.append(data)
        ready_data = {
            "product_name": product.name,
            "product_list": grouped_product
        }
        grouped_orders.append(ready_data)
    return grouped_orders


def get_grouped_date_products(request, model):
    """Grouping buy orders into one product at a time"""
    start_date, end_date = get_dates(request=request)
    orders = date_orders(model=model, start_date=start_date, end_date=end_date)
    grouped_order_list = []
    products = []
    for order in orders:
        if order.product not in products:
            products.append(order.product)
    for product in products:
        grouped_orders = orders.filter(product=product)
        total_quantity = 0
        total_cost = 0
        for grouped_order in grouped_orders:
            total_quantity += grouped_order.quantity
            total_cost += grouped_order.price * grouped_order.quantity
        data = {
            "product_name": product.name,
            "total_quantity": total_quantity,
            "total_cost": total_cost
        }
        grouped_order_list.append(data)
    return grouped_order_list


class BuyOrderGroupedList(APIView):

    def get(self, request):
        grouped_orders = get_grouped_products(request=request, model=BuyOrder)
        return Response(grouped_orders, status=status.HTTP_200_OK)


class BuyOrderDateGroupedList(APIView):

    def get(self, request):
        grouped_order_list = get_grouped_date_products(request=request, model=BuyOrder)
        return Response(grouped_order_list, status=status.HTTP_200_OK)


class BuyOrderDetail(APIView):
    """Getting the BuyOrder object and updating, retrieving, deleting the object"""

    def get_serializer(self, *args, **kwargs):
        return BuyOrderSerializer(*args, **kwargs)

    def get_object(self, pk):
        try:
            return BuyOrder.objects.get(pk=pk)
        except BuyOrder.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = BuyOrderGetSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = BuyOrderSerializer(item, data=request.data)
        if serializer.is_valid():
            get_serializer = BuyOrderGetSerializer(serializer.validated_data)
            quantity_gap = serializer.validated_data["quantity"] - item.quantity
            product = serializer.validated_data['product']
            warehouse = Warehouse.objects.get(product=product)
            warehouse.quantity += quantity_gap
            warehouse.save()
            serializer.save()
            return Response(get_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        product = item.product
        warehouse = Warehouse.objects.get(product=product)
        warehouse.quantity -= item.quantity
        warehouse.save()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuyOrderPaymentList(APIView):

    def get_serializer(self, *args, **kwargs):
        return BuyOrderPaymentSerializer(*args, **kwargs)

    def get(self, request):
        payments = BuyOrderPayment.objects.all().order_by("-id")
        serializer = BuyOrderPaymentGetSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BuyOrderPaymentSerializer(data=request.data, many=True)
        if serializer.is_valid():
            buy_order = serializer.validated_data[0]['buy_order']
            total_payment = 0
            for buy_order_payment in serializer.validated_data:
                payment = buy_order_payment['payment']
                total_payment += payment
            # TODO do i have to check if debt <= payment
            buy_order.debt -= total_payment
            buy_order.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetBuyOrderPaymentList(APIView):

    def get_object(self, order_id):
        try:
            return BuyOrder.objects.get(id=order_id)
        except BuyOrder.DoesNotExist:
            raise Http404

    def get(self, request, order_id):
        buy_order = self.get_object(order_id)
        payments = buy_order.buyorderpayment_set.filter(buy_order=buy_order)
        serializer = BuyOrderPaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BuyOrderPaymentDetail(APIView):

    def get_object(self, pk):
        try:
            return BuyOrderPayment.objects.get(pk=pk)
        except BuyOrderPayment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = BuyOrderPaymentSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = BuyOrderPaymentSerializer(item, data=request.data)
        if serializer.is_valid():
            payment = serializer.validated_data.get("payment")
            payment_gap = payment - item.payment
            buy_order = item.buy_order
            buy_order.debt -= payment_gap
            buy_order.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        buy_order = item.buy_order
        buy_order.debt += item.payment
        buy_order.save()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SellOrderList(APIView):

    def get_serializer(self, *args, **kwargs):
        return SellOrderSerializer(*args, **kwargs)

    def get(self, request):
        term = get_search_query(request)
        sell_orders = SellOrder.objects.all().order_by("-id")
        if term:
            sell_orders = sell_orders.filter(Q(product__name__icontains=term) |
                                             Q(client__name__icontains=term) |
                                             Q(client__sale_agent__first_name__icontains=term) |
                                             Q(client__sale_agent__last_name__icontains=term))
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(sell_orders, request)
        serializer = SellOrderGetSerializer(result_page, many=True)
        paginator_response = paginator.get_paginated_response(result_page).data
        return Response({"count": paginator_response["count"],
                         "next": paginator_response["next"],
                         "previous": paginator_response["previous"],
                         "sell_order_list": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = SellOrderSerializer(data=data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            sell_orders = SellOrder.objects.filter(product=product)
            ordered_quantity = 0
            for sell_order in sell_orders:
                ordered_quantity += sell_order.quantity
            warehouse_product_quantity = Warehouse.objects.get(product=product).quantity
            if warehouse_product_quantity >= serializer.validated_data['quantity'] + ordered_quantity + Decimal(20.00):
                debt = serializer.validated_data['quantity'] * Decimal(serializer.validated_data['price'])
                serializer.validated_data['debt'] = debt
                serializer.save()
            else:
                error_message = {
                    "error": "Omborda mahsulot yetarli emas"
                }
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientSellOrderList(APIView):

    def get(self, request, client_id):
        orders = SellOrder.objects.filter(client=client_id).order_by("-updated_date")
        serializer = ClientSellOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SellOrderGroupedList(APIView):

    def get(self, request):
        grouped_orders = get_grouped_products(request=request, model=SellOrder)
        return Response(grouped_orders, status=status.HTTP_200_OK)


class SellOrderDateGroupedList(APIView):

    def get(self, request):
        grouped_orders = get_grouped_date_products(request=request, model=SellOrder)
        return Response(grouped_orders, status=status.HTTP_200_OK)


class SellOrderDetail(APIView):

    def get_serializer(self, *args, **kwargs):
        return SellOrderSerializer(*args, **kwargs)

    def get_object(self, pk):
        try:
            return SellOrder.objects.get(pk=pk)
        except SellOrder.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = SellOrderGetSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = SellOrderSerializer(item, data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                # updating warehouse accordingly
                product = serializer.validated_data['product']
                quantity = serializer.validated_data.get('quantity')
                price = serializer.validated_data.get('price')
                warehouse = Warehouse.objects.get(product=product)
                if serializer.validated_data['status'] == "delivered":
                    last_price = warehouse.last_price
                    profit = quantity * price - quantity * last_price
                    Profit.objects.create(profit=profit, sell_order=item, last_price=last_price)
                    warehouse.quantity -= quantity
                else:
                    # handle to reverse
                    try:
                        profit = Profit.objects.get(sell_order=item)
                    except Profit.DoesNotExist:
                        raise Http404
                    profit.delete()
                    warehouse.quantity += quantity

                warehouse.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        product = item.product
        warehouse = Warehouse.objects.get(product=product)
        warehouse.quantity += item.quantity
        warehouse.save()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SellOrderPaymentList(APIView):

    def get_serializer(self, *args, **kwargs):
        return SellOrderPaymentSerializer(*args, **kwargs)

    def get(self, request):
        payments = SellOrderPayment.objects.all().order_by("-id")
        serializer = SellOrderPaymentGetSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SellOrderPaymentSerializer(data=request.data, many=True)
        if serializer.is_valid():
            sell_order = serializer.validated_data[0]['sell_order']
            total_payment = 0
            for sell_order_payment in serializer.validated_data:
                payment = sell_order_payment['payment']
                total_payment += payment
            # TODO do i have to check if debt <= payment
            sell_order.debt -= total_payment
            sell_order.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellOrderPaymentDetail(APIView):

    def get_object(self, pk):
        try:
            return SellOrderPayment.objects.get(pk=pk)
        except SellOrderPayment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = SellOrderPaymentSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = SellOrderPaymentSerializer(item, data=request.data)
        if serializer.is_valid():
            payment = serializer.validated_data.get("payment")
            payment_gap = payment - item.payment
            sell_order = item.sell_order
            sell_order.debt -= payment_gap
            sell_order.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        sell_order = item.sell_order
        sell_order.debt += item.payment
        sell_order.save()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProviderFailedProductList(APIView):

    def get_serializer(self, *args, **kwargs):
        return FailedProviderProductSerializer(*args, **kwargs)

    def get(self, request):
        items = FailedProviderProduct.objects.all()
        serializer = FailedProviderProductGetSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FailedProviderProductSerializer(data=request.data)
        if serializer.is_valid():
            buy_order = serializer.validated_data.get('buy_order')
            product = buy_order.product
            returned_quantity = serializer.validated_data.get('returned_quantity')
            warehouse = Warehouse.objects.get(product=product)
            warehouse.quantity -= returned_quantity
            warehouse.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderFailedProductDetail(APIView):

    def get_serializer(self, *args, **kwargs):
        return FailedProviderProductSerializer(*args, **kwargs)

    def get_object(self, pk):
        try:
            return FailedProviderProduct.objects.get(pk=pk)
        except FailedProviderProduct.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        failed_product = self.get_object(pk)
        serializer = FailedProviderProductGetSerializer(failed_product)
        return Response(serializer.data)

    def put(self, request, pk):
        failed_product = self.get_object(pk)
        data = request.data
        serializer = FailedProviderProductSerializer(failed_product, data=data)
        if serializer.is_valid():
            quantity_gap = serializer.validated_data["returned_quantity"] - failed_product.returned_quantity
            warehouse = Warehouse.objects.get(product=failed_product.buy_order.product)
            warehouse.quantity -= quantity_gap
            warehouse.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        failed_order = self.get_object(pk)
        warehouse = Warehouse.objects.get(product=failed_order.buy_order.product)
        warehouse.quantity += failed_order.returned_quantity
        warehouse.save()
        failed_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientFailedProductList(APIView):

    def get_serializer(self, *args, **kwargs):
        return FailedClientProductSerializer(*args, **kwargs)

    def get(self, request):
        items = FailedClientProduct.objects.all()
        serializer = FailedClientProductGetSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = FailedClientProductSerializer(data=data)
        if serializer.is_valid():
            sell_order = serializer.validated_data.get('sell_order')
            product = sell_order.product
            price = sell_order.price
            returned_quantity = serializer.validated_data.get('returned_quantity')
            failed_status = serializer.validated_data.get('failed_status')
            profit = Profit.objects.get(sell_order=sell_order)
            if failed_status == "valid":
                warehouse = Warehouse.objects.get(product=product)
                warehouse.quantity += returned_quantity
                warehouse.save()
            profit.profit -= returned_quantity * (price - profit.last_price)
            profit.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientFailedProductDetail(APIView):

    def get_serializer(self, *args, **kwargs):
        return FailedClientProductSerializer(*args, **kwargs)

    def get_object(self, pk):
        try:
            return FailedClientProduct.objects.get(pk=pk)
        except FailedClientProduct.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = FailedProviderProductGetSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = self.get_object(pk)
        data = request.data
        serializer = FailedClientProductSerializer(instance, data=data)
        if serializer.is_valid():
            sell_order = instance.sell_order
            profit = Profit.objects.get(sell_order=sell_order)
            warehouse = Warehouse.objects.get(product=sell_order.product)
            failed_status = data.get("failed_status")
            quantity_gap = instance.returned_quantity - data.get("returned_quantity")

            if instance.failed_status != failed_status and failed_status == "valid":
                warehouse.quantity += data.get("returned_quantity")
            elif instance.failed_status != failed_status and failed_status == "invalid":
                warehouse.quantity -= data.get("returned_quantity")
            profit.profit += quantity_gap*(sell_order.price-profit.last_price)
            profit.save()
            warehouse.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        sell_order = instance.sell_order
        warehouse = Warehouse.objects.get(product=sell_order.product)
        profit = Profit.objects.get(sell_order=sell_order)
        if instance.failed_status == "valid":
            warehouse.quantity -= instance.returned_quantity
            warehouse.save()
        profit.profit -= instance.returned_quantity*(sell_order.price-profit.last_price)
        profit.save()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AgentSellOrder(APIView):
    # product_name, sell_order_status, quantity, price, client, created_date
    def get(self, request, agent_id):
        agent_sell_orders = SellOrder.objects.filter(client__sale_agent_id=agent_id).order_by("-created_date")
        data = []
        for agent_sell_order in agent_sell_orders:
            sell_order = {
                "product_name": agent_sell_order.product.name,
                "status": agent_sell_order.status,
                "quantity": agent_sell_order.quantity,
                "price": agent_sell_order.price,
                "client": agent_sell_order.client.name,
                "created_date": agent_sell_order.created_date
            }
            data.append(sell_order)
        serializer = AgentSellOrderSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# we are taking profit report here
class ProfitReport(APIView):

    def get(self, request):
        start_date, end_date = get_dates(request=request)
        days = (end_date - start_date).days
        products = []
        for profit in Profit.objects.filter(created_date__gt=start_date, created_date__lt=end_date):
            if profit.sell_order.product not in products:
                products.append(profit.sell_order.product)

        grouped_profit = []
        for product in products:
            product_list = []
            for day in range(days):
                beginning_current_date = start_date + timedelta(days=day)
                ending_current_date = start_date + timedelta(days=day+1)
                whole_daily_profit_list = Profit.objects.filter(created_date__gt=beginning_current_date,
                                                                created_date__lt=ending_current_date)
                daily_profit_list = Profit.objects.filter(created_date__gt=beginning_current_date,
                                                          created_date__lt=ending_current_date).filter(
                    sell_order__product=product)
                daily_total_profit = 0
                for obj in whole_daily_profit_list:
                    daily_total_profit += obj.profit
                product_profit = 0
                for daily_profit in daily_profit_list:
                    product_profit += daily_profit.profit
                data = {
                    "date": ending_current_date,
                    "product_profit": product_profit,
                    "daily_total_profit": daily_total_profit
                }
                product_list.append(data)
            ready_data = {
                "product_name": product.name,
                "product_list": product_list
            }
            grouped_profit.append(ready_data)
        return Response(grouped_profit, status=status.HTTP_200_OK)


def get_grouped_date_profit(request):
    start_date, end_date = get_dates(request=request)
    profit_list = Profit.objects.filter(created_date__gt=start_date, created_date__lt=end_date)
    grouped_profit_list = []
    products = []
    for item in profit_list:
        if item.sell_order.product not in products:
            products.append(item.sell_order.product)
    for product in products:
        grouped_profit = profit_list.filter(sell_order__product=product)
        total_profit = 0
        for obj in grouped_profit:
            total_profit += obj.profit
        data = {
            "product_name": product.name,
            "total_profit": total_profit
        }
        grouped_profit_list.append(data)
    return grouped_profit_list


class ProfitGroupReport(APIView):

    def get(self, request):
        grouped_profit_list = get_grouped_date_profit(request=request)
        return Response(grouped_profit_list, status=status.HTTP_200_OK)


class DailyProfit(APIView):

    def get(self, request):
        start_date, end_date = get_dates(request=request)
        days = (end_date - start_date).days
        daily_total_profit = []
        for day in range(days):
            beginning_current_date = start_date + timedelta(days=day)
            ending_current_date = start_date + timedelta(days=day+1)
            whole_daily_profit_list = Profit.objects.filter(created_date__gt=beginning_current_date,
                                                            created_date__lt=ending_current_date)
            total_profit = 0
            for profit in whole_daily_profit_list:
                total_profit += profit.profit
            data = {
                "date": ending_current_date,
                "total_profit": total_profit
            }
            daily_total_profit.append(data)
        return Response(daily_total_profit, status=status.HTTP_200_OK)
