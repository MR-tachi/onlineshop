from shop.models import Profile
from rest_framework_json_api import serializers


class ProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Profile
        fields = (
            'phone',
            'city',
            'nationaID',
        )
 