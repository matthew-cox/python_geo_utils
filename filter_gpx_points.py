#!/usr/bin/env python
'''
Take a GPX file and remove some points based on distance between them
'''
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
import gpxpy
import gpxpy.gpx
import latlon
#
##############################################################################
#
# Global variables
#
DEFAULT_DISTANCE = 0.08
DEFAULT_LOG_LEVEL = 'WARNING'
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
# process_track()
#
def process_track(track=None, spacing=None):
    '''
    process_track(track, spacing) - Take a GPX track and filter it to points at least spacing apart
    '''
    gpx_track = None
    if None not in [track]:
        orig_num_points = new_num_points = 0
        spacing = spacing if spacing else DEFAULT_DISTANCE

        _get_logger().info("Processing track: '%s'", track.name)
        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_track.name = track.name + " (filtered to {})".format(spacing)

        for segment in track.segments:
            # Create a segment in our GPX track:
            new_segment = gpxpy.gpx.GPXTrackSegment()

            current_point = previous_point = None

            for point in segment.points:
                orig_num_points += 1
                _get_logger().debug('Point at (%f,%f) -> %s', point.latitude, point.longitude,
                                    point.elevation)
                current_point = LatLon.LatLon(point.latitude, point.longitude)
                if not previous_point:
                    _get_logger().debug('No previous point!')
                    previous_point = current_point
                    new_segment.points.append(point)
                    new_num_points += 1
                else:
                    distance = previous_point.distance(current_point)
                    _get_logger().debug('Distance between points: %f', distance)
                    if distance >= spacing:
                        previous_point = current_point
                        new_segment.points.append(point)
                        new_num_points += 1

            gpx_track.segments.append(new_segment)

        _get_logger().info("Reduced points from '%s' to '%s'", orig_num_points, new_num_points)

    return gpx_track

#
###############################################################################
#
# process_files()
#
def process_files(files=None, spacing=None):
    '''
    process_files(files=[], spacing=DEFAULT_DISTANCE)
    '''

    if None in [files]:
        raise RuntimeError("No files to process!")

    spacing = spacing or DEFAULT_DISTANCE

    for gpx_file in files:
        new_gpx = gpxpy.gpx.GPX()

        # Parsing an existing file:
        _get_logger().info("Processing file: '%s'", gpx_file)
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            new_gpx.tracks.append(process_track=track, spacing=spacing)

        print(clean_output(new_gpx.to_xml()))

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
# main()
#
def main():
    """
    Main function to do the work
    """
    #
    # Handle CLI args
    #
    parser = argparse.ArgumentParser(description=('Take an existing GPX file and filter the points '
                                                  'to only those a certain distance apart.'))

    parser.add_argument('-f', '--files', default=[], action='append',
                        required=True, type=argparse.FileType('r'),
                        help='Which GPX file to process. Repeat to '
                        'process multiple files.')

    parser.add_argument('--debug', default=False, action='store_true',
                        help='Enable additional output')

    parser.add_argument('-d', '--distance', default=DEFAULT_DISTANCE,
                        action='store', type=float,
                        help=('Minimum distance between points for inclusion. '
                              'Default: {}'.format(DEFAULT_DISTANCE)))

    parser.add_argument('-l', '--log-level', action='store', required=False,
                        choices=["debug", "info", "warning", "error", "critical"],
                        default=DEFAULT_LOG_LEVEL,
                        help='Logging verbosity. Default: {}'.format(DEFAULT_LOG_LEVEL))

    args = parser.parse_args()

    # Enable the debug level logging when in debug mode
    args.log_level = 'debug' if args.debug else args.log_level

    # Configure logging
    logging.basicConfig(format='%(levelname)s:%(module)s.%(funcName)s:%(message)s',
                        level=getattr(logging, args.log_level.upper()))

    _get_logger().info("Log level is '%s'", args.log_level.upper())

    process_files(files=args.files, spacing=args.distance)

if __name__ == '__main__':
    main()
