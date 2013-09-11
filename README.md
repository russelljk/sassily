#Sassily

##Overview

Sassily is a management command for Django that converts scss files to css and can optionally watch the directory for changes.

##License

Sassily is released under the zlib license and can be used for personal, commercial and educational purposes. See the `LICENSE` file in the root directory.

##Requirements

* **Django** - [https://www.djangoproject.com/]()
* **Sass** - [http://sass-lang.com/]()

Optional

* **Compass** - [http://compass-style.org/]()

##Quick Start

###Installation

Install directly from **GitHub**:

    $ git clone git://github.com/russelljk/django-sassily.git
    $ cd django-sassily
    $ python setup.py install

###Configuration
    
Add the following to your Django `settings.py`. 

    SASSILY_SRC_DIR = '/path/to/your/scss/files'
    SASSILY_DEST_DIR = '/path/to/static/css'

These are the source and destination directories. Source should contain any scss files. The destination will contain the finished css files. Don't place a trailing slash on the directories.

Install `sassily` by adding it to `INSTALLED_APPS`.

    INSTALLED_APPS = (
        ...
        'sassily',
    )

####Using Compass

Make sure you have Compass installed and add the following to your settings.

    SASSILY_USE_COMPASS = True

###Structure

Next copy all scss files into the `SASSILY_SRC_DIR` directory. You might want to consider a directory structure like the following:

    /project
        /scss
            /src
                style.scss
                print.scss
            /imports
                ...
            
In the above example all your scss files go into `project/scss/src`. Make sure to set `SASSILY_SRC_DIR` to that directory as well. 

Any .scss files in source directory, and any subdirectories, are automatically converted and moved to `SASSILY_DEST_DIR`. For that reason place any shared or imported .scss files in a sister directory and use a relative import to access them.

    @import "../imports/basics.scss";

###Running sassily

Note that if you have style.scss in the source directory any file named style.css in the destination directory **will be overwritten**.

    ./manage.py sassily

In addition the following options are availiable.

    --watch, -w
        Watches a directory for changes.
    
    --compress, -c
        Compress all css files. 
