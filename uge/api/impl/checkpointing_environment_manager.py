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
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.invalid_request import InvalidRequest
from uge.objects.qconf_object_factory import QconfObjectFactory
from .dict_based_object_manager import DictBasedObjectManager


class CheckpointingEnvironmentManager(DictBasedObjectManager):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*is not a checkpointing.*'), ObjectNotFound),
        (re.compile('.*no ckpt interface definition.*'), ObjectNotFound),
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = []

    GENERATE_OBJECT_FACTORY_METHOD = QconfObjectFactory.generate_checkpointing_environment
    OBJECT_NAME_KEY = 'ckpt_name'
    OBJECT_CLASS_NAME = 'CheckpointingEnvironment'
    OBJECT_CLASS_UGE_NAME = 'ckpt'
    OBJECT_CLASS_UGE_LIST_DETAILS_NAME = 'ld'

    def __init__(self, qconf_executor):
        DictBasedObjectManager.__init__(self, qconf_executor)

    def get_bulk_dump_filename(self, object):
        return 'conf_api_dump_' + object.data['ckpt_name']

#############################################################################
# Testing.
if __name__ == '__main__':
    pass
