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
from uge.exceptions.object_already_exists import ObjectAlreadyExists
from uge.exceptions.invalid_request import InvalidRequest
from uge.api.impl.list_based_object_manager import ListBasedObjectManager


class SubmitHostManager(ListBasedObjectManager):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*already exists.*'), ObjectAlreadyExists),
        (re.compile('.*does not exist.*'), ObjectNotFound),
        (re.compile('.*may not remove.*'), InvalidRequest),
        (re.compile('.*resolving host.*'), ObjectNotFound),
        (re.compile('.*no submit host defined.*'), ObjectNotFound),
    ]

    OBJECT_NAME = 'submit host'
    OBJECT_CLASS_UGE_NAME = 's'

    def __init__(self, qconf_executor):
        ListBasedObjectManager.__init__(self, qconf_executor)


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
