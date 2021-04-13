from .models import ProductCopy
from rest_framework import serializers


class ProductCopySerializer(serializers.ModelSerializer):
    # status = ChoiceField(choices=ORDER_STATUS)
    # type_of_order = ChoiceField(choices=DELIVERY_TYPE)
    # status = serializers.StringRelatedField(many=True)

    class Meta:
        model = ProductCopy
        depth = 2
        fields = '__all__'
        # fields = ['id', ]
        # ordering_fields = "__all__"
        # ordering = (
        #     "number",
        # )
