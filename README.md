mythcli
=======

Mythcli is a partially implemented command-line interface of the MytTV Services API in Python 2.

It contains only a few MythTV DVR get requests and returns the response in RSS 2.0 format.

To view the available mythcli commands and options, run:

    ./src/mythcli.py --help

and

    ./src/mythcli.py <subcommand> --help

Optionally, create a symbolic link of mythcli.py to a directory in $PATH. For example, from this directory:

    ln -s $(pwd)/src/mythcli.py ~/bin/mythcli.py

For example, to update an RSS feed of upcoming MythTV recordings once a day, create a similar cron job listed below (all arguments are optional):

    # m h  dom mon dow   command
    00  0  *   *   *     mythcli.py --date-format "%a %B %d, %Y" --time-format "%I:%M %p" upcoming --link http://www.example.com/mythcli/dvr/upcoming.xml --url http://mythbackend:6544/Dvr/GetUpcomingList?ShowAll=false > /var/www/mythcli/dvr/upcoming.xml

This program is licensed under GPLv3 (see included file COPYING).
