from shop.models import Profile, Product, Order, OrderItem, Product, Category
from rest_framework_json_api import serializers


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")    
    class Meta:
        model = Profile
        fields = ['username', 'phone', 'city', 'nationaID']


class ProductSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Product
        fields = ['name', 'dkp', 'ratingCount', 'cover']

class OrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")    
    
    class Meta:
        model = Order
        fields = ['pk', 'username', 'createDate', 'informations', 'status']


class OrderItemSerializer(serializers.ModelSerializer):
    dkpc = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'dkpc', 'name', 'price', 'quantity', 'status']

    def get_dkpc(self, obj):
        return obj.variantProduct.dkpc if obj.variantProduct else None

    def get_name(self, obj):
        return obj.variantProduct.product.name if obj.variantProduct and obj.variantProduct.product else None

class OrderDetailSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    username = serializers.CharField(read_only=True, source="user.username")    

    class Meta:
        model = Order
        fields = ['id', 'username', 'createDate', 'informations', 'note', 'status', 'orderitems']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'desciption', 'dkp', 'createDate', 'averageRating', 'ratingCount', 'cover']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']