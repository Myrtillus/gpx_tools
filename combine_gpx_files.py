#!/usr/bin/env python
# -*- coding: latin 1 -*-


import pdb
import sys
import xml.etree.ElementTree as ET

ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
ET.register_namespace('gpxx', "http://www.garmin.com/xmlschemas/GpxExtensions/v3")
ET.register_namespace('gpxtrkx',"http://www.garmin.com/xmlschemas/TrackStatsExtension/v1" )
ET.register_namespace('wptx1', "http://www.garmin.com/xmlschemas/WaypointExtension/v1")
ET.register_namespace('gpxtpx', "http://www.garmin.com/xmlschemas/TrackPointExtension/v1")

# tsekkaa input argumentit, joissa tulee gpx fileet sisaan

files=sys.argv[2:]
target=sys.argv[1]


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


# otetaan ensimmäinen track ja siivoillaan siitä ensin palasia pois ja kasataan sen jälkeen track pointit kyytiin
base=elements[0]

# haetaan trackin sisällä oleva extension osuus ja poistetaan se
ext=base.getroot().find('{http://www.topografix.com/GPX/1/1}trk').find('{http://www.topografix.com/GPX/1/1}extensions')
base.getroot().find('{http://www.topografix.com/GPX/1/1}trk').remove(ext)

# haetaan trackin segmentit ja poistetaan kaikki paitsi ensimmäinen
extra_segments=base.getroot().find('{http://www.topografix.com/GPX/1/1}trk').findall('{http://www.topografix.com/GPX/1/1}trkseg')[1:]
if extra_segments:
    for es in extra_segments:
        base.getroot().find('{http://www.topografix.com/GPX/1/1}trk').remove(es)

# heitetään segmentin sisältä kaikki pisteet mäkeen ja korvataan ne uusilla
destroy_points=base.getroot().find('{http://www.topografix.com/GPX/1/1}trk').find('{http://www.topografix.com/GPX/1/1}trkseg').findall('{http://www.topografix.com/GPX/1/1}trkpt')
for item in destroy_points:
    base.getroot().find('{http://www.topografix.com/GPX/1/1}trk').find('{http://www.topografix.com/GPX/1/1}trkseg').remove(item)

for item in point_elements:
    base.getroot().find('{http://www.topografix.com/GPX/1/1}trk').find('{http://www.topografix.com/GPX/1/1}trkseg').append(item)


open(target,'w').writelines(ET.tostring(base.getroot()))










