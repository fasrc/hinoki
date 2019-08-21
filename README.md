# Hinoki

A python API wrapper and CI/CD scaffold for Sensu Go

## Overview

Hinoki uses a combination of code and convention to create a deployment
pipeline for Sensu checks, filters, assets, and handlers.  You can use 
just the API wrapper for your own purposes, or employ the folder 
convention and helper modules to set up your own CI/CD pipeline and treat
your Sensu configuration as code.

## Requirement & Installation

Requires Python > 3.7

#### Install:

The most expedient install method is pip:

```pip install hinoki```

Configuration is **required** for this app's commands to function properly!  Please see below.

#### Configure:

Create a ```config.yml``` file (example with documentation in docs/config.yml.example)
in a ```.hinoki``` folder in the home directory of the user which will run the commands.

```/home/[user]/.hinoki/config.yml```

There is an example configuration file in this repo, under docs/config.yml.example, which lists
each option and whether it is required.  There are several values which are explicitly required
and **will not work correctly with defaults**.  Please read the example config file and be
mindful of these values!

Hinoki expects a particular file structure convention in order to work properly.  An example
structure can be viewed in the data directory of this repository.  The example config file 
shows an example of using the `definition_base_dir` parameter to point to the directory you create.

Hinoki also requires a destination folder for packaged assets.  This can be any folder provided
that the user running hinoki has write permissions to it.  This directory can be configured using
the `assets_destination` parameter.

#### Run:

Available commands:

```Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  build-assets
  import
  init
  validate
```

  * **validate**: run through validation of all subfolders containing definitions.
   check for invalid json, and for file names that match object names.

  * **import**: run through all directories containing configuration and import their
   contents to the sensu api.  build assets, tar them, move them to a configurable 
   location, and automatically add the hashes of the built packages to the 
   asset definition files.

  * **init**: initialize a new sensu install from scratch; if you have a clean install,
   run this before running your imports.

  * **build-assets**: run only the build assets portion of the build - tar them, move them
   to a configurable location, and automatically add the hashes of the built packages to the 
   asset definition files.


## Building from Source:

This project uses setuptools for builds:

**Build:**

```python setup.py sdist bdist_wheel```

**Install:**

``pip install dist/hinoki-0.0.1-py2.py3-none-any.whl``

## Acknowledgements

@jtriley, who helped get me started creating a python project and provided 
code review, feedback, debugging help, and lots of other general assistance
with the project.

@jakedavis, who generously agreed to share the name 
[hinoki](https://sea-region.github.com/jakedavis) with me.  Great minds think alike!

