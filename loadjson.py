#!/usr/bin/env python

import json
import MySQLdb

conn = MySQLdb.connect(host= "192.168.59.103", user="student", passwd="secret", db="crime")
query = """INSERT INTO seattle_crime (event_clearance_code, cad_event_number,
   event_clearance_subgroup,
   event_clearance_group,
   cad_cdw_id,
   event_clearance_date,
   zone_beat,
   initial_type_description,
   district_sector,
   initial_type_subgroup,
   hundred_block_location,
   general_offense_number,
   event_clearance_description,
   longitude,
   latitude,
   initial_type_group,
   census_tract)
VALUES  ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

files=[0, 1000, 2000]
datadir="data/%s.json"

for f in files:
  print f
  json_data=open(datadir % f)
  data_list = json.load(json_data)
  for event in data_list:
    # insert into database
    cursor = conn.cursor()
    try:
      cursor.execute(query, (int(event['event_clearance_code']), int(event['cad_event_number']), event['event_clearance_subgroup'],
        event['event_clearance_group'], int(event['cad_cdw_id']), event['event_clearance_date'],  event['zone_beat'],
        event['initial_type_description'], event['district_sector'], event['initial_type_subgroup'], event['hundred_block_location'],
        int(event['general_offense_number']), event['event_clearance_description'], event['longitude'], event['latitude'],
        event['initial_type_group'], event['census_tract']))
      conn.commit()
    except:
      conn.rollback()
    finally:
      cursor.close()
    json_data.close()

conn.close()