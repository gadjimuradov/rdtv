import arrow

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from timezone_field import TimeZoneField

class Appointment(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    time = models.DateTimeField()
    time_zone = TimeZoneField(default='Europe/Moscow')
    task_id = models.CharField(max_length=50,editable=False,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.name

    def get_absolute_url(self):
    	return reverse('view_appointment', args=[str(self.id)])

    def clean(self):
    	appointment_time = arrow.get(self.time,self.time_zone.zone)

    	if appointment_time < arrow.utcnow():
    		raise ValidationError('You cannot schedule an appointment for the past. Please check your time and time_zone')
    def shedule_reminder(self):
    	appointment_time = arrow.get(self.time , self.time_zone.zone)
    	reminder_time = appointment_time.replace(minutes=settings.REMINDER_TIME)

    	from .task import send_sms_reminder
    	result = send_sms_reminder.apply_async((self.pk,), eta=reminder_time)

    	return result.id

    def save(self, *args, **kwargs):
    	if self.task_id:
    		celery_app.control.revoke(self.task_id)
    	super(Appointment,self).save(*args,**kwargs)
    	self.task_id = self.shedule_reminder()
    	super(Appointment,self).save(*args,**kwargs)
