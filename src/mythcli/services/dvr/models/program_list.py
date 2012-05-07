""" RSS feed centric model """

import urllib2
import urlparse

from datetime import datetime

# RFC-2822 formatted datetime
from email import utils

from mythcli.tools import timezone
from xml.etree.ElementTree import ElementTree

MYTHTV_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# Fallback value. No limit if 0
MAX_ITEMS = 0

def _rss_item_description(program):
    # Extract values from input XML
    
    title = program.findtext("Title")
    subtitle = program.findtext("SubTitle")
    starttime = program.findtext("StartTime")
    endtime = program.findtext("EndTime")
    category = program.findtext("Category")
    description = program.findtext("Description")
    channel_number = program.findtext("Channel/ChanNum")
    channel_callsign = program.findtext("Channel/CallSign")
    recording_starttime = program.findtext("Recording/StartTs")
    recording_endtime = program.findtext("Recording/EndTs")
    
    # Generate values for item description
    
    if subtitle:
        title += " - " + subtitle
    
    channel = channel_number + " - " + channel_callsign
    
    starttime_dt = datetime.strptime(starttime, MYTHTV_DATETIME_FORMAT)
    endtime_dt = datetime.strptime(endtime, MYTHTV_DATETIME_FORMAT)
    rec_start_dt = datetime.strptime(recording_starttime, MYTHTV_DATETIME_FORMAT)
    rec_end_dt = datetime.strptime(recording_endtime, MYTHTV_DATETIME_FORMAT)
    
    #"%Y-%m-%d"    
    air_date = timezone.strflocaltime(starttime_dt, "%a %d %B, %Y")            
    air_time = timezone.strflocaltime(starttime_dt, "%H:%M") + " - " + \
               timezone.strflocaltime(endtime_dt, "%H:%M")
    
    record_length_td = rec_end_dt - rec_start_dt
    record_length_mins = record_length_td.seconds / 60
    record_length = "{0:02}".format(record_length_mins / 60) + ":" + \
                    "{0:02}".format(record_length_mins % 60)
    
    # Create and return the item description
                
    summary = """<div>
Title:         %(title)s<br/>
Channel:       %(channel)s<br/>
Airdate:       %(air_date)s<br/>
Airtime:       %(air_time)s<br/>
Record Length: %(record_length)s<br/>
Category:      %(category)s<br/>
Description:   %(description)s
        </div>""" % { "title": title, "channel": channel,
                   "air_date": air_date, "air_time": air_time, "record_length": record_length,
                   "category": category, "description": description }
    
    return summary

def _rss_item(args, program):
    title = program.findtext("Title")
    channel_id = program.findtext("Channel/ChanId")

    # Replace template's item link hostname with mythbackend's hostname
    #urlsplit(), urlunsplit()
    hostname = urlparse.urlparse(args.url).hostname
    result = urlparse.urlparse(args.item_link)
    parts = urlparse.ParseResult(result.scheme, hostname, result.path, result.params, result.query, result.fragment)
    link = urlparse.urlunparse(parts)
    
    description = _rss_item_description(program)

    starttime = program.findtext("StartTime")
    starttime_dt = datetime.strptime(starttime, MYTHTV_DATETIME_FORMAT)
    guid = channel_id + "-" + starttime_dt.strftime("%Y%m%d%H%M%S")

    # Use web2py naming convention
    model_dict = dict(
                    title = title,
                    link = link,
                    description = description,
                    guid = guid,
                    created_on = utils.formatdate())

    return model_dict
    
def _rss_items(args):
    url = args.url
    #NOTE max() evens works when one of the the values is None (None is ignored)
    max_items_list = getattr(args, "max_items", None)
    if max_items_list:
        max_items = max(max_items_list[0], 0)
    else:
        max_items = MAX_ITEMS

    model_dict = []
    tree = ElementTree()
    tree.parse(urllib2.urlopen(url))
    programs = tree.findall("Programs/Program")
    if programs is not None:
        for i, program in enumerate(programs):
            if max_items > 0 and i == max_items:
                break
            model_dict.append(_rss_item(args, program))
            
    return model_dict

def rss(args):
    """ Return RSS data in a dictionary tree """
    date = utils.formatdate()

    # Use web2py naming convention
    model_dict = dict(
                    title = args.title,
                    link = args.link,
                    pub_date = date,
                    created_on = date,
                    entries = _rss_items(args))
    
    return model_dict
