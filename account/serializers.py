from .models import Address
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        depth = 1
        fields = '__all__'
        # fields = ['id', ]
        # ordering_fields = "__all__"
        # ordering = (
        #     "number",
        # )

    # def get_photo_url(self, product):
    #     request = self.context.get('request')
    #     image_url = product.image
    #     return request.build_absolute_uri(image_url)