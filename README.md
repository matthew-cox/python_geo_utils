#Images To GPX

Take a directory of GPS tagged images and output GPX

##Python

This code has been tested with Pythin 2.7.x

####Mac OS X El Capitan

If you are running Mac OS X El Capitan, consider leveraging [PyEnv](https://github.com/yyuu/pyenv) to install a non-global, more up-to-date Python.

###Requirements

* [ExifRead](https://pypi.python.org/pypi/ExifRead/)
* [gpxpy](https://github.com/tkrajina/gpxpy)

###Initial Setup

To install all the things you need for your local Python environment:

    pip install -r ./requirements.txt

##Execution

###Options

    $ ./images_to_gpx.py -h
    usage: images_to_gpx.py [-h] [-d DIRECTORY] [--debug] [-l {debug,info,warning,error,critical}]

    Take a directory of GPS tagged images and output GPX track

    optional arguments:
      -h, --help            show this help message and exit
      -d DIRECTORY, --directory DIRECTORY
                            Which directory of images to process
      --debug               Enable additional output
      -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                            Logging verbosity. Default: warning

###Process A Directory

    $ ./images_to_gpx.py -d ~/Pictures/2015/10/20
    <?xml version="1.0" encoding="UTF-8"?>
    <gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd" version="1.0" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
    <trk>
    <trkseg>
    <trkpt lat="37.7969027778" lon="-122.405388889">
    <ele>15.8055727554</ele></trkpt>
    <trkpt lat="37.7954222222" lon="-122.404869444">
    <ele>5.84390243902</ele></trkpt></trkseg></trk></gpx>
