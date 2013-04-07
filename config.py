__author__ = 'james'

# sign up for account here: http://opendata.socrata.com/signup
# then get token here: http://opendata.socrata.com/profile/app_tokens
token="YOUR_TOKEN_HERE"

#
# we only go back to the server every CACHE_TIMEOUT_SECONDS
# if we can wait 4 hours to get the data from SPD, we certainly
# can wait 5-15-30 more minutes, no?
#
CACHE_TIMEOUT_SECONDS=.5*60

# this url works for me
baseUrl = "http://data.seattle.gov/resource/3k2p-39jp.json?$where=event_clearance_date%%3E%%27%s%%27&zone_beat=%s&$order=event_clearance_date%%20desc&$limit=1000"

logname="seacri"
