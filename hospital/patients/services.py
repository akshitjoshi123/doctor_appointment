from accounts.models import Specialist, User
from appointments.models import Appointment
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from doctors.constants import ACTION_MAIL_SUBJECT


class PatientsManager():
    def get_patients(self, *args, **kwargs):
        return User.objects.filter(specialist = None)


class ReSheduleManager():
    def get_patients(self, *args, **kwargs):
        return Appointment.objects.filter(patient=self.request.user)

    def set_reschedule(self, *args, **kwargs):
        doctor_record = Appointment.objects.filter(id=self.kwargs['pk']).first()
        email_send_to = doctor_record.doctor.email
        context = {'patient_name': self.request.user,
                'date': doctor_record.date_time,
                'status': doctor_record.status}
        body = render_to_string('patient_reschedule.txt', context)
        email = EmailMessage(ACTION_MAIL_SUBJECT, body , to=[email_send_to])
        email.send()