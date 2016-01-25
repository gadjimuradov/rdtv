from celery import shared_task
from django.conf import settings
from twilio.rest import TwilioRestClient

import arrow

from .models import Appointment

client = TwilioRestClient()

@shared_task
def send_sms_reminder(appointment_id):
	try:
		appointment = Appointment.objects.get(pk=appointment_id)
	except Appointment.DoesNotExist:
		return
    appointment_time = arrow.get(appointment.time, appointment.time_zone.zone)
    body = 'Привет {0}. Ваша встреча назначена {1}.'.format(
        appointment.name,
        appointment_time.format('h:mm a')
    )

    message = client.messages.create(
        body=body,
        to=appointment.phone_number,
        from_=settings.TWILIO_NUMBER,
    )		