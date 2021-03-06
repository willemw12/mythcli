#PYTHON2
#import codecs
#import sys

#NOTE in general, <string>.format() is the preferred method to format a string

def feed(rss_channel_model_dict):
    """ Generate RSS 2.0 from a program_list model. """
    
    #PYTHON2 Print in UTF-8
    #sys.stdout = codecs.getwriter("UTF-8")(sys.stdout)

    print("""<?xml version="1.0"  encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>%(title)s</title>
    <link>%(link)s</link>
    <description>%(description)s</description>
    <pubDate>%(pub_date)s</pubDate>
    <lastBuildDate>%(created_on)s</lastBuildDate>
    <language>%(language)s</language>""" \
        % rss_channel_model_dict)

    for rss_item_model_dict in rss_channel_model_dict["entries"]:
        #print "      <description><![CDATA[%(description)s]]></description>"

        print("""    <item>""")

        #NOTE the 'guid' part is only to make the link unique (to avoid duplicates in the QuiteRSS feed reader)
        #guid.replace("-", "/")
        if rss_item_model_dict["link"] is not None:
            print("""      <link>%(link)s/%(guid)s</link>""" \
                  % rss_item_model_dict)

        if rss_item_model_dict["sub_title"] != "":
            print("""      <title><![CDATA[%(title)s: %(sub_title)s]]></title>""" % rss_item_model_dict)
        else:
            print("""      <title><![CDATA[%(title)s]]></title>""" % rss_item_model_dict)

        print("""      <description>
        <![CDATA[""")
        description_dict = rss_item_model_dict["description"]
        print("         <table>")
        for entry in description_dict["program_description"]:
            #if c in string:whitespace for c in entry[0]:
            if " " in entry[0]:
                print("""            <tr><td align="right" valign="top" style="white-space: nowrap">%s:</td><td>%s</td></tr>""" % (entry[0], entry[1]))
            else:
                print("""            <tr><td align="right" valign="top">%s:</td><td>%s</td></tr>""" % (entry[0], entry[1]))
        print("         </table>")

        print("""       ]]>
      </description>
      <guid isPermaLink="false">%(guid)s</guid>
      <pubDate>%(pub_date)s</pubDate>
     </item>""" \
            % rss_item_model_dict)

    print("""  </channel>
</rss>
""")
    
    #ALTERNATIVE
    #template = "<html><body><h1>Hello {who}!</h1></body></html>"
    #print(template.format(who="Reader"))
