from django.db import models

class Volunteer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    location = models.CharField(max_length=100)

    def __str__(self):  # overrides the string method
        return str(self.first_name + ' ' + self.last_name)