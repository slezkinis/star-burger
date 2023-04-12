from rest_framework.serializers import ListField 
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField
from rest_framework.serializers import ValidationError
import phonenumbers

from .models import Product, Order


class ApplicationSerializer(ModelSerializer):
    phonenumber = CharField()
    firstname = CharField()
    lastname = CharField()
    products = ListField(write_only=True)
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

    class Meta():
        model = Order
        fields = [
            'id',
            'firstname',
            'lastname',
            'lastname',
            'phonenumber',
            'products',
            'address'
        ]
