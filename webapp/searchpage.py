from geopy import distance, Nominatim
import datetime
from django.shortcuts import render
from django import forms
from . import models
from .models import Volunteer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
import urllib.parse
from django.utils.html import strip_tags


class SignupForm(forms.Form):
    # old fields
    # readonly_fields = ('daily_ratings',)
    # current fields
    first_name = forms.CharField(max_length=20, label='First Name')
    last_name = forms.CharField(max_length=20, label='Last Name')
    phone_number = forms.IntegerField(label='Phone Number')
    pickup_time = forms.DateTimeField(label='Pickup Date/Time')
    pickup_loc = forms.CharField(max_length=100, label='Pickup Location')


def submission(request):
    submitted = False
    if request.method == 'POST':
        form = SignupForm(request.POST)
        volunteer_match = 'none'
        cd = None
        if form.is_valid():
            #form.save()
            cd = form.cleaned_data
            all_volunteers = Volunteer.objects.all()
            #print(all_volunteers)

            for vol in all_volunteers:
                print(cd['pickup_loc'])
                print(cd['pickup_time'])
                if calc_distance(cd['pickup_loc'], vol.location) <= 10: # match with volunteer who is located <= 10 miles away and available during the specified time
                    vol_times_available = vol.times_available.split(' ')
                    print(vol_times_available)
                    i = 0
                    while i < len(vol_times_available)-3:
                        print("start: " + str(datetime.datetime.strptime(strip_tags(vol_times_available[i]) + ' ' + strip_tags(vol_times_available[i+1][0:-1]), '%Y-%m-%d %H:%M:%S')))
                        print("end: " + str(datetime.datetime.strptime(
                            strip_tags(vol_times_available[i+2]) + ' ' + strip_tags(vol_times_available[i + 3])[0:-1],
                            '%Y-%m-%d %H:%M:%S')))

                        start_time = datetime.datetime.strptime(strip_tags(vol_times_available[i]) + ' ' + strip_tags(vol_times_available[i+1][0:-1]), '%Y-%m-%d %H:%M:%S')
                        end_time = datetime.datetime.strptime(strip_tags(vol_times_available[i+2]) + ' ' + strip_tags(vol_times_available[i + 3])[0:-1],
                            '%Y-%m-%d %H:%M:%S')
                        print("start_time: " + str(start_time))
                        print("end_time: " + str(end_time))
                        if start_time <= cd['pickup_time'].replace(tzinfo=None) <= end_time:
                            volunteer_match = vol
                            # Update volunteer model to reflect match
                            volunteer_match.walk_shifts += cd['first_name'] + ', ' + cd['last_name'] + ', ' + str(
                                cd['phone_number']) + ', ' + str(cd['pickup_time']) + ', ' + cd['pickup_loc'] + '; '
                            volunteer_match.save()
                            break
                        else:
                            i += 4

                    #break

        #return HttpResponseRedirect('/?submitted=True')


        # Print volunteer match (or lack thereof) on redirected page
        vol_id = str(volunteer_match.id) if volunteer_match != 'none' else 'none'
        vol_name = str(volunteer_match.first_name)if volunteer_match != 'none' else 'none'
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