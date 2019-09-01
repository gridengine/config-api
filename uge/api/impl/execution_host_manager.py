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
import os
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.invalid_request import InvalidRequest
from uge.objects.qconf_object_factory import QconfObjectFactory
from .dict_based_object_manager import DictBasedObjectManager


class ExecutionHostManager(DictBasedObjectManager):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*resolving host.*'), ObjectNotFound),
        (re.compile('.*not an execution host.*'), ObjectNotFound),
        (re.compile('.*is still referenced in.*'), InvalidRequest),
        (re.compile('.*no execution host defined.*'), ObjectNotFound),
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = []

    GENERATE_OBJECT_FACTORY_METHOD = QconfObjectFactory.generate_execution_host
    OBJECT_NAME_KEY = 'hostname'
    OBJECT_CLASS_NAME = 'ExecutionHost'
    OBJECT_CLASS_UGE_NAME = 'e'
    OBJECT_CLASS_UGE_LIST_DETAILS_NAME = 'ld'

    BULK_SEPARATOR = '^===========+'

    def __init__(self, qconf_executor):
        DictBasedObjectManager.__init__(self, qconf_executor)

    def get_bulk_dump_filename(self, object):
        return 'conf_api_dump_' + object.data['hostname']

    def write_objects(self, object_list, dirname):
        if 'SGE_ALLOW_CHANGE_LOAD_VALUES' in os.environ:
            self.object_dump_ignored_key_list = []
        else:
            self.object_dump_ignored_key_list = ['load_values', 'processors']
        super(ExecutionHostManager, self).write_objects(object_list, dirname)

    def list_objects(self):
        name_list = DictBasedObjectManager.list_objects(self)
        name_list.append('global')
        return name_list


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
