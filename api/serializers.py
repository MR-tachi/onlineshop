from shop.models import Profile
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

 