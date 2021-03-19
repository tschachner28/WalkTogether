from django.shortcuts import render

def searchpage(request):
    return render(request=request, template_name='searchpage.html', context={"searchpage": searchpage})

