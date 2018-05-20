#!/usr/bin/env python
"""
Take a directory of GPS tagged images and produce a GPX track file
"""
#
# Standard imports
#
from __future__ import print_function
import argparse
import logging
import os
import re
#
# Non-standard imports
#
import exifread
from geojson import dumps, GeometryCollection, LineString, Point
#
# Ensure ./lib is in the lib path for local includes
#
sys.path.append(os.path.realpath(os.path.join('.', 'lib')))
#
##############################################################################
#
# Global variables
#
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
# _convert_to_degress()
#
# Implementation from: https://gist.github.com/erans/983821
#
def _convert_to_degress(value=None):
    """
    Helper function to convert the GPS coordinates stored in the EXIF
    to degress in float format
    """
    result = None
    if None not in [value]:
        degree = value[0]
        degree = float(degree.num) / float(degree.den)

        minute = value[1]
        minute = float(minute.num) / float(minute.den)

        second = value[2]
        second = float(second.num) / float(second.den)

        result = degree + (minute / 60.0) + (second / 3600.0)

    return result
#
###############################################################################
#
# get_lat_lon_ele()
#
# Implementation from: https://gist.github.com/erans/983821
#
def get_lat_lon_ele(gps_info):
    """
    get_lat_lon_ele(gps_info) - Returns the latitude and longitude, if available
    """
    #pprint(gps_info)
    lat = lon = ele = None
    if None not in [gps_info]:

        gps_altitude = gps_info.get("GPSAltitude", None)
        gps_latitude = gps_info.get("GPSLatitude", None)
        gps_latitude_ref = gps_info.get('GPSLatitudeRef', None)
        gps_longitude = gps_info.get('GPSLongitude', None)
        gps_longitude_ref = gps_info.get('GPSLongitudeRef', None)

        if None not in [gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref,
                        gps_altitude]:
            lat = _convert_to_degress(gps_latitude)

            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

            if gps_altitude[0].den:
                ele = float(gps_altitude[0].num) / float(gps_altitude[0].den)

    return lat, lon, ele
#
###############################################################################
#
# process_directory()
#
def process_directory(directory=None):
    '''
    process_directory(directory=None) - Process all files in the given directory
    '''

    track = []

    if None in [directory]:
        _get_logger().warning("Missing arguments!")
    else:
        for the_file in os.listdir(directory):
            image_file = os.sep.join([directory, the_file])

            _get_logger().info("File is '%s'", image_file)
            if os.path.isfile(image_file):
                # Open image file for reading (binary mode)
                file_handle = open(image_file, 'rb')

                # Return Exif tags
                try:
                    tags = exifread.process_file(file_handle, details=False)
                except (Exception) as err:
                    raise err

                gps_info = {}

                for tag, value in tags.items():

                    if re.search('^GPS', tag):
                        _get_logger().debug("Tag: '%s'", tag)
                        split = tag.split(' ')
                        key = split[1]
                        _get_logger().debug("Key: '%s', value '%s'", key, value)
                        gps_info[key] = tags[tag].values

                # pylint: disable=unused-variable
                (lat, lon, ele) = get_lat_lon_ele(gps_info)

                if lat and lon:
                    track.append(Point((lon, lat)))

    return LineString(track)
#
###############################################################################
#
# is_directory()
#
def is_directory(argument):
    '''
    is_directory(argument) - Argument validator for the CLI args
    '''

    if os.path.isdir(argument):
        return argument
    else:
        error = "{} is not a directory".format(argument)
        raise argparse.ArgumentTypeError(error)
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
    parser = argparse.ArgumentParser(description=('Take a directory of GPS tagged'
                                                  ' images and output GPX track'))

    parser.add_argument('-d', '--directory', default=[], action='append',
                        required=True, type=is_directory,
                        help='Which directory of images to process. Repeat to '
                        'process multiple directories.')

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

    tracks = []

    for directory in args.directory:
        # Create a segment in our GPX track:
        tracks.append(process_directory(directory))

    # Only make a collection if there is more than one track
    if len(tracks) > 1:
        print(dumps(GeometryCollection(tracks)))
    else:
        print(dumps(tracks[0]))

if __name__ == '__main__':
    main()
