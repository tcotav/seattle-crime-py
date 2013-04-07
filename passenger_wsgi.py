#!/usr/bin/python

__author__ = 'james'


import os, sys
import datetime

__author__ = 'james'

#from config import *
import urllib2
import os
import sys
import logging
import time

try:
    import json
except ImportError:
    import simplejson as json

cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import bottle
from bottle import route, run, static_file, request


def application(environ, start_response):
    return bottle.default_app().wsgi(environ,start_response)

dateFormat='%H:%M:%S %Y-%m-%d'
token="TipKr7CKbaEaa7XRFmU6K9j62"
useDate='2013-02-21T00:00:00'
zoneBeat='B2';
baseUrl = "http://data.seattle.gov/resource/3k2p-39jp.json?$where=event_clearance_date%%3E%%27%s%%27&zone_beat=%s&$order=event_clearance_date%%20desc&$limit=1000"

logger=logging.getLogger("seacri")

def initLogger():
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('seacri.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


initLogger()


def getUrl(useDate, zoneBeat):
    try:
        url = baseUrl % (useDate, zoneBeat)
        logger.debug(url)
        req = urllib2.Request(url)
        req.add_header("X-App-Token", token)
        resp = urllib2.urlopen(req)
        response = resp.read()
        return process(response)
    except urllib2.HTTPError, e:
        print "The server at %s could not handle the request." % url
        print "Error code: ", e.code
        logger.debug("HTTPError - error code: %s" % e.code)
        return {'error': "Error code: %s"% e.code}
    except urllib2.URLError, e:
        print "We failed to reach the server at %s." % url
        print "Reason: ", e.reason
        logger.debug("URLError -- error reason: %s" % e.reason)
        return {'error': "Error code: %s"% e.reason}


sBlockLoc='hundred_block_location'
sGeoLoc='incident_location'
sEvtDesc='event_clearance_description'
sEvtDate='event_clearance_date'

def process(jsonDataAsString):
    retArray=[]
    count=0
    for l in json.loads(jsonDataAsString):
        del(l['incident_location']['needs_recoding'])
        l['incident_location'] = [float(l['incident_location']['latitude']) , float(l['incident_location']['longitude']) ]

        (dt, ttime)=l[sEvtDate].split('T')

        retArray.append({
            'date':'%s %s' % (ttime, dt),
            'block':l[sBlockLoc],
            'desc':l[sEvtDesc],
            'geoloc':l[sGeoLoc]})
        count+=1
    logger.debug("processed %d rows" % count)
    print retArray
    return {'dataRows':retArray}


@route('/')
def server_static():
    logger.info("page hit|/")
    return static_file('index.html', root='public/')


@route('/<filename>')
def server_static(filename):
    logger.info("page hit|%s" % filename)
    return static_file(filename, root='public/')

beatCache={}
beatTimeCache={}
CACHE_TIMEOUT_SECONDS=.5*60

@route('/hello')
def getHeader():
    for k in request.headers.keys():
        logger.debug("HEADER %s-%s" % (k, request.headers[k]))
    return "Hello World!"

@route('/crime/<beat>')
def hello(beat="B2"):
    logger.info("page hit|/crime/%s" % beat)
    curTime=time.time()


    if beatTimeCache.has_key(beat):
        logger.debug("found key %s" % beat)
        if curTime - beatTimeCache.get(beat) < CACHE_TIMEOUT_SECONDS:
            logger.debug("fell through -- returning cached value")
            return beatCache[beat]
    else:
        logger.debug("using cached value")
        # refresh the data
        criData=getUrl( datetime.date.today() + datetime.timedelta(days=-1), beat)
        # now update the caches
        beatTimeCache[beat]=curTime
        criData['lastUpdated'] = datetime.datetime.now().strftime(dateFormat)
        criData['updateIntervalMinutes'] = CACHE_TIMEOUT_SECONDS/60
        beatCache[beat]=criData
        return criData

if __name__ == "__main__":
    bottle.debug(True)
    run(reloader=True)

