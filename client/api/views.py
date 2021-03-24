from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from client.models import Client, AgentClientReport
from client.api.serializers import ClientSerializer, ClientGetSerializer, AgentClientReportSerializer,\
     AgentClientReportGetSerializer


class AgentClientReportList(APIView):

    def get_serializer(self, *args, **kwargs):
        return AgentClientReportSerializer(*args, **kwargs)

    def get(self, request):
        clients = AgentClientReport.objects.all().order_by("-id")
        serializer = AgentClientReportGetSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = AgentClientReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentClientReportDetail(APIView):

    def get_serializer(self, *args, **kwargs):
        return AgentClientReportSerializer(*args, **kwargs)

    def get_object(self, pk):
        try:
            return AgentClientReport.objects.get(pk=pk)
        except AgentClientReport.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        client = self.get_object(pk)
        serializer = AgentClientReportGetSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = self.get_object(pk=pk)
        data = request.data
        serializer = AgentClientReportSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientList(APIView):

    def get_serializer(self, *args, **kwargs):
        return ClientSerializer(*args, **kwargs)

    def get(self, request):
        clients = Client.objects.all().order_by("-id")
        serializer = ClientGetSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetail(APIView):

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


