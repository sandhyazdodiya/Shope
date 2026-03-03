from rest_framework import serializers
from my_app.models import Item


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class ItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    price = serializers.FloatField()
    discount_price = serializers.FloatField(required=False, allow_null=True)
    category = serializers.ChoiceField(choices=CATEGORY_CHOICES)
    label = serializers.ChoiceField(choices=LABEL_CHOICES)
    slug = serializers.SlugField()
    description = serializers.CharField()
    image = serializers.ImageField(required=False, allow_null=True)


    def create(self, validated_data):
        """
        Create and return a new `Item` instance, given the validated data.
        """
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Item` instance, given the validated data.
        """
        # If PUT: DRF validation ensures all fields are in validated_data.
        # If PATCH: validated_data only contains what you sent.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# curl --location --request PUT 'http://localhost:8000/drf_my_app/items/2/' \
# --header 'Accept: */*' \
# --header 'Accept-Language: en-IN,en;q=0.9' \
# --header 'Connection: keep-alive' \
# --header 'Origin: http://localhost:3001' \
# --header 'Referer: http://localhost:3001/' \
# --header 'Sec-Fetch-Dest: empty' \
# --header 'Sec-Fetch-Mode: cors' \
# --header 'Sec-Fetch-Site: same-site' \
# --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36' \
# --header 'sec-ch-ua: "Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"' \
# --header 'sec-ch-ua-mobile: ?0' \
# --header 'sec-ch-ua-platform: "Linux"' \
# --header 'X-CSRFToken: n7xYGc042JW92IhGjfaYPXVf2Pg3USB16L0nMiiUQcPvFj5QOkOMAAAZYVHg0lld' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: csrftoken=TODzggs0YD3wNLYkFfOYVNPU6gBngDUm' \
# --data '{"title": "New Title"}'



# curl --location --request PATCH 'http://localhost:8000/drf_my_app/items/2/' \
# --header 'Accept: */*' \
# --header 'Accept-Language: en-IN,en;q=0.9' \
# --header 'Connection: keep-alive' \
# --header 'Origin: http://localhost:3001' \
# --header 'Referer: http://localhost:3001/' \
# --header 'Sec-Fetch-Dest: empty' \
# --header 'Sec-Fetch-Mode: cors' \
# --header 'Sec-Fetch-Site: same-site' \
# --header 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36' \
# --header 'sec-ch-ua: "Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"' \
# --header 'sec-ch-ua-mobile: ?0' \
# --header 'sec-ch-ua-platform: "Linux"' \
# --header 'X-CSRFToken: n7xYGc042JW92IhGjfaYPXVf2Pg3USB16L0nMiiUQcPvFj5QOkOMAAAZYVHg0lld' \
# --header 'Content-Type: application/json' \
# --header 'Cookie: csrftoken=TODzggs0YD3wNLYkFfOYVNPU6gBngDUm' \
# --data '{"title": "New Title"}'


class ItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
