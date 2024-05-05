from shop.models import Profile, Product
from rest_framework_json_api import serializers


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")    
    class Meta:
        model = Profile
        fields = (
            'username',
            'phone',
            'city',
            'nationaID',
        )


class ProductSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Product
        fields = (
            'name',
            'dkp',
            'ratingCount',
            'cover',
        )

 