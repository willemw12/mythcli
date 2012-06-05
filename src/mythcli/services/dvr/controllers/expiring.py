from mythcli.services.dvr.models import program_list
from mythcli.services.dvr.views import program_list_rss

DEFAULT_RSS_CHANNEL_LINK = "http://localhost/mythcli/dvr/expiring.xml"
DEFAULT_RSS_CHANNEL_TITLE = "MythTV - Expiring Recordings"
DEFAULT_SERVICE_REQUEST_URL = "http://localhost:6544/Dvr/GetExpiringList"   #count=max_items
TEMPLATE_ITEM_LINK = "http://localhost/mythweb/tv/recorded"

def add_subparser(subparsers):
    parser = subparsers.add_parser("expiring", description="List expiring recordings in RSS 2.0 format.", help="list conflicting recordings")
    parser.add_argument("-l", "--link", default=DEFAULT_RSS_CHANNEL_LINK, help="RSS feed link. Default: " + DEFAULT_RSS_CHANNEL_LINK)
    parser.add_argument("-t", "--title", default=DEFAULT_RSS_CHANNEL_TITLE, help="RSS feed title")
    parser.add_argument("-u", "--url", default=DEFAULT_SERVICE_REQUEST_URL, help="MythTV DVR GetConflictList URL request. Default: request all from localhost")
    
    # Set function to be called when this subparser is selected
    parser.set_defaults(func=run, item_link=TEMPLATE_ITEM_LINK)

def run(args):
    model_dict = program_list.ProgramList(args).model()
    program_list_rss.feed(model_dict)
