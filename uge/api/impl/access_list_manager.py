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
import types
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists
from uge.exceptions.invalid_request import InvalidRequest
from uge.exceptions.invalid_argument import InvalidArgument
from uge.objects.qconf_object_factory import QconfObjectFactory
from .dict_based_object_manager import DictBasedObjectManager


class AccessListManager(DictBasedObjectManager):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*is still referenced in.*'), InvalidRequest),
        (re.compile('.*not allowed to set.*'), InvalidRequest),
        (re.compile('.*unknown specifier.*'), InvalidRequest),
        (re.compile('.*does not exist.*'), ObjectNotFound),
        (re.compile('.*doesn\'t exist.*'), ObjectNotFound),
        (re.compile('.* no list_name.*'), ObjectNotFound),
        (re.compile('.*is already in access list.*'), ObjectAlreadyExists),
        (re.compile('.*is not in access list.*'), ObjectNotFound),
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = []

    GENERATE_OBJECT_FACTORY_METHOD = QconfObjectFactory.generate_access_list
    OBJECT_NAME_KEY = 'name'
    OBJECT_CLASS_NAME = 'AccessList'
    OBJECT_CLASS_UGE_NAME = 'u'

    def __init__(self, qconf_executor):
        DictBasedObjectManager.__init__(self, qconf_executor)

    def delete_object(self, name):
        deleted_object = self.get_object(name)
        self.qconf_executor.execute_qconf('-dul %s' % (name), self.QCONF_ERROR_REGEX_LIST)

    def __check_and_prepare_input(self, input_value, input_arg_name):
        if type(input_value) == bytes or type(input_value) == str:
            if input_value.find(' ') >= 0:
                raise InvalidArgument(
                    'Value for argument %s must be provided either as a comma-separated string list, or as a python '
                    'list of strings.' % input_arg_name)
            return input_value
        elif type(input_value) == list:
            input_value = ','.join(input_value)
            return input_value
        else:
            raise InvalidArgument(
                'Input value must be provided either as a comma-separated string list, or as a python list of strings '
                '(%s input: %s).' % (input_arg_name, input_value))

    def add_users_to_acls(self, user_names, access_list_names):
        user_name_list = self.__check_and_prepare_input(user_names, 'user_names')
        acl_name_list = self.__check_and_prepare_input(access_list_names, 'access_list_names')
        self.qconf_executor.execute_qconf('-au %s %s' % (user_name_list, acl_name_list), self.QCONF_ERROR_REGEX_LIST)
        acl_list = []
        for acl_name in acl_name_list.split(','):
            acl = self.get_object(acl_name)
            acl_list.append(acl)
        return acl_list

    def delete_users_from_acls(self, user_names, access_list_names):
        user_name_list = self.__check_and_prepare_input(user_names, 'user_names')
        acl_name_list = self.__check_and_prepare_input(access_list_names, 'access_list_names')
        self.qconf_executor.execute_qconf('-du %s %s' % (user_name_list, acl_name_list), self.QCONF_ERROR_REGEX_LIST)
        acl_list = []
        for acl_name in acl_name_list.split(','):
            acl = self.get_object(acl_name)
            acl_list.append(acl)
        return acl_list


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
