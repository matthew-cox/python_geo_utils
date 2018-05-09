#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
'''
Take a GPX file and output a GeoJSON representation
'''
#
# Standard Imports
#
from __future__ import print_function
import argparse
import json
import logging
import os
import sys
#
# Non-standard imports
#
from geojson import dumps, Feature, LineString, Point
#
# Ensure ./lib is in the lib path for local includes
#
sys.path.append(os.path.realpath(os.path.join('.', 'lib')))
#
##############################################################################
#
# Global variables
#
DEFAULT_DISTANCE = 0.08
DEFAULT_LOG_LEVEL = 'warning'
#
##############################################################################
#
# _get_logger() - reusable code to get the correct logger by name
#
def _get_logger():
    '''_get_logger() - reuable code to get the correct logger by name'''
    return logging.getLogger(os.path.basename(__file__))
#
###############################################################################
#
# process_files()
#
def process_files(files=None):
    '''
    process_files(files=[], distance=DEFAULT_DISTANCE)
    '''

    if None not in [files]:
        for points_file in files:

            _path = os.path.dirname(points_file.name)
            _file = os.path.basename(points_file.name).split('.')[0] + '.geojson'
            output_file = os.path.sep.join([_path, _file])

            # Parsing an existing file:
            _get_logger().info("Processing file: '%s'", points_file.name)
            _get_logger().info("Writing output to: '%s'", output_file)

            file_points = json.load(points_file)
            points = []

            for point in file_points.get('points'):
                _get_logger().debug('Point at (%f,%f)', point[0], point[1])
                points.append(Point((point[1], point[0])))

            with open(output_file, 'w', encoding="utf8") as output_handle:
                output_handle.write(dumps(Feature(geometry=LineString(points),
                                                  properties={"name":
                                                              os.path.basename(points_file.name)})))

#
###############################################################################
#
# main()
#
def main():
    """
    Main function to do the work
    """
    #
    # Handle CLI args
    #
    parser = argparse.ArgumentParser(description='Take JSON of points and convert it to GeoJSON')

    parser.add_argument('-f', '--files', default=[], action='append',
                        required=True, type=argparse.FileType('r'),
                        help='Which GPX file to process. Repeat to '
                        'process multiple files.')

    parser.add_argument('--debug', default=False, action='store_true',
                        help='Enable additional output')

    parser.add_argument('-l', '--log-level', action='store', required=False,
                        choices=["debug", "info", "warning", "error", "critical"],
                        default=DEFAULT_LOG_LEVEL,
                        help='Logging verbosity. Default: {}'.format(DEFAULT_LOG_LEVEL))

    args = parser.parse_args()

    # Enable the debug level logging when in debug mode
    if args.debug:
        args.log_level = 'debug'

    # Configure logging
    logging.basicConfig(format='%(levelname)s:%(module)s.%(funcName)s:%(message)s',
                        level=getattr(logging, args.log_level.upper()))

    _get_logger().info("Log level is '%s'", args.log_level.upper())

    process_files(files=args.files)

if __name__ == '__main__':
    main()
