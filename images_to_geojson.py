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
import sys
from typing import Dict, Optional, Tuple

#
# Non-standard imports
#
import exifread
from exifread.utils import Ratio
from geojson import dumps, GeometryCollection, LineString, Point

#
# Ensure ./lib is in the lib path for local includes
#
sys.path.append(os.path.realpath(os.path.join(".", "lib")))
#
##############################################################################
#
# Global variables
#
DEFAULT_LOG_LEVEL = "WARNING"
#
##############################################################################
#
# _get_logger() - reusable code to get the correct logger by name
#
def _get_logger() -> logging.Logger:
    """_get_logger() - reuable code to get the correct logger by name"""
    return logging.getLogger(os.path.basename(__file__))


#
###############################################################################
#
# _convert_to_degress()
#
# Implementation from: https://gist.github.com/erans/983821
#


def _convert_to_degrees(
    value: Optional[Tuple[Ratio, Ratio, Ratio]] = None,
    degree: Optional[Ratio] = None,
    minute: Optional[Ratio] = None,
    second: Optional[Ratio] = None,
) -> float:
    """
    Helper function to convert the GPS coordinates stored in the EXIF
    to degrees in float format.

    Args:
        value (Tuple[Ratio, Ratio, Ratio]):
                                    A tuple containing the GPS coordinate values in the format
                                    (degree, minute, second)

        OR

        degree (Optional[Ratio]):    Degree portion of coordinates
        minute (Optional[Ratio]):    Minute portion of coordinates
        second (Optional[Ratio]):    Second portion of coordinates

    Raises:
        ValueError: If the input `value` is invalid.

    Returns:
        float: The GPS coordinate value in degrees.
    """
    if value and (degree and minute and second):
        raise RuntimeError("Given value array AND individual components. Choose one.")

    if value:
        degree = value[0]
        minute = value[1]
        second = value[2]

    if not (degree and minute and second):
        raise ValueError("Invalid value for GPS coordinates")

    n_degree = float(degree.num) / float(degree.den)
    n_minute = float(minute.num) / float(minute.den)
    n_second = float(second.num) / float(second.den)

    return n_degree + (n_minute / 60.0) + (n_second / 3600.0)


#
###############################################################################
#
# get_lat_lon_ele()
#
# Implementation from: https://gist.github.com/erans/983821
#
def get_lat_lon_ele(gps_info: Dict):
    """
    get_lat_lon_ele(gps_info) - Returns the latitude and longitude, if available
    """
    # pprint(gps_info)
    lat = lon = ele = None
    if gps_info:

        gps_altitude = gps_info.get("GPSAltitude", None)
        gps_latitude = gps_info.get("GPSLatitude", None)
        gps_latitude_ref = gps_info.get("GPSLatitudeRef", None)
        gps_longitude = gps_info.get("GPSLongitude", None)
        gps_longitude_ref = gps_info.get("GPSLongitudeRef", None)

        if None not in [
            gps_latitude,
            gps_latitude_ref,
            gps_longitude,
            gps_longitude_ref,
            gps_altitude,
        ]:
            lat = _convert_to_degrees(gps_latitude)

            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degrees(gps_longitude)
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
def process_directory(directory: str) -> LineString:
    """
    process_directory(directory=None) - Process all files in the given directory
    """

    if not directory:
        raise ValueError("No directory specified")

    track = []
    logger = _get_logger()
    for the_file in os.listdir(directory):
        image_file = os.sep.join([directory, the_file])

        logger.info("File is '%s'", image_file)
        if not os.path.isfile(image_file):
            logger.debug("Skipping non-file '%s'", image_file)
            continue

        gps_info = {}

        # Open image file for reading (binary mode)
        with open(image_file, mode="rb") as image:
            # Process Exif tags
            for tag, value in exifread.process_file(
                image, details=False
            ).items():  # pyright: ignore
                logger.debug("Tag: '%s'", tag)
                # All the ones we care about start with GPS
                if re.search("^GPS", tag):
                    logger.info("Tag: '%s'", tag)
                    key = tag.split(" ")[1]
                    logger.debug("Key: '%s', value '%s'", key, value)
                    # This .values does something odd: turns a string into a list
                    # *except* when the string is 1 alpha-char or already looks list like "[...]"
                    gps_info[key] = value.values

        (lat, lon, ele) = get_lat_lon_ele(gps_info)  # pylint: disable=unused-variable

        if lat and lon:
            track.append(Point((lon, lat)))

    return LineString(track)


#
###############################################################################
#
# is_directory()
#
def is_directory(argument: str):
    """
    is_directory(argument) - Argument validator for the CLI args
    """

    if os.path.isdir(argument):
        return argument

    error = f"{argument} is not a directory"
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
    parser = argparse.ArgumentParser(
        description=(
            "Take a directory of GPS tagged" " images and output GeoJSON LineString"
        )
    )

    parser.add_argument(
        "-d",
        "--directory",
        default=[],
        action="append",
        required=True,
        type=is_directory,
        help="Which directory of images to process. Repeat to "
        "process multiple directories.",
    )

    parser.add_argument(
        "--debug", default=False, action="store_true", help="Enable additional output"
    )

    parser.add_argument(
        "-l",
        "--log-level",
        action="store",
        required=False,
        choices=["debug", "info", "warning", "error", "critical"],
        default=DEFAULT_LOG_LEVEL,
        help=f"Logging verbosity. Default: {DEFAULT_LOG_LEVEL}",
    )

    args = parser.parse_args()

    # Enable the debug level logging when in debug mode
    args.log_level = "debug" if args.debug else args.log_level

    # Configure logging
    logging.basicConfig(
        format="%(levelname)s:%(module)s.%(funcName)s:%(message)s",
        level=getattr(logging, args.log_level.upper()),
    )

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


if __name__ == "__main__":
    main()
