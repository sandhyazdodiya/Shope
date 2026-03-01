from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from my_app.models import Item
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


# # Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class Items(View):
    def get(self, request, *args, **kwargs):
        items = Item.objects.all().values()
        return JsonResponse(list(items), content_type="application/json", safe=False)

    def post(self, request, *args, **kwargs):
        item = json.loads(request.body)
        print("request", request.body, type(request.body))
        print("item", item, type(item))
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





