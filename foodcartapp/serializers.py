from rest_framework.serializers import ModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField

from .models import Product, Order, OrderElements


class OrderElementsSerializer(ModelSerializer):
    def create(self, order, product_data):
        return OrderElements.objects.create(
            order=order,
            product=Product.objects.get(id=product_data['product']),
            quantity=product_data['quantity'],
            price=Product.objects.get(id=product_data['product']).price * product_data['quantity']
            )

    
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
        return Order.objects.create(
            address=request.data['address'],
            firstname=request.data['firstname'],
            lastname=request.data['lastname'],
            phonenumber=request.data['phonenumber'],
        )
    
    class Meta:
        model = Order
        fields = [
            'firstname',
            'lastname',
            'phonenumber',
            'products',
            'address'
        ]
