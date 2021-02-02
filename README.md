(c) Copyright 2016-2021 Univa Corporation (acquired and owned by Altair Engineering Inc.)
    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License.

    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

    See the License for the specific language governing permissions and
    limitations under the License.


# UGE Python Configuration Library

## Prerequisites

UGE PyCL requires recent versions of the following software:

1. UGE (8.3.1p9, 8.4.0, or later)
2. Python (v2.7.5 or later in v2.7 series)
3. Setuptools (0.9.8 or later; for egg installation)
4. Nose (1.3.7 or later; for testing)
5. Sphinx (1.1.3 or later; for generating documentation)
6. Standard development tools (make)

The software versions listed above were used for prototype development and
testing, on CentOS 7.2 (64-bit). It is likely that any recent version of 
Python (such as those that come with current linux distributions) should work.
UGE versions 8.3.1p9 or later or 8.4.0 and later will work with the Configuration API.
Minor modifications to the code that checks versions will have to be made to support
versions greater than 8.4.0.  

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

  adjust test_values.json according to your needs, esp. the host_names have to be resolvable,
  otherwise some execution host tests might fail

```sh
$ make test 
```

