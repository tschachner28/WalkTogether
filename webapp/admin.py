from django.contrib import admin
from . models import Volunteer
from tinymce.widgets import TinyMCE
from django.db import models

class SiteAdmin(admin.ModelAdmin):
    #fields = ["first_name", "last_name", "student_id", "email", "grade", "submitted", "submitted_date", "stress_rating", "daily_ratings"]
    fields = ["first_name", "last_name", "location", "times_available", "phone_number", "walk_shifts"]

    formfield_overrides = {models.TextField: {'widget': TinyMCE()}}

admin.site.register(Volunteer, SiteAdmin)
#admin.site.register(Volunteer)