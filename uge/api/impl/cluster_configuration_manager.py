#!/usr/bin/env python
# 
# ___INFO__MARK_BEGIN__
########################################################################## 
# Copyright 2016,2017 Univa Corporation
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License. 
########################################################################### 
# ___INFO__MARK_END__
# 
import re
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.invalid_request import InvalidRequest
from uge.objects.qconf_object_factory import QconfObjectFactory
from .dict_based_object_manager import DictBasedObjectManager


class ClusterConfigurationManager(DictBasedObjectManager):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*resolving host.*'), ObjectNotFound),
        (re.compile('.*no config defined.*'), ObjectNotFound),
        (re.compile('.*configuration.*not defined.*'), InvalidRequest),
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = []

    GENERATE_OBJECT_FACTORY_METHOD = QconfObjectFactory.generate_cluster_configuration
    OBJECT_NAME_KEY = None
    OBJECT_CLASS_NAME = 'ClusterConfiguration'
    OBJECT_CLASS_UGE_NAME = 'conf'

    def __init__(self, qconf_executor):
        DictBasedObjectManager.__init__(self, qconf_executor)

    def verify_object_before_add(self, pycl_object):
        if not pycl_object.name:
            raise InvalidRequest('Cluster configuration name must be specified.')
        if pycl_object.name == 'global':
            raise InvalidRequest('Global cluster configuration cannot be added.')
        return

    def verify_object_before_delete(self, pycl_object):
        if not pycl_object.name:
            raise InvalidRequest('Cluster configuration name must be specified.')
        if pycl_object.name == 'global':
            raise InvalidRequest('Global cluster configuration cannot be deleted.')
        return

    def get_object(self, name):
        if name == 'global':
            # This avoids name resolution for 'global'
            pycl_object = DictBasedObjectManager.get_object(self, '')
            pycl_object.name = name
        else:
            pycl_object = DictBasedObjectManager.get_object(self, name)
        return pycl_object


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
