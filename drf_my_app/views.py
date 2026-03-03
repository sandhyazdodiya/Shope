from my_app.models import Item
from .serializers import ItemSerializer, ItemModelSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class ItemViewSet(ViewSet):
    """
    ViewSet for listing and creating Items.
    """
    
    # Routers map 'GET' to the 'list' method
    def list(self, request):
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)

    # Routers map 'POST' to the 'create' method
    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # Routers map 'GET/item/_id?' to the 'retrieve' method
    def retrieve(self, request, pk=None):
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    # Routers map 'PUT/item/_id?' to the 'retrieve' method
    def update(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # Routers map 'PATCH/item/_id?' to the 'retrieve' method
    def partial_update(self, request, pk=None):
        # For PATCH requests, you MUST add partial=True
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        item = Item.objects.get(pk=pk).delete()
        return Response(status=204)


class ItemAPIView(APIView):

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)

    def put(self, request, item_id):
        item = Item.objects.get(id=item_id)
        serializer = ItemSerializer(item, request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, item_id):
        item = Item.objects.get(id=item_id)
        serializer = ItemSerializer(item, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, item_id):
        item = Item.objects.get(id=item_id)
        item.delete()
        return Response(status=204)


class ItemModelSerializerView(APIView):

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemModelSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)

    def put(self, request, item_id):
        item = Item.objects.get(id=item_id)
        serializer = ItemModelSerializer(item, request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def patch(self, request, item_id):
        item = Item.objects.get(id=item_id)
        serializer = ItemModelSerializer(item, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, item_id):
        item = Item.objects.get(id=item_id)
        item.delete()
        return Response(status=204)


class ItemModelViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer



