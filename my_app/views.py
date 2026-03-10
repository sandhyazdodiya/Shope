from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from my_app.models import Item, AuthToken
import json, secrets, jwt, datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import Project, Employee
from django.db import connection
from django.core.paginator import Paginator



# # Create your views here.

class Items(View):
    def get(self, request, *args, **kwargs):
        # items = Item.objects.all().values()
        # return JsonResponse(list(items), content_type="application/json", safe=False)

        # page = int(request.GET.get("page", 1))
        # page_size = int(request.GET.get("size", 10))

        # start_index = (page -1) * page_size 
        # end_index = start_index + page_size
        # items = Item.objects.all().values()[start_index:end_index]
        # return JsonResponse(
        #     {
        #         "page" : page,
        #         "page_size" : page_size,
        #         "total" : Item.objects.count(),
        #         "items" : list(items)
        #     },
        #     content_type = "application/json", safe=False
        # )

        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        all_items = Item.objects.all().values()
        paginator = Paginator(all_items, page_size)
        items_page = paginator.get_page(page)
        return JsonResponse(
            {
                "page" : page,
                "page_size" : page_size,
                "total_pages" : paginator.num_pages,
                "total_item" : paginator.count,
                "items" : list(items_page),

            },
        content_type="application/json", safe=False)


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


# curl --location --request GET 'http://localhost:8000/my_app/items/?page=2&size=10' \
# --header 'X-CSRFToken: z1zUXKqmNBgVevR5QzGvWgBEUwvK4vy2yxycsV6a3YIUkjqeA0UUAB4c7HGhnLNJ' \
# --header 'sessionid: wiu5y8uy7vxsm6t7ujuf5skl2w2qrok5' \
# --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6InVkYXkiLCJleHAiOjE3NzMxNDY0ODYsImlhdCI6MTc3MzEzOTI4Nn0.Mnfv2-afOE8vUM-ItHLFMLg3jW9wU0bPbvPcA-oMzrI' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: csrftoken=9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
# --data-raw '{
#     "username" : "uday",
#     "password" : "Sandhya@0506"

# }'

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
# X-CSRFToken - <csrftoken>
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

def token_login_api(request):

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        user = authenticate(username=username, password=password)

        if not user:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        token = secrets.token_hex(32)

        AuthToken.objects.create(user=user, token=token)

        return JsonResponse({"token": token})

def token_logout_api(request):
    # auth_header = request.headers.get("Authorization")
    # token = auth_header.split(" ")[1]

    # AuthToken.objects.filter(token=token).delete()

    # return JsonResponse({"message": "Logged out successfully"}) 

    logout(request)  # deletes session
    return JsonResponse({"message": "Logged out successfully"})


def jwt_login_api(request):

    if request.method == "POST":

        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.datetime.now() + datetime.timedelta(hours=2),
            "iat": datetime.datetime.now()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return JsonResponse({ "message": "Login successful", "token": token })



# JWT Authentication
# curl --location 'http://localhost:8000/my_app/items/' \
# --header 'X-CSRFToken: 9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
# --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6InVkYXkiLCJleHAiOjE3NzI3MjcwMjcsImlhdCI6MTc3MjcxOTgyN30.uPGjw40aNqUw7JX0JftlT3qk4DM_DFpAX6ye_GfoaiA' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: csrftoken=9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
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

def jwt_logout_api(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})


class Employees(View):
    # def get(self, *args, **kwargs):
        # get department name for each employee
        # employees = Employee.objects.all()
        # print("all employees", employees)
        # emp_dep = []
        # for emp in employees:
        #     print("emp", emp.name)
        #     print("department", emp.department.name)
        #     emp_dep.append([emp.name, emp.department.name])
        # print(connection.queries)
        # return JsonResponse({"data": list(connection.queries)}, status=200)

        # def get(self, *args, **kwargs):
        #     # get department name for each employee using select_related
        #     employees = Employee.objects.select_related('department')
        #     print("all employees", employees)
        #     emp_dep = []
        #     for emp in employees:
        #         print("emp", emp.name)
        #         print("department", emp.department.name)
        #         emp_dep.append([emp.name, emp.department.name])
        #     print(connection.queries)
        #     return JsonResponse({"data": list(connection.queries)}, status=200)

        def get(self, *args, **kwargs):
            # Prefetches all employees working on those projects
            projects = Project.objects.prefetch_related('employees')
            print("all projects", projects)
            proj_emp = []
            for project in projects:
                emps = []
                for emp in project.employees.all():
                    emps.append(emp.name)
                proj_emp.append([project.name, emps])
            print(connection.queries)
            return JsonResponse({"data": list(connection.queries)}, status=200)


        # def get(self, *args, **kwargs):
        #     # Prefetches all employees working on those projects
        #     projects = Project.objects.all()
        #     print("all projects", projects)
        #     proj_emp = []
        #     for project in projects:
        #         emps = []
        #         for emp in project.employees.all():
        #             emps.append(emp.name)
        #         proj_emp.append([project.name, emps])
        #     print(connection.queries)
        #     return JsonResponse({"data": list(connection.queries)}, status=200)


