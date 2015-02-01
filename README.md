mythcli
=======

Mythcli is a Python program to generate MythTV RSS feeds, for example of upcoming or conflicting recordings.


Features
--------

Mythcli is a partially implemented command-line interface of the MythTV Services API (MythTV versions .25 and higher). It supports only a few MythTV DVR Service requests and returns the response in RSS 2.0 format. Mythcli runs on Python 3 (3.2 or higher).

To view the available mythcli commands and options, run:

    $ ./src/mythcli.py --help

and

    $ ./src/mythcli.py <subcommand> --help

This program is licensed under GPLv3 (see included file COPYING).


Usage
-----

Optionally, create a symbolic link, located in one of the $PATH directories, to mythcli.py. For example, from this directory, run:

    $ ln -s $(pwd)/src/mythcli.py ~/bin/mythcli

To update, for example, an RSS feed of **upcoming recordings** once a day on your local web server, create a similar cron job listed below. It is assumed here that the mythbackend server is running on the same machine:

    LANG=en_US.UTF-8
    PATH=/home/$USER/bin:$PATH

    # m h  dom mon dow   command
    00  0  *   *   *     mythcli upcoming --feed-url http://www.webserver.com/mythcli/dvr/upcoming.xml > /var/www/mythcli/dvr/upcoming.xml

Or to get notified in an RSS feed about programs that won't be **recorded** because of **conflicts**:

    LANG=en_US.UTF-8
    PATH=/home/$USER/bin:$PATH

    # m h  dom mon dow   command
    00  0  *   *   *     mythcli conflicting --conflicting-with --short-desc --feed-url http://www.webserver.com/mythcli/dvr/conflicting.xml > /var/www/mythcli/dvr/conflicting.xml

The same examples as above, but with US datetime format and with the mytbackend server running on another machine:

    LANG=en_US.UTF-8
    PATH=/home/$USER/bin:$PATH

    # m h  dom mon dow   command
    00  0  *   *   *     mythcli --date-format "%a %B %d, %Y" --time-format "%I:%M %p" upcoming --feed-url http://www.webserver.com/mythcli/dvr/upcoming.xml --service-url http://mythbackend:6544/Dvr/GetUpcomingList?ShowAll=false --mythweb-base-url http://mythbackend > /var/www/mythcli/dvr/upcoming.xml
    00  0  *   *   *     mythcli --date-format "%a %B %d, %Y" --time-format "%I:%M %p" conflicting --conflicting-with --feed-url http://www.webserver.com/mythcli/dvr/conflicting.xml --service-url http://mythbackend:6544/Dvr/GetConflictList --mythweb-base-url http://mythbackend > /var/www/mythcli/dvr/conflicting.xml

`service-url` is the URL to the MythTV service. The other options are there for configuring the RSS output.

`www.webserver.com` and `mythbackend` are example hostnames.

The mythcli program needs to have permission to write its output in the related web server folder, for example in /var/www/mythcli/dvr/.

The RSS feeds in these examples will be located at [http://www.webserver.com/mythcli/dvr/upcoming.xml](http://www.webserver.com/mythcli/dvr/upcoming.xml) and [http://www.webserver.com/mythcli/dvr/conflicting.xml](http://www.webserver.com/mythcli/dvr/conflicting.xml).

