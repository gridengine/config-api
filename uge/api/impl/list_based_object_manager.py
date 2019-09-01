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
import sys
import types
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.invalid_request import InvalidRequest
from uge.exceptions.object_already_exists import ObjectAlreadyExists
from uge.exceptions.invalid_argument import InvalidArgument
from uge.objects.qconf_object import QconfObject
from uge.objects.qconf_name_list import QconfNameList


class ListBasedObjectManager(object):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*already exists.*'), ObjectAlreadyExists),
        (re.compile('.*does not exist.*'), ObjectNotFound),
        (re.compile('.*may not remove.*'), InvalidRequest),
    ]

    OBJECT_NAME = None
    OBJECT_CLASS_UGE_NAME = None

    def __init__(self, qconf_executor):
        self.logger = LogManager.get_instance().get_logger(self.__class__.__name__)
        self.qconf_executor = qconf_executor

    def __prepare_names(self, names):
        if sys.version_info < (3,):
            text_type = unicode
            binary_type = str
        else:
            text_type = str
            binary_type = bytes
        if type(names) == text_type or type(names) == binary_type:
            if names.find(','):
                name_list = names.split(',')
            else:
                name_list = names.split()
        elif type(names) == list:
            name_list = names
        else:
            raise InvalidArgument(
                'Names must be provided either as a list, or as a string containing names separated by space or comma.')
        name_list2 = []
        for name in name_list:
            trimmed_name = name.strip()
            if len(trimmed_name):
                name_list2.append(trimmed_name)
        return ','.join(name_list2)

    def add_names(self, names):
        names = self.__prepare_names(names)
        self.qconf_executor.execute_qconf('-a%s %s' % (self.OBJECT_CLASS_UGE_NAME, names), self.QCONF_ERROR_REGEX_LIST,
                                          combine_error_lines=False)
        name_list = self.list_names()
        name_list.set_modify_metadata()
        return name_list

    def delete_names(self, names):
        names = self.__prepare_names(names)
        self.qconf_executor.execute_qconf('-d%s %s' % (self.OBJECT_CLASS_UGE_NAME, names), self.QCONF_ERROR_REGEX_LIST,
                                          combine_error_lines=False)
        name_list = self.list_names()
        name_list.set_modify_metadata()
        return name_list

    def list_names(self):
        try:
            qconf_output = self.qconf_executor.execute_qconf('-s%s' % (self.OBJECT_CLASS_UGE_NAME),
                                                             self.QCONF_ERROR_REGEX_LIST).get_stdout()
            name_list = QconfNameList(metadata={'description': 'List of %s names' % (self.OBJECT_NAME)},
                                      data=QconfObject.get_list_from_qconf_output(qconf_output))
        except ObjectNotFound as ex:
            name_list = QconfNameList(metadata={'description': 'List of %s names' % (self.OBJECT_NAME)}, data=[])
        return name_list


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
