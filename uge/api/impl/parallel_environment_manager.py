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
from uge.exceptions.object_not_found import ObjectNotFound
from uge.objects.qconf_object_factory import QconfObjectFactory
from .dict_based_object_manager import DictBasedObjectManager


class ParallelEnvironmentManager(DictBasedObjectManager):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*is not a parallel environment.*'), ObjectNotFound),
        (re.compile('.*no parallel environment defined.*'), ObjectNotFound),
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = []

    GENERATE_OBJECT_FACTORY_METHOD = QconfObjectFactory.generate_parallel_environment
    OBJECT_NAME_KEY = 'pe_name'
    OBJECT_CLASS_NAME = 'ParallelEnvironment'
    OBJECT_CLASS_UGE_NAME = 'p'
    OBJECT_CLASS_UGE_LIST_DETAILS_NAME = 'ld'

    def __init__(self, qconf_executor):
        DictBasedObjectManager.__init__(self, qconf_executor)

    def get_bulk_dump_filename(self, object):
        return 'conf_api_dump_' + object.data['pe_name']

#############################################################################
# Testing.
if __name__ == '__main__':
    pass
