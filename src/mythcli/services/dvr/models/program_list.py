""" RSS feed centric model of a MythTV program list. """

import sys
import urllib.request, urllib.error, urllib.parse

from datetime import datetime
# RFC-2822 formatted datetime
from email import utils
from xml.etree.ElementTree import ElementTree

from mythcli import MYTHTV_SERVICES_DATETIME_FORMAT
from mythcli.tools import timezone

LIMIT_ITEMS = 50

# See http://www.mythtv.org/wiki/Record_table
RecordTypeList = ["Not Recording", "Single Record", "Timeslot Record", "Channel Record", 
                  "All Record", "Weekslot Record", "Find One Record", "Override Record (Forced)", 
                  "Don't Record", "Find Daily Record", "Find Weekly Record"]

# Fallback value. No limit if 0
MAX_ITEMS = 0

class ProgramList:

    def __init__(self, args):
        date = utils.formatdate()
    
        # Use web2py naming convention
        self.model_dict = dict(
                                title=args.title,
                                link=args.link,
                                pub_date=date,
                                created_on=date,
                                entries=self.__items__(args))

    def model(self):        
        """ Return RSS data in a dictionary/list tree. """

        return self.model_dict
    
    def __items__(self, args):
        """ Return RSS items dictionary. """

        url = args.url
        tree = ElementTree()
        try:
            tree.parse(urllib.request.urlopen(url))
        except urllib.error.URLError as exc:
            sys.stderr.write("URL %s not known\n" % url)
            #sys.stderr.write("%s\n" % exc.reason)
            sys.exit(exc.reason.errno)
    
        #NOTE max() evens works when one of the the values is None (None is ignored)
        max_items = max(args.max_items[0], 0)
        #ALTERNATIVE when args.max_items has no default value
        #max_items_list = getattr(args, "max_items", None)
        #if max_items_list:
        #    max_items = max(max_items_list[0], 0)
        #else:
        #    max_items = MAX_ITEMS
    
        item_dict_list = []
        programs = tree.findall("Programs/Program")
        if programs is not None:
            for i, program in enumerate(programs):
                if (max_items > 0 and i == max_items) or i == LIMIT_ITEMS:
                    break
                item_dict_list.append(self.__item__(args, program))
                
        return item_dict_list

    def __item__(self, args, program):
        """ Return RSS item dictionary. """
    
        title = program.findtext("Title")
        channel_id = program.findtext("Channel/ChanId")

        # Replace template's item link hostname with mythbackend's hostname and remove the port number
        #urlsplit(), urlunsplit()
        hostname = urllib.parse.urlparse(args.url).hostname
        result = urllib.parse.urlparse(args.item_link)
        parts = urllib.parse.ParseResult(result.scheme, hostname, result.path, result.params, result.query, result.fragment)
        link = urllib.parse.urlunparse(parts)
        
        description_list = self.__program_description__(args, program)
    
        starttime = program.findtext("StartTime")
        starttime_dt = datetime.strptime(starttime, MYTHTV_SERVICES_DATETIME_FORMAT)
        guid = channel_id + "-" + starttime_dt.strftime("%Y%m%d%H%M%S")
    
        # Use web2py naming convention
        item_dict = dict(title=title,
                         link=link,
                         #description={ "program_description": description_list },
                         description=dict(program_description=description_list),
                         guid=guid,
                         created_on=utils.formatdate())
    
        return item_dict
        
    def __program_description__(self, args, program):
        """ Return program description list. """

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
        #recording_status_index = program.findtext("Recording/Status")
        recording_type_index = program.findtext("Recording/RecType")
        
        # Generate values for item description
        
        if subtitle:
            title += " - " + subtitle
        
        if args.title_desc:
            # Return description with only the title
            description_list = [["Title", title]]
            return description_list
        
        channel = channel_number + " - " + channel_callsign
        
        starttime_dt = datetime.strptime(starttime, MYTHTV_SERVICES_DATETIME_FORMAT)
        endtime_dt = datetime.strptime(endtime, MYTHTV_SERVICES_DATETIME_FORMAT)
        air_date = timezone.strflocaltime(starttime_dt, args.date_format[0])
        air_time = timezone.strflocaltime(starttime_dt, args.time_format[0]) + " - " + \
                   timezone.strflocaltime(endtime_dt, args.time_format[0])

        if args.short_desc:
            # Return short description
            description_list = [["Title", title],
                                ["Channel", channel],
                                ["Airdate", air_date],
                                ["Airtime", air_time]]
            return description_list
        
        rec_start_dt = datetime.strptime(recording_starttime, MYTHTV_SERVICES_DATETIME_FORMAT)
        rec_end_dt = datetime.strptime(recording_endtime, MYTHTV_SERVICES_DATETIME_FORMAT)
        
        # Record length in hours and minutes
        recording_length_td = rec_end_dt - rec_start_dt
        recording_length_mins = recording_length_td.seconds // 60
        recording_length = "{0:2}".format(recording_length_mins // 60) + ":" + \
                           "{0:02}".format(recording_length_mins % 60) + ":00"

        recording_type = RecordTypeList[int(recording_type_index)]
        
    #    #summary = """
    #    summary = """Title:         %(title)s
    #Channel:       %(channel)s
    #Airdate:       %(air_date)s
    #Airtime:       %(air_time)s
    #Record Length: %(recording_length)s
    #Category:      %(category)s
    #Description:   %(description)s
    #""" % { "title": title, "channel": channel,
    #                   "air_date": air_date, "air_time": air_time, 
    #                   "recording_length": recording_length,
    #                   "recording_type": recording_type,
    #                   "category": category, "description": description }
    #    
    #    return summary
    
        description_list = [  ["Title", title],
                              ["Channel", channel],
                              ["Airdate", air_date],
                              ["Airtime", air_time],
                              ["Record Length", recording_length],
                              ["Record Type", recording_type],
                              ["Category", category],
                              ["Description", description]]
    
        return description_list
