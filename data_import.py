#!/usr/bin/python

import os,sys
import datetime

import urllib2
import logging
import time

try:
    import json
except ImportError:
    import simplejson as json


dateFormat='%H:%M:%S %Y-%m-%d'
token="YOUR_TOKEN_HERE"
useDate='2013-02-21T00:00:00'
#baseUrl = "http://data.seattle.gov/resource/3k2p-39jp.json?$where=event_clearance_date%%3E%%27%s%%27&zone_beat=%s&$order=event_clearance_date%%20desc&$limit=1000"
baseUrl = "http://data.seattle.gov/resource/3k2p-39jp.json?$where=event_clearance_date%%3E%%3D%%27%s%%27&zone_beat=%s&$order=event_clearance_date%%20desc&$limit=%s"

logname="seacri"
logger=logging.getLogger(logname)
dateFormat='%H:%M:%S %Y-%m-%d'

def initLogger():
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('%s.log' % logname)
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


# http://data.seattle.gov/resource/3k2p-39jp.json?$where=event_clearance_date%3E%272015-02-15%27&zone_beat=Q1&$order=event_clearance_date%20desc&$limit=1000
def getUrl(useDate, zoneBeat, limit, offset):
    try:
        if offset == 0:
            url = baseUrl % (useDate, zoneBeat, limit)
        else:
            url = "%s&$offset=%s" % ((baseUrl % (useDate, zoneBeat, limit)), offset)
        logger.debug(url)
        req = urllib2.Request(url)
        req.add_header("X-App-Token", token)
        resp = urllib2.urlopen(req)
        response = resp.read()
        print len(response)
        dumpAsFile("data/%s.json" % offset, response)
    except urllib2.HTTPError, e:
        print "The server at %s could not handle the request." % url
        print "Error code: ", e.code
        logger.debug("HTTPError - error code: %s" % e.code)
        sys.exit(1)
    except urllib2.URLError, e:
        print "We failed to reach the server at %s." % url
        print "Reason: ", e.reason
        logger.debug("URLError -- error reason: %s" % e.reason)
        sys.exit(1)

sBlockLoc='hundred_block_location'
sGeoLoc='incident_location'
sEvtDesc='event_clearance_description'
sEvtDate='event_clearance_date'

def dumpAsFile(name, data):
  f=open(name, "wb")
  f.write(data)
  f.close()

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

if __name__ == "__main__":

    """
    get all data from 365 days ago forward
    chunks of 1000 records
    using an offset
    """
    beat = "Q1"
    day_count=1
    limit=1000
    offset=0
    while True:
      getUrl(datetime.date.today() + datetime.timedelta(days=-365), beat, limit, offset)
      print offset
      offset+=limit
      time.sleep(2)

