#######################################################################
##                                                                   ##
##   Copyright (c) 2016, 2017 Univa.  All rights reserved.           ##
##   http://www.univa.com                                            ##
##                                                                   ##
##   License:                                                        ##
##     Apache 2.0                                                    ##
##                                                                   ##
##                                                                   ##
#######################################################################

ifndef TOP
ROOT            = $(dir $(filter %params.mk,$(MAKEFILE_LIST)))
ROOT            := $(ROOT:%/util/=%)
ROOT            := $(ROOT:util/=.)
export TOP             := $(shell cd $(ROOT) >/dev/null 2>&1 && echo $$PWD)
endif

export PYCL_REL_STR       = Development
#export GIT_REV          := git$(shell git rev-parse --verify head)

# Setting the system environment variable PYCL_REL when running make
# will override the contents of the release string.
#
# ie:
#
# $ PYCL_REL="UGE PyCL v1.0" make
#
# By default the file will contain the value of the UC_REL_STR makefile 
# variable bellow.
ifneq ($(strip $(GIT_REV)),)
export PYCL_REL_STR       = Development version ($(GIT_REV))
endif
export VERSION            = 8.6.14a0
export PYCL_PACKAGE_NAME  = uge-pycl

