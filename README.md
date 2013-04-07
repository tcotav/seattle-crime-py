seattle-crime-py
================

Seattle 911 data displayed on google maps html5 page pulled in via bottle.py python formatted for viewing on mobile.  I thought -- what, other than the weather, would I like to look at in the morning?

Data is sourced from http://data.seattle.gov (using the Socrata web api)

Currently running live on dreamhost.com account with url: http://seattle.gnslngr.us

Access processed json at url: http://seattle.gnslngr.us/crime/<seattle police beat>.  

For example, for Ballard, you would use http://seattle.gnslngr.us/crime/B2

Find your precinct here: 
    http://www.seattle.gov/police/maps/precinct_map.htm
and from THERE get the beat (precincts are broken down into beats)

Seattle police have similar site here: http://web5.seattle.gov/mnm/incidentresponse.aspx  (You can actually click through to police report via their link there -- kinda cool).
