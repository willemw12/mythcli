mythcli
=======

Mythcli is a partially implemented command-line interface of the MytTV Services API.


Features
--------

Mythcli runs in Python 3 (3.2). Mythcli v0.1 runs in Python 2 (2.7).

It contains only a few MythTV DVR get requests and returns the response in RSS 2.0 format.

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
    00  0  *   *   *     mythcli --date-format "%a %B %d, %Y" --time-format "%I:%M %p" upcoming --link http://www.example.com/mythcli/dvr/upcoming.xml --url http://mythbackend:6544/Dvr/GetUpcomingList?ShowAll=false > /var/www/mythcli/dvr/upcoming.xml

Or to get notified in an RSS feed about programs that won't be recorded because of a conflict:

    # m h  dom mon dow   command
    00  0  *   *   *     mythcli conflicting --link http://www.example.com/mythcli/dvr/conflicting.xml --url http://mythbackend:6544/Dvr/GetConflictList > /var/www/mythcli/dvr/conflicting.xml
