#!/usr/bin/env python

import argparse

from mythcli.services.dvr.controllers import expiring, recorded, upcoming

def main():
    # Create top-level parser
    parser = argparse.ArgumentParser(description="MythTV Services API command-line interface.")
    #parser.add_argument("-d", "--debug", action="store_const", const=True, default=False, help="set log level to debug")
    #parser.add_argument("-q", "--quiet", action="store_const", const=True, default=False, help="set log level to fatal")
    #parser.add_argument("-v", "--verbose", action="store_const", const=True, default=False, help="set log level to info")    
    parser.add_argument("--max-items", type=int, nargs=1, help="limit number of requested items. Default: no limit (0)")
    #parser.add_argument("--version", action="store_const", const=True, default=False, help="print version")    

    # Register subcommands
    #subparsers = parser.add_subparsers(title="subcommands", description="<valid subcommands>", help="<additional help>")
    subparsers = parser.add_subparsers(title="subcommands")
    expiring.add_subparser(subparsers)
    recorded.add_subparser(subparsers)
    upcoming.add_subparser(subparsers)

    # Parse the arguments and call whatever function (subcommand) was selected
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
