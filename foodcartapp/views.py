from django.http import JsonResponse
from django.templatetags.static import static
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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


@api_view(['POST'])
def register_order(request):
    if 'products' not in request.data:
        content = {'error': 'products: products is a required field'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if not request.data['products']:
        content = {'error': 'products: products cannot be empty'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if not isinstance(request.data['products'], list):
        content = {'error': 'products: products must be a list'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
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
