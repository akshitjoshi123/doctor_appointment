from appointments.models import Appointment
from accounts.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from doctors.constants import INVITE_DOCTOR_EMAIL_SUBJECT, INVITE_DOCTOR_EMAIL_BODY, ACTION_MAIL_SUBJECT

class InviteDoctorManager():
    def set_invite_doctor(self, data, *args, **kwargs):
        email_send_to = data.invite_email
        email = EmailMessage(INVITE_DOCTOR_EMAIL_SUBJECT, INVITE_DOCTOR_EMAIL_BODY, to=[email_send_to])
        email.send()

class DoctorManager():
    def get_doctor_list(self, *args, **kwargs):
        return User.objects.exclude(specialist = None)


    def set_update_doctor_profile(self, *args, **kwargs):
        return User.objects.filter(username=self.request.user)


class ActionAppointment():
    def get_appointment(self, *args, **kwargs):
        return Appointment.objects.filter(doctor=self.request.user)

    def set_action(self, *args, **kwargs):
        patient_record = Appointment.objects.filter(id=self.kwargs['pk']).first()
        email_send_to = patient_record.patient.email
        context = {'doctor_name': self.request.user,
                'date': patient_record.date_time,
                'status': patient_record.status}
        body = render_to_string('appointment_action.txt', context)
        email = EmailMessage(ACTION_MAIL_SUBJECT, body , to=[email_send_to])
        email.send()


class RescheduleAppointment():
    def get_appointment(self, *args, **kwargs):
        return Appointment.objects.filter(doctor=self.request.user)

    def set_reschedule(self, *args, **kwargs):
        patient_record = Appointment.objects.filter(id=self.kwargs['pk']).first()
        email_send_to = patient_record.patient.email
        context = {'doctor_name': self.request.user,
                'date': patient_record.date_time}
        body = render_to_string('appointment_reschedule.txt', context)
        email = EmailMessage(ACTION_MAIL_SUBJECT, body , to=[email_send_to])
        email.send()

class MyPatientProfile():
    def get_profile(self, *args, **kwargs):
        return Appointment.objects.filter(doctor=self.request.user)
