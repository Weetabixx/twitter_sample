#imports
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from sets import Set

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
            data = oEmbed(url)
            htmlstrings += data['html']
        except PyOembedException, e:
            print 'An error was ocurred: %s' % e
    
    # data is a dict with keys that will depends on the media type. You should
    # choose how to display the content based on the data['type'] value and
    # the oEmbed spec ( http://oembed.com/ ).
    context = {}
    context['tweets'] = htmlstrings
        
    return HttpResponse(template.render(context))