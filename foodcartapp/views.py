from django.http import JsonResponse
from django.templatetags.static import static
import json
import phonenumbers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ListField 
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField
from rest_framework.serializers import ValidationError


from .models import Product, Order, Order_elements


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


class ApplicationSerializer(Serializer):
    phonenumber = CharField()
    firstname = CharField()
    lastname = CharField()
    products = ListField()
    address = CharField()

    def validate_firstname_type(self, value):
        if not isinstance(value, str):
            raise ValidationError('firstname must be a string!')
        return value

    def validate_lastname_type(self, value):
        if not isinstance(value, str):
            raise ValidationError('lastname must be a string!')
        return value

    def validate_products(self, value):
        if not isinstance(value, list):
            raise ValidationError('firstname must be a string!')
        if not value:
            raise ValidationError("this field can't be empty")
        for product in value:
            try:
                Product.objects.get(id=product['product'])
            except:
                raise ValidationError('one of product is not valid')
        return value
    
    def validate_address_type(self, value):
        if not isinstance(value, str):
            raise ValidationError('address must be a string!')
        return value

    def validate_phonenumber(self, value):
        if not isinstance(value, str):
            raise ValidationError('phonenumber must be a string!')
        if not value:
            raise ValidationError("this field can't be empty")
        parsed_number = phonenumbers.parse(value, 'RU')
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError('phonenumber is not valid')
        return value


@api_view(['POST'])
def register_order(request):
    print(request.data)
    serializer = ApplicationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)        
    order = Order.objects.create(
        address=request.data['address'],
        firstname=request.data['firstname'],
        lastname=request.data['lastname'],
        phonenumber=request.data['phonenumber'],
    )
    for product_data in request.data['products']:
        product = Order_elements.objects.create(
            order=order,
            product=Product.objects.get(id=product_data['product']),
            quantity=product_data['quantity'],
        )
    return Response({}, status=status.HTTP_200_OK)
