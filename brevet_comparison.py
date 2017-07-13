#!/usr/bin/env python
# -*- coding: latin 1 -*-

import numpy
import matplotlib.pyplot as plt
import pdb
import sys
import xml.etree.ElementTree as ET
import math  
from math import cos, asin, sqrt
from math import radians, cos, sin, asin, sqrt


ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
ET.register_namespace('gpxx', "http://www.garmin.com/xmlschemas/GpxExtensions/v3")
ET.register_namespace('gpxtrkx',"http://www.garmin.com/xmlschemas/TrackStatsExtension/v1" )
ET.register_namespace('wptx1', "http://www.garmin.com/xmlschemas/WaypointExtension/v1")
ET.register_namespace('gpxtpx', "http://www.garmin.com/xmlschemas/TrackPointExtension/v1")


"""
https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
"""


"""
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin...
"""
"""
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

"""

  
def recalculate_coordinate(val,  _as=None):  
  """ 
    Accepts a coordinate as a tuple (degree, minutes, seconds) 
    You can give only one of them (e.g. only minutes as a floating point number) and it will be duly 
    recalculated into degrees, minutes and seconds. 
    Return value can be specified as 'deg', 'min' or 'sec'; default return value is a proper coordinate tuple. 
  """  
  deg,  min,  sec = val  
  # pass outstanding values from right to left  
  min = (min or 0) + int(sec) / 60  
  sec = sec % 60  
  deg = (deg or 0) + int(min) / 60  
  min = min % 60  
  # pass decimal part from left to right  
  dfrac,  dint = math.modf(deg)  
  min = min + dfrac * 60  
  deg = dint  
  mfrac,  mint = math.modf(min)  
  sec = sec + mfrac * 60  
  min = mint  
  if _as:  
    sec = sec + min * 60 + deg * 3600  
    if _as == 'sec': return sec  
    if _as == 'min': return sec / 60  
    if _as == 'deg': return sec / 3600  
  return deg,  min,  sec  
        
  
def points2distance(start,  end):  
  """ 
    Calculate distance (in kilometers) between two points given as (long, latt) pairs 
    based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula). 
    Implementation inspired by JavaScript implementation from http://www.movable-type.co.uk/scripts/latlong.html 
    Accepts coordinates as tuples (deg, min, sec), but coordinates can be given in any form - e.g. 
    can specify only minutes: 
    (0, 3133.9333, 0)  
    is interpreted as  
    (52.0, 13.0, 55.998000000008687) 
    which, not accidentally, is the lattitude of Warsaw, Poland. 
  """  

  start_long = math.radians(recalculate_coordinate(start[0],  'deg'))  
  start_latt = math.radians(recalculate_coordinate(start[1],  'deg'))  
  end_long = math.radians(recalculate_coordinate(end[0],  'deg'))  
  end_latt = math.radians(recalculate_coordinate(end[1],  'deg'))  
  d_latt = end_latt - start_latt  
  d_long = end_long - start_long  
  a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2  
  c = 2 * math.asin(math.sqrt(a))  
  return 6371 * c  




# tsekkaa input argumentit, joissa tulee gpx fileet sisaan

files=sys.argv[1:]


# parse all files to list of trees
elements=[]

for item in files:
    elements.append(ET.parse(item))


# ideoita
# - kaivele kaikista fileistä träkit ('{http://www.topografix.com/GPX/1/1}trk')
# - kaivele träkeistä segmentit ('{http://www.topografix.com/GPX/1/1}trkseg')
# - kaivele segmenteistä track pointit ('{http://www.topografix.com/GPX/1/1}trkpt')
#
# esim: trees[0].getroot().findall('{http://www.topografix.com/GPX/1/1}trk')[0]
# .findall('{http://www.topografix.com/GPX/1/1}trkseg')[0]
# .findall('{http://www.topografix.com/GPX/1/1}trkpt')

# root - trk - seg - trkpt

# Tarkoituksena on tunkea kaikki track pointit yhteen ja samaan segmenttiin yhteen ainoaan träkkiin

point_elements=[]
for element in elements:
    tracks=element.getroot().findall('{http://www.topografix.com/GPX/1/1}trk')
    for track in tracks:
        segments=track.findall('{http://www.topografix.com/GPX/1/1}trkseg')
        for segment in segments:
            points=segment.findall('{http://www.topografix.com/GPX/1/1}trkpt')
            point_elements.extend(points)

# nyt kaikista fileistä on kerätty pisteet point_elements listalle
# point_elements[0].attrib antaa koordinaatit

# aikaleima: point_elements[0]._children[1].text         '2017-07-07T10:41:25Z'

# loopataan lävitse pisteet ja lasketaan pisteiden väliset etäisyydet

distances=[]
cumtime=[]
starttime = datetime.datetime.strptime(point_elements[0]._children[1].text,"%Y-%m-%dT%H:%M:%SZ")
for index in range(0,len(point_elements)-1):
	startpoint = ((float(point_elements[index].attrib['lon']),0,0),(float(point_elements[index].attrib['lat']),0,0))
	endpoint = ((float(point_elements[index+1].attrib['lon']),0,0),(float(point_elements[index+1].attrib['lat']),0,0))
	endtime = datetime.datetime.strptime(point_elements[index+1]._children[1].text,"%Y-%m-%dT%H:%M:%SZ")

	distances.append(points2distance(startpoint, endpoint))
	cumtime.append(endtime-starttime)

# lasketaan kumulatiiviset kilometrit
cumdistance = numpy.cumsum(distances)

# lasketaan kumulatiiviset tunnit
cumhours = [(x.days*24.0+x.seconds/3600.0) for x in cumtime]

# Brevet rajat
limit_kilometers =[ 0,200,300,400,600,1000,1200]
limit_hours=[0,13.5,20,27,40,75,90]

# kilometritase eli paljonko ollaan edellä kilometreissä
kilometer_budget = [(x[1] - numpy.interp(x[0],limit_hours, limit_kilometers)) for x in zip(cumhours,cumdistance)]


# Tuntitase, montako tuntia ollaan haamua edellä.
hour_budget = [(numpy.interp(x[1],limit_kilometers,limit_hours))- x[0] for x in zip(cumhours,cumdistance)]


# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(3)
axarr[0].plot(limit_hours,limit_kilometers,'r')
axarr[0].plot(cumhours,cumdistance,'g')
axarr[0].set_title('Kilometrikertyma vs tunnit')
axarr[0].grid(b=True)
axarr[0].set_xlim(left = 0 , right = max(cumhours)+5)


axarr[1].plot(cumhours, kilometer_budget)
axarr[1].set_title('Kilometritase: Paljonko ollaan haamua edella kilometreissa')
axarr[1].grid(b=True)
axarr[1].set_xlim(left = 0 , right = max(cumhours)+5)

axarr[2].plot(cumhours, hour_budget)
axarr[2].set_title('Tuntitase: Paljonko haamulta kestaa ajaa kiinni pysahtynyt kuski')
axarr[2].grid(b=True)
axarr[2].set_xlim(left = 0 , right = max(cumhours)+5)


plt.show()








