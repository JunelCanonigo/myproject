from django.db import models

class Drivers(models.Model):
    plate_number = models.CharField('Plate Number', max_length=10, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) 
    address = models.CharField(max_length=120)
    email_address = models.EmailField('Email Address', blank=True, null=True)
    phone_number = models.CharField('Phone Number', max_length=25)

    def __str__(self):
        return f"{self.plate_number} {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name']
        verbose_name_plural = "Drivers"
