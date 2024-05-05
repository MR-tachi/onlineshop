from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from shop.models import Profile , Product
import api.serializers as f


@api_view(['GET', 'POST'])
def profile_list(request):
    """
    List all profiles, or create a new profile.
    """
    if request.method == 'GET':
        Profiles = Profile.objects.all()
        serializer = f.ProfileSerializer(Profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = f.ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
def product_list(request):
    """
    List all products, or create a new product.
    """
    if request.method == 'GET':
        Products = Product.objects.all()
        serializer = f.ProductSerializer(Products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = f.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    """
    Retrieve, update or delete a Product.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = f.ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = f.ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == '':
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)