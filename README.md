**Last Updated: 2018-05-20 14:23 @matthew-cox**

Table of Contents
=================
  * [Python Geo Utilities](#python-geo-utilities)
    * [Python](#python)
        * [Pyenv + Virtualenv](#pyenv--virtualenv)
      * [Non-standard Requirements](#non-standard-requirements)
      * [Initial Setup](#initial-setup)
        * [Configure Local Python Virtualenv](#configure-local-python-virtualenv)
    * [Filter GPX Points](#filter-gpx-points)
      * [Execution](#execution)
        * [Options](#options)
        * [Process A GPX File](#process-a-gpx-file)
    * [GPX To GeoJSON](#gpx-to-geojson)
      * [Execution](#execution-1)
        * [Options](#options-1)
    * [Images To GeoJSON](#images-to-geojson)
      * [Execution](#execution-2)
        * [Options](#options-2)
        * [Process A Directory](#process-a-directory)
        * [Process Multiple Directories](#process-multiple-directories)
    * [Images To GPX](#images-to-gpx)
      * [Execution](#execution-3)
        * [Options](#options-3)
        * [Process A Directory](#process-a-directory-1)
        * [Process Multiple Directories](#process-multiple-directories-1)
    * [Points To GeoJSON](#points-to-geojson)
      * [Execution](#execution-4)
        * [Options](#options-4)
    * [Hat Tip](#hat-tip)

# Python Geo Utilities

Small collection of Python scripts for working with GPS, GPX, and GeoJSON. Included:

* [Filter GPX Points](#filter-gpx-points)
* [GPX To GeoJSON](#gpx-to-geojson)
* [Images To GPX](#images-to-gpx)
* [Points To GeoJSON](#points-to-geojson)

## Python

This code has been tested with Python 2.7.x and 3.6.x

#### Pyenv + Virtualenv

Consider leveraging [PyEnv](https://github.com/yyuu/pyenv) to install a non-global, more up-to-date Python.

### Non-standard Requirements

* [ExifRead](https://pypi.python.org/pypi/ExifRead/)
* [geojson](https://github.com/frewsxcv/python-geojson)
* [gpxpy](https://github.com/tkrajina/gpxpy)
* [LatLon](https://pypi.python.org/pypi/LatLon/1.0.2)

### Initial Setup

#### Configure Local Python Virtualenv

    # install newish python 3.6.x
    $ pyenv install 3.6.5

    # create a repo specific virtualenv
    $ pyenv virtualenv 3.6.5 python_geo_utils-36

    # switch to the new virtualenv
    $ pyenv local python_geo_utilis-36

    # ensure that pip and setuptools are new
    $ pip install --upgrade pip setuptools

    # install all the requirements
    $ pip install -r ./requirements.txt

## Filter GPX Points

Take an existing GPX file and filter the points to include only those a certain distance apart.

### Execution

#### Options

    $ ./filter_gpx_points.py -h
    usage: filter_gpx_points.py [-h] -f FILES [--debug] [-d DISTANCE] [-l {debug,info,warning,error,critical}]

    Take an existing GPX file and filter the points to include only those a certain distance apart.

    optional arguments:
      -h, --help            show this help message and exit
      -f FILES, --files FILES
                            Which GPX file to process. Repeat to process multiple files.
      --debug               Enable additional output
      -d DISTANCE, --distance DISTANCE
                            Minimum distance between points for inclusion. Default: 0.08
      -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                            Logging verbosity. Default: warning

#### Process A GPX File

<details>
  <summary><code>$ ./filter_gpx_points.py -l info -f ./test.gpx | head</code></summary>

```xml
INFO:filter_gpx_points.process_files:Processing file: '<open file './test.gpx', mode 'r' at 0x10e71ded0>'
INFO:filter_gpx_points.process_files:Processing track: '2016/6/16 7:43:3 GMT'
INFO:filter_gpx_points.process_files:Reduced points from '480' to '122'
<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd" version="1.0" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
<trk>
<name>2016/6/16 7:43:3 GMT</name>
<trkseg>
<trkpt lat="59.33191" lon="18.03158667"><ele>112.0</ele><time>2016-06-16T07:43:03Z</time></trkpt>
<trkpt lat="59.331195" lon="18.03086333"><ele>39.0</ele><time>2016-06-16T07:45:34Z</time></trkpt>
<trkpt lat="59.33065333" lon="18.032735"><ele>79.0</ele><time>2016-06-16T07:46:34Z</time></trkpt>
<trkpt lat="59.33027333" lon="18.03428667"><ele>111.0</ele><time>2016-06-16T07:47:34Z</time></trkpt>
<trkpt lat="59.32986167" lon="18.03614167"><ele>63.0</ele><time>2016-06-16T07:49:04Z</time></trkpt>
```

</details>

## GPX To GeoJSON

Take GPX files and create a GeoJSON equivilant.

### Execution

#### Options

    $ ./gpx_to_geojson.py -h

    usage: gpx_to_geojson.py [-h] -f FILES [--debug] [-l {debug,info,warning,error,critical}]

    Take an existing GPX file convert it to GeoJSON

    optional arguments:
      -h, --help            show this help message and exit
      -f FILES, --files FILES
                            Which GPX file to process. Repeat to process multiple files.
      --debug               Enable additional output
      -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                            Logging verbosity. Default: warning

## Images To GeoJSON

Take a directory of GPS tagged images and output GPX file representing the tracks.

### Execution

#### Options

    $ ./images_to_geojson.py --help

    usage: images_to_geojson.py [-h] -d DIRECTORY [--debug] [-l {debug,info,warning,error,critical}]

    Take a directory of GPS tagged images and output GeoJSON LineString

    optional arguments:
      -h, --help            show this help message and exit
      -d DIRECTORY, --directory DIRECTORY
                            Which directory of images to process. Repeat to process multiple directories.
      --debug               Enable additional output
      -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                            Logging verbosity. Default: warning


#### Process A Directory

<details>
  <summary><code>$ ./images_to_geojson.py -d ~/Pictures/2015/10/20</code></summary>

```json
{"type": "LineString", "coordinates": [[-122.405388889,37.7969027778], [-122.404869444,37.7954222222]]}
```

</details>

#### Process Multiple Directories

<details>
  <summary><code>$ ./images_to_gpx.py -d ~/Pictures/2015/10/20 -d ~/Pictures/2015/10/21</code></summary>

```json
{"type": "GeometryCollection", "geometries": [{"type": "LineString", "coordinates": [[-122.405388889,37.7969027778],[-122.404869444,37.7954222222]]}, {"type": "LineString", "coordinates": [[-122.404786111,37.7951305556],[-122.404555556,37.7950555556],[-122.401947222,37.7975388889],[-122.401038889,37.8048277778],[-122.401038889,37.8048277778],[-122.400825,37.8046333333],[-122.400908333,37.8053083333],[-122.400916667,37.8045472222],[-122.40455,37.7951861111]]}]}
```

</details>

## Images To GPX

Take a directory of GPS tagged images and output GPX file representing the tracks.

### Execution

#### Options

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

#### Process A Directory

<details>
  <summary><code>$ ./images_to_gpx.py -d ~/Pictures/2015/10/20</code></summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd" version="1.0" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
<trk>
<trkseg>
<trkpt lat="37.7969027778" lon="-122.405388889"><ele>15.8055727554</ele></trkpt>
<trkpt lat="37.7954222222" lon="-122.404869444"><ele>5.84390243902</ele></trkpt></trkseg></trk></gpx>
```

</details>

#### Process Multiple Directories

<details>
  <summary><code>$ ./images_to_gpx.py -d ~/Pictures/2015/10/20 -d ~/Pictures/2015/10/21</code></summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd" version="1.0" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
<trk>
<trkseg>
<trkpt lat="37.7969027778" lon="-122.405388889"><ele>15.8055727554</ele></trkpt>
<trkpt lat="37.7954222222" lon="-122.404869444"><ele>5.84390243902</ele></trkpt></trkseg>
<trkseg>
<trkpt lat="37.7951305556" lon="-122.404786111"><ele>9.54981992797</ele></trkpt>
<trkpt lat="37.7950555556" lon="-122.404555556"><ele>10.6586608443</ele></trkpt>
<trkpt lat="37.7975388889" lon="-122.401947222"><ele>12.3848878394</ele></trkpt>
<trkpt lat="37.8048277778" lon="-122.401038889"><ele>0.50634765625</ele></trkpt>
<trkpt lat="37.8048277778" lon="-122.401038889"><ele>0.929656969171</ele></trkpt>
<trkpt lat="37.8046333333" lon="-122.400825"><ele>4.00738552437</ele></trkpt>
<trkpt lat="37.8053083333" lon="-122.400908333"><ele>3.31253071253</ele></trkpt>
<trkpt lat="37.8045472222" lon="-122.400916667"><ele>1.78895162521</ele></trkpt>
<trkpt lat="37.7951861111" lon="-122.40455"><ele>9.76016260163</ele></trkpt></trkseg></trk></gpx>
```

</details>

## Points To GeoJSON

Take a JSON file of `Lat, Lng` pairs and convert to GeoJSON

### Execution

#### Options

    $ ./points_to_geojson.py -h

    usage: points_to_geojson.py [-h] -f FILES [--debug] [-l {debug,info,warning,error,critical}]

    Take JSON of points and convert it to GeoJSON

    optional arguments:
      -h, --help            show this help message and exit
      -f FILES, --files FILES
                            Which GPX file to process. Repeat to process multiple files.
      --debug               Enable additional output
      -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                            Logging verbosity. Default: warning

## Hat Tip

Thanks to [Eran Sandler](http://eran.sandler.co.il) for the example code (`_convert_to_degress` and `get_lat_lon`):

* [Extract GPS Latitude and Longitude Data from EXIF using Python Imaging Library (PIL)](http://eran.sandler.co.il/2011/05/20/extract-gps-latitude-and-longitude-data-from-exif-using-python-imaging-library-pil/)
* [Get Latitude and Longitude from EXIF using PIL](https://gist.github.com/erans/983821)
