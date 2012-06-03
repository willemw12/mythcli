#PYTHON2
#import codecs
#import sys

def feed(rss_model_dict):
    """ Generate RSS 2.0 from a conflicting_program_list model. """
    
    #PYTHON2 Print in UTF-8
    #sys.stdout = codecs.getwriter("UTF-8")(sys.stdout)

    print("""<?xml version="1.0"  encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>%(title)s</title>
    <link>%(link)s</link>
    <pubDate>%(pub_date)s</pubDate>
    <lastBuildDate>%(created_on)s</lastBuildDate>
    <language>en</language>""" \
        % rss_model_dict)

    for rss_item_model_dict in rss_model_dict["entries"]:
        #print "      <description><![CDATA[%(description)s]]></description>"

        print("""    <item>
      <title><![CDATA[%(title)s]]></title>
      <link>%(link)s</link>
      <description>
        <![CDATA[""" \
            % rss_item_model_dict)

        description_dict = rss_item_model_dict["description"]

        print("         <table>")
        for entry in description_dict["program_description"]:
            #if c in string:whitespace for c in entry[0]:
            if " " in entry[0]:
                print("""            <tr><td align="right" valign="top" style="white-space: nowrap">%s:</td><td>%s</td></tr>""" % (entry[0], entry[1]))
            else:
                print("""            <tr><td align="right" valign="top">%s:</td><td>%s</td></tr>""" % (entry[0], entry[1]))
        print("         </table>")

        #### Section with additional code, compared to program_list_rss.py
        
        descriptions_list = description_dict["program_descriptions_conflicting_with"]
        if descriptions_list is not None and descriptions_list != []:
            print("         <br/>\n         Conflicts with upcoming recording%s:\n         <br/><br/>" % ("s" if len(descriptions_list) > 1 else ""))
            for i, description_list in enumerate(descriptions_list):
                print("         <table>")
                for entry in description_list:
                    #if c in string:whitespace for c in entry[0]:
                    if " " in entry[0]:
                        print("""            <tr><td align="right" valign="top" style="white-space: nowrap">%s:</td><td>%s</td></tr>""" % (entry[0], entry[1]))
                    else:
                        print("""            <tr><td align="right" valign="top">%s:</td><td>%s</td></tr>""" % (entry[0], entry[1]))
                print("         </table>")
                if i < len(descriptions_list) - 1:
                    print("         <br/>")

        ####
        
        print("""       ]]>
      </description>
      <guid isPermaLink="false">%(guid)s</guid>
      <pubDate>%(created_on)s</pubDate>
    </item>""" \
            % rss_item_model_dict)

    print("""  </channel>
</rss>
""")
