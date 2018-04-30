#imports
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import startup

#make pages here
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())