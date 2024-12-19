from django.urls import path, include
from .views import AppointmentViewset, MedicalFormViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'appointment', AppointmentViewset)
router.register(r'medical_form', MedicalFormViewSet)

urlpatterns = [
    path('', include(router.urls)),
]