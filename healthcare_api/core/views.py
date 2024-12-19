from rest_framework import viewsets
from rest_framework import permissions
from .models import Appointment, MedicalForm
from .serializers import AppointmentSerializer, MedicalFormSerializer
from django.conf import settings
from django.core.mail import send_mail

class AppointmentViewset(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        appointment = serializer.save(user=self.request.user)
        self.send_confirmation_email(appointment)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == "confirmed":
            self.send_confirmation_email(instance)

    def send_confirmation_email(self, appointment):
        subject = "Appointment Confirmation"
        message = f"""
        Dear {appointment.user.name},

        Your appointment has been confirmed.
        Here are the details:
        
        Name: {appointment.name}
        Email: {appointment.email}
        Phone Number: {appointment.ph_num}
        Date: {appointment.date}
        Time: {appointment.time}

        Please ensure to update your medical form before your appointment by visiting:
        {settings.FRONTEND_URL}/medical_form

        Thank you,
        Healthcare Team
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [appointment.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

class MedicalFormViewSet(viewsets.ModelViewSet):
    queryset = MedicalForm.objects.all()
    serializer_class = MedicalFormSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MedicalForm.objects.filter(appointment__user=self.request.user)  # Ensure only the current user's forms are accessible
    
    def perform_create(self, serializer):
        # Save the medical form instance
        medical_form = serializer.save()
        
        # Send email notification after saving the form
        self.send_email_notification(medical_form)

    def send_email_notification(self, medical_form):
        subject = f"Medical Form Submitted for Appointment on {medical_form.appointment.date} at {medical_form.appointment.time}"
        message = (
            f"Dear {medical_form.name},\n\n"
            f"Thank you for submitting your medical form for the appointment with Dr. {medical_form.doctor}.\n"
            f"Here are the details:\n\n"
            f"Age: {medical_form.age}\n"
            f"Weight: {medical_form.weight}\n"
            f"Height: {medical_form.height}\n"
            f"Medical History: {medical_form.medical_history}\n"
            f"Allergies: {medical_form.allergies}\n"
            f"Symptoms: {medical_form.symptoms}\n"
            f"Emergency Contact: {medical_form.emergency_contact}\n\n"
            "If you have any questions, feel free to reach out.\n\n"
            "Best Regards,\n"
            "Your Medical Team"
        )
        recipient_list = [medical_form.appointment.email] 
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
