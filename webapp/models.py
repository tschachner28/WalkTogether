from django.db import models

class Volunteer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    #times_available = models.CharField(max_length=300, default='N/A') # format: start_datetime1, end_datetime1; start_datetime2, end_datetime2; etc.
    #phone_number = models.IntegerField(default=-1)
    times_available = models.TextField(max_length=300)  # format: start_datetime1, end_datetime1; start_datetime2, end_datetime2; etc.
    phone_number = models.IntegerField()

    def __str__(self):  # overrides the string method
        return str(self.first_name + ' ' + self.last_name)