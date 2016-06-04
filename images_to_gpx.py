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
# _convert_to_degress() - borrowed from somewhere. source to come
#
def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF
    to degress in float format
    """
    #print dumper.dump( value )
    # pylint: disable=invalid-name
    d0 = value[0].num
    d1 = value[0].den
    d = float(d0) / float(d1)

    m0 = value[1].num
    m1 = value[1].den
    m = float(m0) / float(m1)

    s0 = value[2].num
    s1 = value[2].den
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)
#
###############################################################################
#
# get_lat_lon_ele() - borrowed from somewhere. source to come
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
            # pylint: disable=invalid-name
            e0 = gps_altitude[0].num
            e1 = gps_altitude[0].den
            ele = float(e0) / float(e1)

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
                        help='Which directories of images to process')

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
    print gpx.to_xml()

if __name__ == '__main__':
    main()
