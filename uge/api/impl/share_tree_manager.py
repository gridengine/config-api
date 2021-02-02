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
import types
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.invalid_request import InvalidRequest
from uge.exceptions.invalid_argument import InvalidArgument
from uge.objects.qconf_object_factory import QconfObjectFactory
from .dict_list_based_object_manager import DictListBasedObjectManager

class ShareTreeManager(DictListBasedObjectManager):

    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*no sharetree element.*'),ObjectNotFound),
        (re.compile('.*denied: share tree contains reference to unknown user/project.*'),InvalidRequest),
        (re.compile('.*Unable to locate.*'),ObjectNotFound),
        (re.compile('.share value must be positive.*'),InvalidArgument),
    ]

    QCONF_ERROR_SSTREE_REGEX_LIST = [
        (re.compile('.*no sharetree element.*'),ObjectNotFound),
    ]

    GENERATE_OBJECT_FACTORY_METHOD = QconfObjectFactory.generate_share_tree
    OBJECT_NAME_KEY = None
    OBJECT_CLASS_NAME = 'ShareTree'
    OBJECT_CLASS_UGE_NAME = 'stree'

    def __init__(self, qconf_executor):
        DictListBasedObjectManager.__init__(self, qconf_executor)

    def add_stnode(self, path, shares):
        try:
            share_value = int(shares)
        except ValueError as ex:
            raise InvalidArgument(exception=ex)
        self.qconf_executor.execute_qconf('-astnode %s=%s' % (path, shares), self.QCONF_ERROR_REGEX_LIST)
        return self.get_object()

    def delete_stnode(self, path):
        self.qconf_executor.execute_qconf('-dstnode %s' % (path), self.QCONF_ERROR_REGEX_LIST)
        return self.get_object()

    def object_exists(self):
        try:
            self.qconf_executor.execute_qconf('-sstree', self.QCONF_ERROR_SSTREE_REGEX_LIST)
        except ObjectNotFound as ex:
            return False
        return True

    # The following methods implement behavior where no share tree 
    # is equivalent to empty list
    def get_object_if_exists(self):
        # Return empty list if share is not there
        if self.object_exists():
            stree = self.get_object()
        else:
            stree = self.generate_object(data=[], add_required_data=False)
        return stree

    def delete_object_if_exists(self):
        # Do not throw exception if share tree is not there
        if self.object_exists():
            self.delete_object()

    def modify_or_add_object(self, pycl_object=None, data=None,
                      metadata=None, json_string=None):
        # If empty list is provided, delete share tree
        if type(data) == list and not len(data):
            self.delete_object_if_exists()
            return self.generate_object(data=[], add_required_data=False)
        else:     
            # If share tree exists, modify it
            # If share tree is not there, add it.
            if self.object_exists():
                stree = self.modify_object(pycl_object=pycl_object, data=data, metadata=metadata, json_string=json_string)
            else:
                stree = self.add_object(pycl_object=pycl_object, data=data, metadata=metadata, json_string=json_string)
        return stree

#############################################################################
# Testing.
if __name__ == '__main__':
    pass

