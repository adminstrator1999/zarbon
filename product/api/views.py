from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings

from expense_discount.api.serializers import DiscountGetSerializer, DiscountProductGetSerializer
from user.permissions import IsCEO, IsDirector
from product.api.serializers import ProductSerializer, CategorySerializer, CategoryProductSerializer, \
    ProductDiscountSerializer, ProductGetSerializer
from product.models import Product, Category
from warehouse.models import Warehouse
from expense_discount.models import Discount


class CategoryList(APIView):

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        return CategorySerializer(*args, **kwargs)

    def get(self, request):
        categories = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CategoryList(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


class CategoryDetail(APIView):

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductList(APIView):

    """Giving permission to change or see according the users role"""
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsDirector, IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        return ProductSerializer(*args, **kwargs)

    def get(self, request):
        products = Product.objects.all().order_by("-id")
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductGetSerializer(result_page, many=True)
        paginator_response = paginator.get_paginated_response(result_page).data
        return Response({
                        "count": paginator_response["count"],
                        "next": paginator_response["next"],
                        "previous": paginator_response["previous"],
                        "products": serializer.data}, status=status.HTTP_200_OK)

    """Creates a product"""
    def post(self, request):
        serializers = ProductSerializer(data=request.data)
        if serializers.is_valid():
            # updating creating warehouse accordingly
            product_data = serializers.validated_data
            serializers.save()
            product = Product.objects.get(**product_data)
            Warehouse.objects.create(product=product)

            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListNoPagination(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductGetSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetail(APIView):
    """Giving permission to change or see according the users role"""
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated, IsCEO]

    def get_serializer(self, *args, **kwargs):
        return ProductSerializer(*args, **kwargs)

    def get_discount(self, product):
        try:
            discounts = product.discount_set.filter(product=product, active=True)
            discount_list = []
            for discount in discounts:
                serializer = DiscountProductGetSerializer(discount)
                discount_list.append(serializer.data)
            return discount_list
        except Discount.DoesNotExist:
            return 0

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductGetSerializer(product)
        return Response({"product": serializer.data,
                        "discount": self.get_discount(product)},
                        status=status.HTTP_200_OK)

    # Updates the product
    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductGetSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryProductList(APIView):

    def get(self, request, category_id):
        products = Product.objects.filter(category=category_id)
        # id, product_name, product_unit, product_type, quantity, provider_name, last_update
        product_list = []
        for product in products:
            data = {"id": product.id,
                    "name": product.name,
                    "unit": product.unit,
                    "product_type": product.product_type,
                    "quantity": product.warehouse_set.get(product=product).quantity,
                    "provider": product.provider.name,
                    "last_update": product.warehouse_set.get(product=product).updated_date,
                    }
            serializer = ProductDiscountSerializer(data)
            product_list.append(serializer.data)

        return Response(product_list, status=status.HTTP_200_OK)
