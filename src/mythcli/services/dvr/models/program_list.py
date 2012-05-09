""" RSS feed centric model. """
## - * -  c o d i n g : UTF-8 - * -

import urllib2
import urlparse

from datetime import datetime
# RFC-2822 formatted datetime
from email import utils
from xml.etree.ElementTree import ElementTree

from mythcli import MYTHTV_DATETIME_FORMAT
from mythcli.tools import timezone

LIMIT_ITEMS = 100

# Fallback value. No limit if 0
MAX_ITEMS = 0

#def _rss_item_description(args, program):
def _rss_item_description_entries(args, program):
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
    
    air_date = timezone.strflocaltime(starttime_dt, args.date_format[0])
    air_time = timezone.strflocaltime(starttime_dt, args.time_format[0]) + " - " + \
               timezone.strflocaltime(endtime_dt, args.time_format[0])

    # Record length in hours and minutes
    record_length_td = rec_end_dt - rec_start_dt
    record_length_mins = record_length_td.seconds / 60
    record_length = "{0:2}".format(record_length_mins / 60) + ":" + \
                    "{0:02}".format(record_length_mins % 60) + ":00"
    
#    #summary = u"""
#    summary = """Title:         %(title)s
#Channel:       %(channel)s
#Airdate:       %(air_date)s
#Airtime:       %(air_time)s
#Record Length: %(record_length)s
#Category:      %(category)s
#Description:   %(description)s
#""" % { "title": title, "channel": channel,
#                   "air_date": air_date, "air_time": air_time, "record_length": record_length,
#                   "category": category, "description": description }
#    
#    return summary

    model_list = [["Title", title],
                  ["Channel", channel],
                  ["Airdate", air_date],
                  ["Airtime", air_time],
                  ["Record Length", record_length],
                  ["Category", category],
                  ["Description", description]]

    return model_list

def _rss_item(args, program):
    """ Return RSS item dictionary. """

    title = program.findtext("Title")
    channel_id = program.findtext("Channel/ChanId")

    # Replace template's item link hostname with mythbackend's hostname
    #urlsplit(), urlunsplit()
    hostname = urlparse.urlparse(args.url).hostname
    result = urlparse.urlparse(args.item_link)
    parts = urlparse.ParseResult(result.scheme, hostname, result.path, result.params, result.query, result.fragment)
    link = urlparse.urlunparse(parts)
    
    #description = _rss_item_description(args, program)
    description_entries = _rss_item_description_entries(args, program)

    starttime = program.findtext("StartTime")
    starttime_dt = datetime.strptime(starttime, MYTHTV_DATETIME_FORMAT)
    guid = channel_id + "-" + starttime_dt.strftime("%Y%m%d%H%M%S")

    # Use web2py naming convention
    model_dict = dict(
                    title=title,
                    link=link,
                    #description=description,
                    description_entries=description_entries,
                    guid=guid,
                    created_on=utils.formatdate())

    return model_dict
    
def _rss_items(args):
    url = args.url
    #NOTE max() evens works when one of the the values is None (None is ignored)
    max_items_list = getattr(args, "max_items", None)
    if max_items_list:
        max_items = max(max_items_list[0], 0)
    else:
        max_items = MAX_ITEMS

    model_dict_list = []
    tree = ElementTree()
    tree.parse(urllib2.urlopen(url))
    programs = tree.findall("Programs/Program")
    if programs is not None:
        for i, program in enumerate(programs):
            if (max_items > 0 and i == max_items) or i == LIMIT_ITEMS:
                break
            model_dict_list.append(_rss_item(args, program))
            
    return model_dict_list

def rss(args):
    """ Return RSS data in a dictionary/list tree. """
    date = utils.formatdate()

    # Use web2py naming convention
    model_dict = dict(
                    title=args.title,
                    link=args.link,
                    pub_date=date,
                    created_on=date,
                    entries=_rss_items(args))
    
    return model_dict
