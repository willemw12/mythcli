""" RSS feed centric model of a MythTV program conflict list. """

import sys
import time
import urllib.parse

from datetime import datetime
from xml.etree.ElementTree import ElementTree

from mythcli import MYTHTV_SERVICES_DATETIME_FORMAT
from . import program_list

class ConflictingProgramList(program_list.ProgramList):

    def __init__(self, args):
        super(ConflictingProgramList, self).__init__(args)

    #def model(self):
    #    return super(ProgramConflictList, self).model()
    
    #def __items__(self, args):
    #    return super(ConflictingProgramList, self).__items__(args)

    def __item__(self, args, program):
        """ Return RSS item dictionary. """
        
        item_dict = super(ConflictingProgramList, self).__item__(args, program)

        description_dict = item_dict["description"]
        if args.conflicting_with:
            descriptions_list = self.__program_descriptions_conflicting_with__(args, program)
        else:
            descriptions_list = None
        description_dict["program_descriptions_conflicting_with"] = descriptions_list
        
        return item_dict
    
    #def __program_description__(self, args, program):
    #    return super(ProgramConflictList, self).__program_description__(args, program)

    def __program_descriptions_conflicting_with__(self, args, program):
        """ Return description list of upcoming programs that are in conflict with @program. """

        # Find recordings which overlap with @program recording times

        # Create "upcoming recordings" DVR service URL
        # E.g. change
        #     http://localhost:6544/Dvr/GetConflictList
        # into
        #     http://localhost:6544/Dvr/GetUpcomingList?ShowAll=false
        result = urllib.parse.urlparse(args.url)
        parts = urllib.parse.ParseResult(result.scheme, result.netloc, "Dvr/GetUpcomingList", result.params, "ShowAll=false", "")
        url = urllib.parse.urlunparse(parts)

        # Get "upcoming recordings" list
        tree = ElementTree()
        try:
            tree.parse(urllib.request.urlopen(url))
        except urllib.error.URLError as exc:
            sys.stderr.write("URL %s not known\n" % url)
            #sys.stderr.write("%s\n" % exc.reason)
            sys.exit(exc.reason.errno)

        # Find upcoming recordings with recordings times overlapping with @program recording times

        rec_start = time.mktime(datetime.strptime(program.findtext("Recording/StartTs"), MYTHTV_SERVICES_DATETIME_FORMAT).timetuple())
        rec_end = time.mktime(datetime.strptime(program.findtext("Recording/EndTs"), MYTHTV_SERVICES_DATETIME_FORMAT).timetuple())
        recording_time_range = (rec_start, rec_end)

        channel_id = program.findtext("Channel/ChanId")
        starttime = program.findtext("StartTime")
        starttime_dt = datetime.strptime(starttime, MYTHTV_SERVICES_DATETIME_FORMAT)
        recording_guid = channel_id + "-" + starttime_dt.strftime("%Y%m%d%H%M%S")

        max_items = max(args.max_items[0], 0)
        descriptions_list = []
        programs = tree.findall("Programs/Program")
        if programs is not None:
            for i, program in enumerate(programs):
                if (max_items > 0 and i == max_items) or i == program_list.LIMIT_ITEMS:
                    break

                # Skip @program it self
                channel_id = program.findtext("Channel/ChanId")
                starttime = program.findtext("StartTime")
                starttime_dt = datetime.strptime(starttime, MYTHTV_SERVICES_DATETIME_FORMAT)
                upcoming_guid = channel_id + "-" + starttime_dt.strftime("%Y%m%d%H%M%S")
                if upcoming_guid == recording_guid:
                    continue

                # Check overlapping recording times
                rec_start = time.mktime(datetime.strptime(program.findtext("Recording/StartTs"), MYTHTV_SERVICES_DATETIME_FORMAT).timetuple())
                rec_end = time.mktime(datetime.strptime(program.findtext("Recording/EndTs"), MYTHTV_SERVICES_DATETIME_FORMAT).timetuple())
                upcoming_recording_time_range = (rec_start, rec_end)
                if time_range_overlapping(upcoming_recording_time_range, recording_time_range):
                    s = args.subparser_short_desc
                    args.short_desc = args.subparser_short_desc
                    t = args.subparser_title_desc
                    args.title_desc = args.subparser_title_desc
                    descriptions_list.append(super(ConflictingProgramList, self).__program_description__(args, program))
                    args.short_desc = s
                    args.title_desc = t
                    
        return descriptions_list

####

def time_range_overlapping(range1, range2):
    """ Return True if a range overlaps the other range partly or completely. """
    
    (start1, end1) = range1
    (start2, end2) = range2

    # Range1 starts or ends in range2 or vice versa    
    return ((start2 <= start1 <= end2) or (start2 <= end1 <= end2) or
            (start1 <= start2 <= end1) or (start1 <= end2 <= end1))
