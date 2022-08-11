from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:itemId>', views.detail, name='detail'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('shoppingcart', views.shoppingcart, name='shoppingcart'),
    path('shop', views.shop, name='shop'),
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    path('edit_cart', views.edit_cart, name='edit_cart'),
    path('order', views.order, name='order'),
    path('?filter_by=<str:filterby>&filter_field=<str:filterfield>&show=<int:showcount>',
         views.shop, name='shop')
]
