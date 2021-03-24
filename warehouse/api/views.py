from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from report.api.serializers import DirectorWarehouseSerializer
from warehouse.models import Warehouse
from warehouse.api.serializers import *

# filter by quantity and name


def get_search_params(request):
    param = request.query_params
    name = param.get("name", '')
    start_quantity = param.get("start_quantity", 0)
    end_quantity = param.get("end_quantity", False)
    if not start_quantity: start_quantity=0
    if not end_quantity: end_quantity = 99999999
    return name, start_quantity, end_quantity


class WarehouseList(APIView):

    def get(self, request):
        name, start_quantity, end_quantity = get_search_params(request)
        products = Warehouse.objects.filter(product__name__icontains=name, quantity__gte=start_quantity,
                                            quantity__lte=end_quantity)
        serializer = DirectorWarehouseSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
