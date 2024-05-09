from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shop.models import Profile, Product, Order
from .serializers import ProductSerializer, ProfileSerializer, OrderSerializer, OrderDetailSerializer
from rest_framework import generics, mixins, viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from shop.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


@api_view(['GET', 'POST'])
def profile_list(request):
    """
    List all profiles, or create a new profile.
    """
    if request.method == 'GET':
        Profiles = Profile.objects.all()
        serializer = ProfileSerializer(Profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all().prefetch_related('orderitem_set')
    serializer_class = OrderDetailSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'desciption']
    ordering_fields = ['name', 'createDate']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer