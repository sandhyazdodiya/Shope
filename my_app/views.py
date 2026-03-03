from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from my_app.models import Item
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.middleware.csrf import get_token


# # Create your views here.

class Items(View):
    def get(self, request, *args, **kwargs):
        items = Item.objects.all().values()
        return JsonResponse(list(items), content_type="application/json", safe=False)

    def post(self, request, *args, **kwargs):
        item = json.loads(request.body)
        item = Item.objects.create(**item)
        item.save()
        return JsonResponse({"status": "Created Successfully"}, status=201)

    def patch(self, request, item_id, *args, **kwargs):
        item = json.loads(request.body)
        item = Item.objects.filter(id=item_id).update(**item)
        return JsonResponse({"status": "Updated Successfully"}, status=200)

    def delete(self, request, item_id, *args, **kwargs):
        item = Item.objects.filter(id=Item_id).delete()
        return JsonResponse({"status": "Deleted Successfully"}, status=200)


class ItemsUsingSerializer(View):

    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        items = serializers.serialize("json", items) # converts queryset into a json string
        items = json.loads(items) # converts json string to python object dict, or list
        return JsonResponse(items, content_type="application/json", safe=False)
      

def csrf_token_api(request):
    return JsonResponse({"csrfToken": get_token(request)})





