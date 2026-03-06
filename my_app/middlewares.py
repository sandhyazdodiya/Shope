from django.http import JsonResponse
from .models import AuthToken
import jwt, json
from django.conf import settings
from django.contrib.auth.models import User

class TokenAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_urls = ["/my_app/token_login_api", "/my_app/csrf_token"]
    
        if request.path not in public_urls:

            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return JsonResponse({"error": "Authorization token is required"}, status=401)

            if auth_header and auth_header.startswith("Bearer "):

                token = auth_header.split(" ")[1]

                try:
                    token_obj = AuthToken.objects.get(token=token)
                    request.user = token_obj.user

                except AuthToken.DoesNotExist:
                    return JsonResponse({"error": "Invalid token"}, status=401)

        response = self.get_response(request)

        return response

# Token Authentication
# Get CSRF

# curl --location --request GET 'http://localhost:8000/my_app/csrf_token' \
# --header 'Referrer-Policy: same-origin' \
# --header 'Cross-Origin-Opener-Policy: same-origin' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: csrftoken=9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
# --data-raw '{
#     "username" : "uday",
#     "password" : "Sandhya@0506"

# }'

# -Login
# curl --location 'http://localhost:8000/my_app/token_login_api' \
# --header 'X-CSRFToken: 9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
# --header 'sessionid: wiu5y8uy7vxsm6t7ujuf5skl2w2qrok5' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: csrftoken=9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
# --data-raw '{
#     "username" : "uday",
#     "password" : "Sandhya@0506"

# }'

# - Send token in request
# curl --location 'http://localhost:8000/my_app/items/' \
# --header 'X-CSRFToken: 9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
# --header 'Authorization: Bearer be895d532776c4c09c2422a7fbb318f1f6b7c4d8186f51c12a7bd7db00251e00' \
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

# Logout
# curl --location 'http://localhost:8000/my_app/token_logout_api' \
# --header 'X-CSRFToken: 9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
# --header 'Authorization: Bearer be895d532776c4c09c2422a7fbb318f1f6b7c4d8186f51c12a7bd7db00251e00' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: csrftoken=9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
# --data-raw '{
#     "username" : "uday",
#     "password" : "Sandhya@0506"

# }'



class JWTAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        public_urls = ["/my_app/jwt_login_api", "/my_app/csrf_token"]

        if request.path not in public_urls:

            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return JsonResponse({"error": "JWT token is required"}, status=401)

            if not auth_header.startswith("Bearer "):
                return JsonResponse({"error": "Invalid Authorization header"}, status=401)

            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

                user = User.objects.get(id=payload["user_id"])
                request.user = user

            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token expired"}, status=401)

            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)

        # IMPORTANT: always call next middleware/view
        response = self.get_response(request)

        return response

# curl --location 'http://localhost:8000/my_app/jwt_login_api' \
# --header 'X-CSRFToken: 9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
# --header 'sessionid: wiu5y8uy7vxsm6t7ujuf5skl2w2qrok5' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: csrftoken=9G9sFlQYqxC9gYJjUBozOvDInllHtqpR' \
# --data-raw '{
#     "username" : "uday",
#     "password" : "Sandhya@0506"

# }'

# curl --location 'http://localhost:8000/my_app/items/' \
# --header 'X-CSRFToken: KNhXLzZrVe2kdBrbBhYbVVsJGfZto4A1JjgfgKFfbBujjp0klIcAzgVhTqa0HkPI' \
# --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6InVkYXkiLCJleHAiOjE3NzI3ODkzNTcsImlhdCI6MTc3Mjc4MjE1N30.ywmFsCzekAj0YfEF-VB4AtaF5LmjzRt_gpRHZDMsjKo' \
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


 