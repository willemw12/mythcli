mythcli
=======

Mythcli is a Python program to generate MythTV RSS feeds, for example of upcoming or conflicting recordings.


Features
--------

Mythcli is a partially implemented command-line interface of the MythTV Services API (MythTV versions .25 and higher). It supports only a few MythTV DVR Service requests and returns the response in RSS 2.0 format. Mythcli runs on Python 3 (3.2 or higher).

To view the available mythcli commands and options, run:

    ./src/mythcli.py --help

and

    ./src/mythcli.py <subcommand> --help

This program is licensed under GPLv3 (see included file COPYING).


Usage
-----

Optionally, create a symbolic link of mythcli.py in a directory of $PATH. From this directory, run:

    ln -s $(pwd)/src/mythcli.py ~/bin/mythcli

To update, for example, an RSS feed of upcoming MythTV recordings once a day on your local web server, create a similar cron job listed below. All arguments are optional:

    # m h  dom mon dow   command
    00  0  *   *   *     mythcli --date-format "%a %B %d, %Y" --time-format "%I:%M %p" upcoming --feed-url http://www.example.com/mythcli/dvr/upcoming.xml --service-url http://mythbackend:6544/Dvr/GetUpcomingList?ShowAll=false --mythweb-base-url http://mythbackend > /var/www/mythcli/dvr/upcoming.xml

Or to get notified in an RSS feed about programs that won't be recorded because of conflicts:

    # m h  dom mon dow   command
    00  0  *   *   *     mythcli conflicting --conflicting-with --feed-url http://www.example.com/mythcli/dvr/conflicting.xml --service-url http://mythbackend:6544/Dvr/GetConflictList > /var/www/mythcli/dvr/conflicting.xml
