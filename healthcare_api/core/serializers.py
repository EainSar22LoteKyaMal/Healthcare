from rest_framework import serializers
from .models import Appointment, MedicalForm
from datetime import datetime, timezone
import re

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
        
    def validate_ph_num(self, value):
        if not re.match(r'^09\d{8,9}$', value):
            raise serializers.ValidationError(
                "Phone number must be in the format: 09XXXXXXXX or 09XXXXXXXXX (total 10 or 11 digits)."
            )
        return value
        
    def validate_date(self, value):
        if value <= datetime.now(timezone.utc).date():
            raise serializers.ValidationError("Appointment date must be in the future.")
        return value

class MedicalFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalForm
        fields = '__all__'

    def create(self, validated_data):
        appointment = validated_data.pop('appointment') 
        medical_form = MedicalForm.objects.create(appointment=appointment, **validated_data)
        
        return medical_form