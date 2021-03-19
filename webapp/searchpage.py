from geopy import distance, Nominatim
from datetime import datetime
from django.shortcuts import render
from django import forms
from . import models
from .models import Volunteer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse


class SignupForm(forms.Form):
    # old fields
    # readonly_fields = ('daily_ratings',)
    # current fields
    first_name = forms.CharField(max_length=20, label='First Name')
    last_name = forms.CharField(max_length=20, label='Last Name')
    phone_number = forms.IntegerField()
    pickup_time = forms.DateTimeField()
    pickup_loc = forms.CharField(max_length=100, label='Pickup Location')


# Params: loc1 and loc2, both of which are addresses represented as strings
def calc_distance(loc1, loc2):
    d = distance.distance
    g = Nominatim(user_agent="webapp")
    _, loc1_geo = g.geocode(loc1)
    _, loc2_geo = g.geocode(loc2)
    return d(loc1_geo, loc2_geo).miles