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

# After including params.mk, ARCH and other variables should be set.
ifndef TOP
ROOT            = $(dir $(filter %include.mk,$(MAKEFILE_LIST)))
ROOT            := $(ROOT:%/util/=%)
ROOT            := $(ROOT:util/=.)
export TOP             := $(shell cd $(ROOT) >/dev/null 2>&1 && echo $$PWD)
endif

include $(TOP)/util/params.mk
include $(TOP)/util/platform.mk
