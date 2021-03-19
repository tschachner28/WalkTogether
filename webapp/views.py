from django.shortcuts import render
from .models import Volunteer

def searchpage(request):
    #return render(request=request, template_name='searchpage.html', context={"searchpage": searchpage})
    return render(request=request, template_name='searchpage.html', context={"Volunteer": Volunteer.objects.all})

