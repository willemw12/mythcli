#!/usr/bin/env python3

import argparse

from mythcli.services.dvr.controllers import conflicting, expiring, recorded, upcoming

def main():
    """ For all datetime format codes, see http://docs.python.org/library/datetime.html#strftime-and-strptime-behavior """
    
    # Create top-level parser
    parser = argparse.ArgumentParser(description="MythTV Services API command-line interface.")
    #parser.add_argument("--debug", action="store_const", const=True, default=False, help="set log level to debug")
    #parser.add_argument("--quiet", action="store_const", const=True, default=False, help="set log level to fatal")
    #parser.add_argument("--verbose", action="store_const", const=True, default=False, help="set log level to info")
    parser.add_argument("-d", "--date-format", nargs=1, default=["%a %d %B, %Y"], help='examples: "%%Y-%%m-%%d", "%%a %%d %%B, %%Y", "%%x"')
    parser.add_argument("-m", "--max-items", type=int, nargs=1, default=[0], help="limit number of requested items. Default: no limit (0)")
    parser.add_argument("-t", "--time-format", nargs=1, default=["%H:%M"], help='examples: "%%H:%%M", "%%I:%%M %%p", "%%X"')
    #parser.add_argument("--version", action="store_const", const=True, default=False, help="print version")    

    # Register subcommands
    #subparsers = parser.add_subparsers(title="subcommands", description="<valid subcommands>", help="<additional help>")
    subparsers = parser.add_subparsers(title="subcommands")
    conflicting.add_subparser(subparsers)
    expiring.add_subparser(subparsers)
    recorded.add_subparser(subparsers)
    upcoming.add_subparser(subparsers)

    # Parse the arguments and call whatever function (subcommand) was selected
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
