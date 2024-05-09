from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('profiles/', views.profile_list, name='profile-list'),
    path('orders/', views.OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailAPIView.as_view(), name='order-detail'),
]