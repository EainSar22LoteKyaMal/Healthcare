from rest_framework import serializers
from .models import CustomUser
import re
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate_age(self, value):
        if value < 14 or value > 80:
          raise serializers.ValidationError("Age must be between 14 and 80.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    def validate_ph_num(self, value):
        if not re.match(r'^09\d{8,9}$', value):
            raise serializers.ValidationError(
                "Phone number must be in the format: 09XXXXXXXX or 09XXXXXXXXX (total 10 or 11 digits)."
            )
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password) 
        instance.save()
        return instance
    