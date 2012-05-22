from mythcli.services.dvr.models import program_list
from mythcli.services.dvr.views import program_list_rss

DEFAULT_RSS_CHANNEL_LINK = "http://localhost/mythcli/dvr/upcoming.xml"
DEFAULT_RSS_CHANNEL_TITLE = "MythTV - Upcoming Recordings"
DEFAULT_SERVICE_REQUEST_URL = "http://localhost:6544/Dvr/GetUpcomingList?ShowAll=false"   #count=max_items
TEMPLATE_ITEM_LINK = "http://localhost/mythweb/tv/upcoming"

def add_subparser(subparsers):
    parser = subparsers.add_parser("upcoming", description="List upcoming recordings in RSS 2.0 format.", help="list upcoming recordings")
    parser.add_argument("-l", "--link", default=DEFAULT_RSS_CHANNEL_LINK, help="RSS feed link. Default: " + DEFAULT_RSS_CHANNEL_LINK)
    parser.add_argument("-t", "--title", default=DEFAULT_RSS_CHANNEL_TITLE, help="RSS feed title")
    parser.add_argument("-u", "--url", default=DEFAULT_SERVICE_REQUEST_URL, help="MythTV DVR GetUpcomingList URL request. Default: request from localhost; excluding conflicts, previously recorded, etc.")
    # Set function to be called when this subparser is selected
    parser.set_defaults(func=run, item_link=TEMPLATE_ITEM_LINK)

def run(args):
    model_dict = program_list.rss(args)
    program_list_rss.rss(model_dict)
