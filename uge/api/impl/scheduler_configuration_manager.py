#!/usr/bin/env python
#
# ___INFO__MARK_BEGIN__
#######################################################################################
# Copyright 2016-2024 Altair Engineering Inc.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#######################################################################################
# ___INFO__MARK_END__
#
import re
from uge.exceptions.invalid_request import InvalidRequest
from uge.objects.qconf_object_factory import QconfObjectFactory
from .dict_based_object_manager import DictBasedObjectManager


class SchedulerConfigurationManager(DictBasedObjectManager):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*is not a valid.*'), InvalidRequest),
        (re.compile('.*required attribute.*is missing.*'), InvalidRequest),
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = []

    GENERATE_OBJECT_FACTORY_METHOD = QconfObjectFactory.generate_scheduler_configuration
    OBJECT_NAME_KEY = None
    OBJECT_CLASS_NAME = 'SchedulerConfiguration'
    OBJECT_CLASS_UGE_NAME = 'sconf'

    def __init__(self, qconf_executor):
        DictBasedObjectManager.__init__(self, qconf_executor)

    def add_object(self, pycl_object=None, data=None,
                   metadata=None, json_string=None):
        raise InvalidRequest('Scheduler configuration object cannot be added.')

    def delete_object(self):
        raise InvalidRequest('Scheduler configuration cannot be deleted.')

    def list_objects(self):
        raise InvalidRequest('This method is not supported for scheduler configuration.')


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
