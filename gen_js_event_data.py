#!/usr/bin/env python

import json
import MySQLdb

event_types=[
  'SUSPICIOUS CIRCUMSTANCES',
  'TRAFFIC RELATED CALLS',
  'FALSE ALARMS',
  'DISTURBANCES',
  'BURGLARY',
  'CAR PROWL',
  'AUTO THEFTS',
  'NUISANCE, MISCHIEF',
  'OTHER PROPERTY',
  'FRAUD CALLS',
  'PROPERTY DAMAGE'
]

query="select latitude, longitude from seattle_crime where event_clearance_group = %s"


conn = MySQLdb.connect(host= "192.168.59.103", user="student", passwd="secret", db="crime")

ccount=0
f=open("jsdata/out.js", "wb")
for event in event_types:
  try:
    cursor = conn.cursor()
    cursor.execute(query, (event,))
    rows = cursor.fetchall()
    usedata=[]
    for r in rows:
      usedata.append("new google.maps.LatLng(%s,%s)" % (r[0], r[1]))

    f.write("var data%s=[\n" % ccount)
    f.write(",".join(usedata))
    f.write("];\n\n")

  except Exception, ex:
    print ex
  finally:
    cursor.close()
  ccount +=1

f.close()
conn.close()
