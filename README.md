**Last Updated: 2016-06-06 08:34 @matthew-cox**

Table of Contents
=================
  * [Images To GPX](#images-to-gpx)
    * [Python](#python)
        * [Mac OS X El Capitan](#mac-os-x-el-capitan)
      * [Requirements](#requirements)
      * [Initial Setup](#initial-setup)
    * [Execution](#execution)
      * [Options](#options)
      * [Process A Directory](#process-a-directory)
      * [Process Multiple Directories](#process-multiple-directories)
    * [Hat Tip](#hat-tip)

#Images To GPX

Take a directory of GPS tagged images and output GPX

##Python

This code has been tested with Python 2.7.x

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
    usage: images_to_gpx.py [-h] -d DIRECTORY [--debug] [-l {debug,info,warning,error,critical}]

    Take a directory of GPS tagged images and output GPX track

    optional arguments:
      -h, --help            show this help message and exit
      -d DIRECTORY, --directory DIRECTORY
                            Which directory of images to process. Repeat to process multiple directories.
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

###Process Multiple Directories

    $ ./images_to_gpx.py -d ~/Pictures/2015/10/20 -d ~/Pictures/2015/10/21
    <?xml version="1.0" encoding="UTF-8"?>
    <gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd" version="1.0" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
    <trk>
    <trkseg>
    <trkpt lat="37.7969027778" lon="-122.405388889">
    <ele>15.8055727554</ele></trkpt>
    <trkpt lat="37.7954222222" lon="-122.404869444">
    <ele>5.84390243902</ele></trkpt></trkseg>
    <trkseg>
    <trkpt lat="37.7951305556" lon="-122.404786111">
    <ele>9.54981992797</ele></trkpt>
    <trkpt lat="37.7950555556" lon="-122.404555556">
    <ele>10.6586608443</ele></trkpt>
    <trkpt lat="37.7975388889" lon="-122.401947222">
    <ele>12.3848878394</ele></trkpt>
    <trkpt lat="37.8048277778" lon="-122.401038889">
    <ele>0.50634765625</ele></trkpt>
    <trkpt lat="37.8048277778" lon="-122.401038889">
    <ele>0.929656969171</ele></trkpt>
    <trkpt lat="37.8046333333" lon="-122.400825">
    <ele>4.00738552437</ele></trkpt>
    <trkpt lat="37.8053083333" lon="-122.400908333">
    <ele>3.31253071253</ele></trkpt>
    <trkpt lat="37.8045472222" lon="-122.400916667">
    <ele>1.78895162521</ele></trkpt>
    <trkpt lat="37.7951861111" lon="-122.40455">
    <ele>9.76016260163</ele></trkpt></trkseg></trk></gpx>

##Hat Tip

Thanks to [Eran Sandler](http://eran.sandler.co.il) for the example code (`_convert_to_degress` and `get_lat_lon`):

* [Extract GPS Latitude and Longitude Data from EXIF using Python Imaging Library (PIL)](http://eran.sandler.co.il/2011/05/20/extract-gps-latitude-and-longitude-data-from-exif-using-python-imaging-library-pil/)
* [Get Latitude and Longitude from EXIF using PIL](https://gist.github.com/erans/983821)
