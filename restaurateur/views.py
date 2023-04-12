from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from star_burger.settings import YANDEX_APIKEY

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
import requests
from geopy import distance

from .coordinates import fetch_coordinates

from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem
from places.models import Place


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def get_distance(restaurant, order_coords):
    place = Place.objects.get(adress=restaurant.address)
    restaurant_coords = (place.lon, place.lat)
    if not restaurant_coords:
        return None
    distance_restaurant = distance.distance(
        (order_coords[1], order_coords[0]), 
        (restaurant_coords[1], restaurant_coords[0])).km
    return distance_restaurant


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = []
    restaurants = []
    error = False
    for order in Order.objects.filter(executive_restaurant__isnull=True).calcurate_order_cost():
        try:
            order_coords = fetch_coordinates(YANDEX_APIKEY, order.address)
        except:
            error = True
            break
        for restaurant in Restaurant.objects.all():
            restaurant_menu = [product.product for product in restaurant.menu_items.all()]
            for order_product in order.products.all():
                if order_product.product not in restaurant_menu:
                    break
            else:
                restaurants.append(restaurant)
        restaurants_with_distances = []
        if not error:
            for restaurant in restaurants:
                restaurant_distance = get_distance(restaurant, order_coords)
                if not restaurant_distance:
                    error = True
                    break
                restaurants_with_distances.append(
                    (restaurant.name, restaurant_distance)
                )
        restaurants_with_distances = sorted(restaurants_with_distances, key=lambda restaurant: restaurant[1])
        orders.append(
            {
                'client_name': f'{order.firstname} {order.lastname}',
                'phonenumber': order.phonenumber, 
                'id': order.id,
                'address': order.address,
                'cost': f'{order.order_cost} руб.',
                'status': order.status,
                'error': error,
                'comment': order.comment,
                'payment_method': order.payment_method,
                'restaurants': restaurants_with_distances,
                'restaurant': ''
            }
        )
    for order in Order.objects.filter(executive_restaurant__isnull=False).calcurate_order_cost():
        orders.append(
            {
                'client_name': f'{order.firstname} {order.lastname}',
                'phonenumber': order.phonenumber, 
                'id': order.id,
                'address': order.address,
                'cost': f'{order.order_cost} руб.',
                'status': order.status,
                'comment': order.comment,
                'payment_method': order.payment_method,
                'restaurants': '',
                'restaurant': order.executive_restaurant
            }
        )
    return render(request, template_name='order_items.html', context={
        'orders': orders
    })

