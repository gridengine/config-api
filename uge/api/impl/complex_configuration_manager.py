#!/usr/bin/env python
# 
# ___INFO__MARK_BEGIN__
#######################################################################################
# Copyright 2016-2021 Univa Corporation (acquired and owned by Altair Engineering Inc.)
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
from uge.exceptions.invalid_argument import InvalidArgument
from uge.exceptions.object_already_exists import ObjectAlreadyExists
from uge.exceptions.object_not_found import ObjectNotFound
from uge.objects.qconf_object_factory import QconfObjectFactory
from .dict_based_object_manager import DictBasedObjectManager


class ComplexConfigurationManager(DictBasedObjectManager):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*is not a valid.*'), InvalidRequest),
        (re.compile('.*cannot be deleted.*'), InvalidRequest),
        (re.compile('.*error parsing value.*'), InvalidArgument),
        (re.compile('.*should end.*'), InvalidArgument),
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = []

    GENERATE_OBJECT_FACTORY_METHOD = QconfObjectFactory.generate_complex_configuration
    OBJECT_NAME_KEY = None
    OBJECT_CLASS_NAME = 'ComplexConfiguration'
    OBJECT_CLASS_UGE_NAME = 'c'

    def __init__(self, qconf_executor):
        DictBasedObjectManager.__init__(self, qconf_executor)

    def add_object(self, pycl_object=None, data=None,
                   metadata=None, json_string=None):
        raise InvalidRequest('Complex configuration object cannot be added.')

    def delete_object(self):
        raise InvalidRequest('Complex configuration cannot be deleted.')

    def list_objects(self):
        raise InvalidRequest('This method is not supported for complex configuration.')

    def add_cattr(self, name, data):
        cconf = self.get_object('')
        cconf.check_attribute_data(name, data)
        if name in cconf.data:
            raise ObjectAlreadyExists('Complex attribute %s already exists.' % name)
        cconf.data[name] = data
        return self.replace_object(cconf)

    def modify_cattr(self, name, data):
        cconf = self.get_object('')
        if name in cconf.data:
            attr_data = cconf.data[name]
            attr_data.update(data)
        else:
            raise ObjectNotFound('Complex attribute %s does not exist.' % name)
        cconf.check_attribute_data(name, attr_data)
        return self.replace_object(cconf)

    def delete_cattr(self, name):
        cconf = self.get_object('')
        if name in cconf.data:
            del cconf.data[name]
        else:
            raise ObjectNotFound('Complex attribute %s does not exist.' % name)
        return self.replace_object(cconf)


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
