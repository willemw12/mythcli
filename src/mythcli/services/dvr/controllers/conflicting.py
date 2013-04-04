from mythcli.services.dvr.models import conflicting_program_list
from mythcli.services.dvr.views import conflicting_program_list_rss

DEFAULT_RSS_CHANNEL_LINK = "http://localhost/mythcli/dvr/conflicting.xml"
DEFAULT_RSS_CHANNEL_TITLE = "MythTV - Conflicting Recordings"
DEFAULT_SERVICE_REQUEST_URL = "http://localhost:6544/Dvr/GetConflictList"   #count=max_items
DEFAULT_MYTHWEB_BASE_URL = "http://localhost/mythweb"
DEFAULT_MYTHWEB_REL_URL = "tv/upcoming"

def add_subparser(subparsers):
    parser = subparsers.add_parser("conflicting", description="List conflicting recordings in RSS 2.0 format.", help="list conflicting recordings")
    parser.add_argument("-u", "--service-url", default=DEFAULT_SERVICE_REQUEST_URL, help="MythTV DVR GetUpcomingList service request URL. Default: request from localhost; excluding conflicts, previously recorded, etc.")
    parser.add_argument("--feed-url", default=DEFAULT_RSS_CHANNEL_LINK, help="RSS feed link. Default: " + DEFAULT_RSS_CHANNEL_LINK)
    parser.add_argument("--feed-title", default=DEFAULT_RSS_CHANNEL_TITLE, help="RSS feed title")
    parser.add_argument("--mythweb-base-url", help="MythWeb base URL. Default: http://<RSS feed link host name>/mythweb")
    parser.add_argument("--no-feed-item-links", action="store_const", const=True, default=False, help="disable links in RSS feed items")
    
    parser.add_argument("--conflicting-with", action="store_const", const=True, default=False, help="list upcoming recordings that are in conflict with the listed recording")
    parser.add_argument("--short-desc", dest="subparser_short_desc", action="store_const", const=True, default=False, help="list short descriptions")
    parser.add_argument("--title-desc", dest="subparser_title_desc", action="store_const", const=True, default=False, help="list titles")
    
    # Set function to be called when this subparser is selected
    parser.set_defaults(func=run, item_base_link=DEFAULT_MYTHWEB_BASE_URL, item_rel_link=DEFAULT_MYTHWEB_REL_URL)
    
def run(args):
    model_dict = conflicting_program_list.ConflictingProgramList(args).model()
    conflicting_program_list_rss.feed(model_dict)
