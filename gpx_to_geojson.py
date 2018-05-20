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
import logging
import os
import re
import sys
#
# Non-standard imports
#
from geojson import dumps, Feature, FeatureCollection, LineString, MultiLineString, Point
import gpxpy
import gpxpy.gpx
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
        for gpx_file in files:

            _path = os.path.dirname(gpx_file.name)
            _file = os.path.basename(gpx_file.name).split('.')[0] + '.geojson'
            output_file = os.path.sep.join([_path, _file])

            tracks = []

            # Parsing an existing file:
            _get_logger().info("Processing file: '%s'", gpx_file.name)
            _get_logger().info("Writing output to: '%s'", output_file)
            gpx = gpxpy.parse(gpx_file)

            for track in gpx.tracks:
                _get_logger().info("Processing track: '%s'", track.name)

                #properties={"country": "Spain"}
                segments = []
                for segment in track.segments:

                    points = []
                    for point in segment.points:
                        _get_logger().debug('Point at (%f,%f) -> %s', point.latitude,
                                            point.longitude, point.elevation)
                        points.append(Point((point.longitude, point.latitude)))

                    segments.append(LineString(points))
                tracks.append(Feature(geometry=MultiLineString(segments),
                                      properties={"name": track.name}))

            with open(output_file, 'w', encoding="utf8") as output_handle:
                output_handle.write(dumps(FeatureCollection(tracks)))
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
    parser = argparse.ArgumentParser(description='Take an existing GPX file convert it to GeoJSON')

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
