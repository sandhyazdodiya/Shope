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
from django.contrib.auth import authenticate, login, logout


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
        items = serializers.serialize("json", items)
        items = json.loads(items)
        return JsonResponse(items, content_type="application/json", safe=False)

    def post(self, request, *args, **kwargs):
        item  = serializers.serialize("json", request.body)
        item = json.loads(item)
        item = Item.objects.create(**item)
        item.save()
        return JsonResponse(item, content_type="application/json", safe=False)

def csrf_token_api(request):
    return JsonResponse({"csrfToken": get_token(request)})

def session_login_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        login(request, user)  # creates session

        return JsonResponse({"message": "Login successful"})

def session_logout_api(request):
    logout(request)  # deletes session
    return JsonResponse({"message": "Logged out successfully"})


# Session Authentication 

# Get Authentication 

# curl --location --request GET 'http://localhost:8000/my_app/csrf_token' \
# --header 'Referrer-Policy: same-origin' \
# --header 'Cross-Origin-Opener-Policy: same-origin' \
# --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcyNjMyNDkxLCJpYXQiOjE3NzI2MzIxOTEsImp0aSI6ImYwZjdjYTk4ODIxZTQwZjc4MGJkMTU1MjRlOGQ4YzE2IiwidXNlcl9pZCI6IjIifQ.jyd1tbU25LLD2zbbDhztISjwfbSeX2qNNhSwDhhVUAI' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: csrftoken=Dc1WcHYl0G36BgvwHLeN9LNxMG71ntmb' \
# --data-raw '{
#     "username" : "uday",
#     "password" : "Sandhya@0506"

# }'

# Login 

# curl --location 'http://localhost:8000/my_app/session_login_api' \
# --header 'Content-Type: application/json' \
# --header 'X-CSRFToken: wKosdeu7ffNHLCMxAK6VYGo6JebSCHR2ZMfefLii5LGDcI7T7layXh1tlK8JP033' \
# --header 'Cookie: csrftoken=RYFxqRs8ELgLNtrQlwD8OuKerldcPCmf; sessionid=wiu5y8uy7vxsm6t7ujuf5skl2w2qrok5' \
# --data-raw '{
#     "username": "uday",
#     "password": "Sandhya@0506"
# }'

# Create 

# curl --location 'http://localhost:8000/my_app/items/' \
# --header 'X-CSRFToken: RYFxqRs8ELgLNtrQlwD8OuKerldcPCmf' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: csrftoken=RYFxqRs8ELgLNtrQlwD8OuKerldcPCmf; sessionid=wiu5y8uy7vxsm6t7ujuf5skl2w2qrok5' \
# --data '    {
#         "title": "Sleeveless Sports Vest",
#         "price": 999.0,
#         "discount_price": 799.0,
#         "category": "SW",
#         "label": "S",
#         "slug": "sleeveless-sports-vest",
#         "description": "Lightweight sleeveless vest for intense workout sessions.",
#         "image": null
#     }'

