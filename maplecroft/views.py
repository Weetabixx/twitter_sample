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
        
        try:  # fetch embeded version of tweet
            data = oEmbed(url)  # lots of optimisation to do around this
            htmlstrings += data['html']
        except PyOembedException, e:
            print 'An error was ocurred: %s' % e
            
            
    context = {}
    context['tweets'] = htmlstrings
        
    return HttpResponse(template.render(context))
    
    
def map_view(request):
    template = loader.get_template('map.html')
    dots = {}
    f = open("maplecountries", "r")
    for line in f.readlines():  # read number of mentions of each country
        x = line.split(",")
        dots[x[0]] = {}
        dots[x[0]]['size'] = int(x[1])
    f.close()
    
    #  find position of each country
    with open('countries.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            name = row[0]
            longitude = row[2]
            if longitude == "None":  # make sure there is a number value
                longitude = "0"
            latitude = row[3]
            # yes, this is why lots of images are off the coast of west africa
            if latitude == "None":  
                latitude = "0"
            dots[name]['lng'] = longitude
            dots[name]['lat'] = latitude
            
    htmldots = ""
    
    #  add a dot for every country
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
    
    