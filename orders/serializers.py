from .models import ProductCopy
from rest_framework import serializers


class ProductCopySerializer(serializers.ModelSerializer):
    # status = ChoiceField(choices=ORDER_STATUS)
    # type_of_order = ChoiceField(choices=DELIVERY_TYPE)
    # status = serializers.StringRelatedField(many=True)

    image = serializers.ImageField(max_length=None,
                                   use_url=True,
                                   allow_null=True,
                                   required=False)

    class Meta:
        model = ProductCopy
        depth = 2
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