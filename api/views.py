from shop.models import Profile, Product, Order
from .serializers import ProductSerializer, ProfileSerializer, OrderSerializer, OrderDetailSerializer, ShopCartSerializer, ReviewSerializer
from rest_framework import viewsets, filters, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django_filters.rest_framework import DjangoFilterBackend
from shop.models import Product, Category, ShopCart, Review
from .serializers import ProductSerializer, CategorySerializer
class ProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for CRUD operations on profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for CRUD operations on orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on products, with additional support for filtering, searching, and ordering.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'desciption']
    ordering_fields = ['name', 'createDate']

class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for performing CRUD operations on categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling orders with a detailed view for individual orders.
    """
    queryset = Order.objects.prefetch_related('orderitem_set').all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        """
        Returns a detailed serializer for the 'retrieve' action and a standard serializer otherwise.
        """
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer
    
class ShopCartViewSet(viewsets.GenericViewSet, generics.RetrieveUpdateAPIView):
    """
    A viewset for retrieving and updating shopping cart instances.
    """
    queryset = ShopCart.objects.all()
    serializer_class = ShopCartSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing CRUD operations on reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CustomAuthToken(ObtainAuthToken):
    """
    A custom authentication token class that handles creating or retrieving a user's auth token.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email
        })