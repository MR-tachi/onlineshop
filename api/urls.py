from django.urls import path
from api import views

urlpatterns = [
    path('profiles/', views.profile_list),
    path('products/', views.product_list),
    path('products/<int:pk>/', views.product_detail),
    path('orders/' , views.OrderList.as_view()),
]