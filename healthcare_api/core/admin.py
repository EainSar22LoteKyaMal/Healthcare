from django.contrib import admin
from .models import Appointment, MedicalForm

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'ph_num', 'date', 'time', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'ph_num')
    list_filter = ('date', 'time', 'created_at')
    ordering = ('date', 'time')
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('medical_form')

class MedicalFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor', 'age', 'weight', 'height', 'appointment')
    search_fields = ('name', 'doctor')
    list_filter = ('doctor',)
    ordering = ('name',)

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MedicalForm, MedicalFormAdmin)
