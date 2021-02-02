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
from uge.exceptions.object_not_found import ObjectNotFound
from uge.objects.qconf_object_factory import QconfObjectFactory
from .dict_based_object_manager import DictBasedObjectManager


class ResourceQuotaSetManager(DictBasedObjectManager):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*is still referenced in.*'), InvalidRequest),
        (re.compile('.*no resource quota set.*defined.*'), ObjectNotFound),
        (re.compile('.*No resource quota set found.*'), ObjectNotFound),
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = []

    GENERATE_OBJECT_FACTORY_METHOD = QconfObjectFactory.generate_resource_quota_set
    OBJECT_NAME_KEY = 'name'
    OBJECT_CLASS_NAME = 'ResourceQuotaSet'
    OBJECT_CLASS_UGE_NAME = 'rqs'

    def __init__(self, qconf_executor):
        DictBasedObjectManager.__init__(self, qconf_executor)


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
