import codecs
import sys

def rss(rss_model_dict):
    """ Generate RSS 2.0 """
    
    # Print in UTF-8
    sys.stdout = codecs.getwriter("UTF-8")(sys.stdout)

#u"""<?xml version="1.0"  encoding="UTF-8"?>
    print \
"""<?xml version="1.0"  encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>%(title)s</title>
    <link>%(link)s</link>
    <pubDate>%(pub_date)s</pubDate>
    <lastBuildDate>%(created_on)s</lastBuildDate>
    <language>en</language>""" \
        % rss_model_dict

    for rss_item_model_dict in rss_model_dict["entries"]:
        print \
"""    <item>
      <title><![CDATA[%(title)s]]></title>
      <link>%(link)s</link>
      <description><![CDATA[%(description)s]]></description>
      <guid isPermaLink="false">%(guid)s</guid>
      <pubDate>%(created_on)s</pubDate>
    </item>""" \
            % rss_item_model_dict

    print \
"""  </channel>
</rss>
"""
    #ALTERNATIVE
    #template = "<html><body><h1>Hello {who}!</h1></body></html>"
    #print(template.format(who="Reader"))
