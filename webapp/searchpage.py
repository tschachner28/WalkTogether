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
import urllib.parse


class SignupForm(forms.Form):
    # old fields
    # readonly_fields = ('daily_ratings',)
    # current fields
    first_name = forms.CharField(max_length=20, label='First Name')
    last_name = forms.CharField(max_length=20, label='Last Name')
    phone_number = forms.IntegerField(label='Phone Number')
    pickup_time = forms.DateTimeField(label='Pickup Time')
    pickup_loc = forms.CharField(max_length=100, label='Pickup Location')


def submission(request):
    submitted = False
    if request.method == 'POST':
        form = SignupForm(request.POST)
        volunteer_match = None
        cd = None
        if form.is_valid():
            #form.save()
            cd = form.cleaned_data
            all_volunteers = Volunteer.objects.all()

            print(all_volunteers)

            for vol in all_volunteers:
                if calc_distance(cd['pickup_loc'], vol.location) <= 10: # match with volunteer located <= 10 miles away
                    volunteer_match = vol
                    break

        #return HttpResponseRedirect('/?submitted=True')
        vol_id = str(volunteer_match.id) if volunteer_match != None else 'none'
        vol_name = str(volunteer_match.first_name)if volunteer_match != None else 'none'
        #return HttpResponseRedirect('/?submitted=True&vid=' + vol_id + '&vname=' + vol_name + '&loc=' + cd['pickup_loc'] + '&time=' + cd['pickup_time'])
        query = {"vid": vol_id, "vname": vol_name, "pickuploc": cd['pickup_loc'], "pickuptime": cd['pickup_time']}
        return HttpResponseRedirect('/?submitted=True&' + urllib.parse.urlencode(query))

    else:
        form = SignupForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'searchpage.html',
                  {'form': form, 'submitted': submitted}
                  )


# Params: loc1 and loc2, both of which are addresses represented as strings
def calc_distance(loc1, loc2):
    d = distance.distance
    g = Nominatim(user_agent="webapp")
    _, loc1_geo = g.geocode(loc1)
    _, loc2_geo = g.geocode(loc2)
    return d(loc1_geo, loc2_geo).miles