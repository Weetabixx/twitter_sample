#imports
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from sets import Set
import csv


import startup


from pyoembed import oEmbed, PyOembedException
from pyoembed.providers import BaseProvider

class TwitterProvider(BaseProvider):

    # priority of the provider. Increase it if the provider isn't well known
    priority = 10

    # url schemas that are supported by the provider.
    # re.compile'd regex are allowed.
    oembed_schemas = ['https://twitter.com/*/status/*',
                      'https://*.twitter.com/*/status/*']

    # api endpoint that answers to oEmbed requests for the provider.
    oembed_endpoint = 'https://publish.twitter.com/oembed'


#make pages here
def index(request):
    template = loader.get_template('index.html')
    tweetid = '989838191439024128'
    idList = Set([])
    f = open("mapletweets", "r")
    for line in f.readlines():
        if line: # empty strings equate to false
            idList.add(line)
    f.close()
    htmlstrings = ""
    for tweetid in idList:
        url = 'https://twitter.com/MaplecroftRisk/status/' + str(tweetid)
        # handle does not matter, only id
        
        try:
            data = oEmbed(url)  # lots of optimisation to do around this
            htmlstrings += data['html']
        except PyOembedException, e:
            print 'An error was ocurred: %s' % e
    
    # data is a dict with keys that will depends on the media type. You should
    # choose how to display the content based on the data['type'] value and
    # the oEmbed spec ( http://oembed.com/ ).
    context = {}
    context['tweets'] = htmlstrings
        
    return HttpResponse(template.render(context))
    
    
def map_view(request):
    template = loader.get_template('map.html')
    dots = {}
    f = open("maplecountries", "r")
    for line in f.readlines():
        x = line.split(",")
        dots[x[0]] = {}
        dots[x[0]]['size'] = int(x[1])
    f.close()
    
    with open('countries.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            name = row[0]
            longitude = row[2]
            if longitude == "None":
                longitude = "0"
            latitude = row[3]
            if latitude == "None":
                latitude = "0"
            dots[name]['lng'] = longitude
            dots[name]['lat'] = latitude
            
    htmldots = ""
    
    for dot in dots:
        x = 180 + float(dots[dot]['lng'])
        y = 90 + (float(dots[dot]['lat']) * -1)  # longitude is upside down
        htmldots += '<span class="dot" style="height:'
        htmldots += str(dots[dot]['size'])
        htmldots += 'px;width:'
        htmldots += str(dots[dot]['size'])
        htmldots += 'px;position:absolute;left:'
        htmldots += str(x) 
        htmldots += 'px;top:'
        htmldots += str(y) 
        htmldots += 'px;background-color: #bbb;border-radius: 50%;"></span>'
    context = {}
    context['dots'] = htmldots
    return HttpResponse(template.render(context))
    
    