#Images To GPX

Take a directory of GPS tagged images and output GPX

##Python

This code has been tested with Pythin 2.7.x

####Mac OS X El Capitan

If you are running Mac OS X El Capitan, consider leveraging [PyEnv](https://github.com/yyuu/pyenv) to install a non-global, more up-to-date Python.

###Initial Setup

To install all the things you need for your local Python environment:

    pip install -r ./requirements.txt

##Execution

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