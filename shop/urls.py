from django.urls import path, include
from . import views

urlpatterns = [
    path('Product/<int:itemId>', views.detail, name='detail'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('shoppingcart', views.shoppingcart, name='shoppingcart'),
    path('shop', views.shop, name='shop'),
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    path('edit_cart', views.edit_cart, name='edit_cart'),
    path('order', views.order, name='order'),
    path('vieworders', views.vieworders, name='vieworders'),
    path('detailorder/<int:orderId>', views.detailorder, name='detailorder'),
    path('commentmanager', views.commentmanager, name='commentmanager'),
    path('addcomment', views.addcomment, name='addcomment'),
    path('?filter_by=<str:filterby>&filter_field=<str:filterfield>&show=<int:showcount>',
         views.shop, name='shop')
]
