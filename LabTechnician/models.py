from django.db import models
from Donor.models import Appointment, Donor

class DeferringList(models.Model):
    Donor_id = models.OneToOneField(Donor , on_delete=models.CASCADE)


class FininshedAppointment(models.Model):
    Appointment_id = models.ForeignKey(Appointment , on_delete=models.CASCADE)

