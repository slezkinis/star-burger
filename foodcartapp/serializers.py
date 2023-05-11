from rest_framework.serializers import ModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField

from .models import Product, Order, OrderElements


class OrderElementsSerializer(ModelSerializer):
    class Meta:
        model = OrderElements
        fields = [
            'product',
            'quantity'
        ]


class OrderSerializer(ModelSerializer):
    products = OrderElementsSerializer(many=True, allow_empty=False)
    phonenumber = PhoneNumberField()

    def create(self, request):
        order = Order.objects.create(
            address=request.data['address'],
            firstname=request.data['firstname'],
            lastname=request.data['lastname'],
            phonenumber=request.data['phonenumber'],
        )
        for product_data in request.data['products']:
            OrderElements.objects.create(
                order=order,
                product=Product.objects.get(id=product_data['product']),
                quantity=product_data['quantity'],
                price=Product.objects.get(id=product_data['product']).price * product_data['quantity']
                )
        return order
    
    class Meta:
        model = Order
        fields = [
            'firstname',
            'lastname',
            'phonenumber',
            'products',
            'address'
        ]
