from rest_framework.serializers import ListField 
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField
from rest_framework.serializers import ValidationError
import phonenumbers

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

    def create(self, request):
        return Order.objects.create(
            address=request.data['address'],
            firstname=request.data['firstname'],
            lastname=request.data['lastname'],
            phonenumber=request.data['phonenumber'],
        )

    
    def validate_phonenumber(self, value):
        if not isinstance(value, str):
            raise ValidationError('phonenumber must be a string!')
        if not value:
            raise ValidationError("this field can't be empty")
        parsed_number = phonenumbers.parse(value, 'RU')
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError('phonenumber is not valid')
        return value
    
    class Meta:
        model = Order
        fields = [
            'firstname',
            'lastname',
            'phonenumber',
            'products',
            'address'
        ]
