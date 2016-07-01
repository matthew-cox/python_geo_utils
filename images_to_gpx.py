#!/usr/bin/env python
"""
Take a directory of GPS tagged images and produce a GPX track file
"""
import argparse
import logging
import os
import re
import time

import exifread
import gpxpy.gpx

DEFAULT_LOG_LEVEL = 'warning'
#
###############################################################################
#
# _convert_to_degress()
#
# Implementation from: https://gist.github.com/erans/983821
#
def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF
    to degress in float format
    """
    degree = value[0]
    degree = float(degree.num) / float(degree.den)

    minute = value[1]
    minute = float(minute.num) / float(minute.den)

    second = value[2]
    second = float(second.num) / float(second.den)

    return degree + (minute / 60.0) + (second / 3600.0)
#
###############################################################################
#
# clean_output()
#
def clean_output(output=None):
    '''
    clean_output(output=None)

    Remove extra EOLs from gpx.to_xml()
    '''
    if output:
        # remove some superfluous EOLs
        point_pattern = re.compile(r'^(<trkpt [^>]*>)\n', re.MULTILINE)
        elevation_pattern = re.compile(r'^(.*</ele>)\n', re.MULTILINE)
        output = point_pattern.sub(r"\1", output)
        output = elevation_pattern.sub(r"\1", output)
    return output
#
###############################################################################
#
# get_lat_lon_ele()
#
# Implementation from: https://gist.github.com/erans/983821
#
def get_lat_lon_ele(gps_info):
    """
    get_lat_lon_ele(gps_info)

    Returns the latitude and longitude, if available
    """
    #pprint(gps_info)
    lat = None
    lon = None
    ele = None

    gps_altitude = gps_info.get("GPSAltitude", None)
    gps_latitude = gps_info.get("GPSLatitude", None)
    gps_latitude_ref = gps_info.get('GPSLatitudeRef', None)
    gps_longitude = gps_info.get('GPSLongitude', None)
    gps_longitude_ref = gps_info.get('GPSLongitudeRef', None)

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref and gps_altitude:
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
    process_directory(directory=None)

    Process all files in the given directory
    '''

    track = {}

    if None in [directory]:
        logging.warn("Missing arguments!")
        return track

    for the_file in os.listdir(directory):
        image_file = os.sep.join([directory, the_file])

        logging.info("File is '%s'", image_file)
        if os.path.isfile(image_file):
            # Open image file for reading (binary mode)
            file_handle = open(image_file, 'rb')

            # Return Exif tags
            try:
                tags = exifread.process_file(file_handle, details=False)
            except Exception, err:
                raise err

            gps_info = {}
            date = None

            for tag in tags.keys():
                if re.search('^GPS', tag):
                    logging.debug("Tag: '%s'", tag)
                    split = tag.split(' ')
                    key = split[1]
                    logging.debug("Key: '%s', value '%s'", key, tags[tag])
                    gps_info[key] = tags[tag].values

                if tag == 'Image DateTime':
                    logging.debug("Key: '%s', value '%s'", tag, tags[tag])
                    #pprint(tags[tag])
                    date = time.strptime(tags[tag].values, '%Y:%m:%d %H:%M:%S')

            (lat, lon, ele) = get_lat_lon_ele(gps_info)

            if lat and lon and ele:
                track[time.mktime(date)] = gpxpy.gpx.GPXTrackPoint(lat, lon,
                                                                   elevation=ele)
    return track
#
###############################################################################
#
# is_directory()
#
def is_directory(argument):
    '''
    is_directory(argument)

    Argument validator for the CLI args
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

    gpx = gpxpy.gpx.GPX()
    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    for directory in args.directory:
        # Create a segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        track = process_directory(directory)

        for track_time in sorted(track.iterkeys()):
            #pprint(track[track_time])
            gpx_segment.points.append(track[track_time])

    #pprint(track)
    print clean_output(gpx.to_xml())

if __name__ == '__main__':
    main()
