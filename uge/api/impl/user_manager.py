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


class UserManager(DictBasedObjectManager):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*is still referenced in.*'), InvalidRequest),
        (re.compile('.*does not exist.*'), ObjectNotFound),
        (re.compile('.*no user list defined.*'), ObjectNotFound),
        (re.compile('.*is not known as user.*'), ObjectNotFound),
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = [
        (re.compile('.*is not known as user.*'), ObjectNotFound),
    ]

    GENERATE_OBJECT_FACTORY_METHOD = QconfObjectFactory.generate_user
    OBJECT_NAME_KEY = 'name'
    OBJECT_CLASS_NAME = 'User'
    OBJECT_CLASS_UGE_NAME = 'user'

    def __init__(self, qconf_executor):
        DictBasedObjectManager.__init__(self, qconf_executor)


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
