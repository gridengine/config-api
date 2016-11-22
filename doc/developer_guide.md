# UGE Python Configuration Library - Developer Guide

## Prerequisites

UGE PyCL requires recent versions of the following software:

1. UGE (8.3.1p9, 8.4.0)
2. Python (v2.7.5 or later in v2.7 series)
3. Setuptools (0.9.8 or later; for egg installation)
4. Nose (1.3.7 or later; for testing)
5. Sphinx (1.1.3 or later; for generating documentation)
6. Standard development tools (make

The software versions listed above were used for prototype development and
testing, on CentOS 7.2 (64-bit). It is likely that any recent version of 
Python (such as those that come with current linux distributions) should work. However, at the moment the only supported UGE versions are 8.3.1p9 and 8.4.0

## Build

In the top level directory run:

```sh
  $ make 
```

The above command will create UGE PyCL egg package in the `dist` directory, which can be installed using the `easy_install` command. It will also run `sphinx-build` command and generate HTML documentation in the `dist/doc/html` directory.

## Basic API Usage

For simple testing, without installing UGE PyCL egg package, do the following:

1) Setup PYTHONPATH environment variable to point to the top level directory:

```sh
  $ export PYTHONPATH=<UGE_PYCL_ROOT>
```

Note that the above step is not needed if UGE PyCL egg package is installed.

2) Source the appropriate UGE setup file:

```sh
  $ source <SGE_ROOT>/<SGE_CELL>/settings.sh
```

3) List queues using QconfApi object:

```sh
  $ python -c "from uge.api import QconfApi; api = QconfApi(); print api.list_queues()"
```

## Running Test Suite

1) Setup PYTHONPATH environment variable to point to the top level directory:

```sh
  $ export PYTHONPATH=<UGE_PYCL_ROOT>
```

This step is not needed if UGE PyCL egg package is installed.

2) Source the appropriate UGE setup file:

```sh
  $ source <SGE_ROOT>/<SGE_CELL>/settings.sh
```

3) Run test suite:

```sh
  $ make test 
```

## Library Development 

### Source Code 

UGE PyCL python code contains several submodules under the top level 'uge'
directory:

- api: high-level qconf API class and related implementation classes
- cli: command line interface classes
- config: configuration manager class
- constants: status codes 
- exceptions: exception classes
- log: log manager and related classes
- objects: qconf object factory and object classes
- utility: various utility classes

Note that python unit tests can be found under the top level 'test'
directory, while the sphinx documentation files are in the 'doc/source' 
directory.

### Adding Support for New UGE Releases

In those cases when new UGE release contains no changes to UGE objects and 
underlying qconf command switches with respect to the previous version of the 
software, UGE PyCL support for the new release can be added by 
editing the 'uge/objects/uge_release_object_map.py' file and cloning the
appropriate 'UGE_RELEASE_OBJECT_MAP' entry. For example, if UGE version X.Y.Zp1
does not have any object changes relative to version X.Y.Z, the following map 
entry would be sufficient:

```
  UGE_RELEASE_OBJECT_MAP['X.Y.Zp1'] = UGE_RELEASE_OBJECT_MAP['X.Y.Z']
```

If, on the other hand, one or more UGE objects changed (e.g., new keywords 
were added, default key values were modified, etc.), the following steps
are necessary:

1. Create new object class file by cloning the most recent existing file. 
Current object file naming convention is to use all lowercase class name 
with words separated by the underscore character, and followed by 
'v<VERSION_STRING>'. In version string dots are always replaced by underscores.
For example, ClusterQueue object version 1.0 is in file 
'cluster_queue_v1_0.py'.
2. Edit new object class file, and make necessary changes. Typically, editing
new object definitions, such as the 'REQUIRED_DATA_DEFAULTS' map should be
sufficient.
3. Edit the 'uge/objects/uge_release_object_map.py' file. 
Add 'UGE_RELEASE_OBJECT_MAP' entry for the new UGE version by copying one 
of the earlier entries, and make necessary corrections. For example, 
suppose that, relative to version X.Y.Z, UGE patch release X.Y.Zp1 
contains a new ClusterQueue class of version A.B. In that case, the 
appropriate entries in the 'UGE_RELEASE_OBJECT_MAP' would be the following:

```
  UGE_RELEASE_OBJECT_MAP['X.Y.Zp1'] = copy.copy(UGE_RELEASE_OBJECT_MAP['X.Y.Z'])
  UGE_RELEASE_OBJECT_MAP['X.Y.Zp1']['ClusterQueue'] = 'A.B'
```

Adding support for new UGE objects is slightly more complex, and would 
involve the steps listed below:

1. Create new object class definition file under the 'uge/objects' directory.
2. Add corresponding 'UGE_RELEASE_OBJECT_MAP' entry in the
'uge/objects/uge_release_object_map.py' file.
3. Implement new factory method in the 'uge/object/qconf_object_factory' file.
4. Implement new manager class in the 'uge/api/impl' directory.
5. Add high-level API methods in the 'uge/api/qconf_api.py' file.
6. Add object unit tests file under the 'test' directory.
7. Modify object and API documentation files in the 'doc/source' directory.

### Enhancing Library Functionality

Modifying existing library functionality, or adding new high-level API methods 
without introducing new objects would typically involve the following steps:

1. Implement changes in the appropriate manager class ('uge/api/impl' 
directory).
2. Add or modify high-level API methods as necessary ('uge/api/qconf_api.py' 
file).
3. Add or modify unit tests as needed ('test' directory).
4. Modify API documentation files as needed ('doc/source' directory).

Adding new command line interfaces built on top of API can be done by 
implementing a CLI class that is derived from QconfCli class, and has
three methods:

1. __init__(): Class constructor, should define CLI options and flags.
2. check_input_args(): Optional method, should verify that required options 
have been passed in, and throw exception if that was not the case.
3. run_command(): Method that performs CLI task, typically by calling 
high-level API method.

QconfCli class, as well as examples of working command line interfaces can be 
found in the 'uge/cli' directory.

