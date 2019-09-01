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
import copy
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists
from uge.exceptions.invalid_argument import InvalidArgument
from uge.exceptions.invalid_request import InvalidRequest
from uge.objects.qconf_object_factory import QconfObjectFactory
from uge.objects.qconf_object import QconfObject
from uge.objects.qconf_name_list import QconfNameList


class DictListBasedObjectManager(object):
    QCONF_ERROR_REGEX_LIST = [
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = []

    GENERATE_OBJECT_FACTORY_METHOD = None
    OBJECT_CLASS_NAME = None
    OBJECT_CLASS_UGE_NAME = None

    def __init__(self, qconf_executor):
        self.logger = LogManager.get_instance().get_logger(self.__class__.__name__)
        self.qconf_executor = qconf_executor

    def generate_object(self, data=None, metadata=None,
                        json_string=None, uge_version=None,
                        add_required_data=True):
        if not uge_version:
            uge_version = self.qconf_executor.get_uge_version()
        generated_object = self.GENERATE_OBJECT_FACTORY_METHOD(
            uge_version, data=data, metadata=metadata,
            json_string=json_string, add_required_data=add_required_data)
        return generated_object

    def __prepare_object(self, pycl_object=None, data=None,
                         metadata=None, json_string=None,
                         add_required_data=True):
        uge_version = self.qconf_executor.get_uge_version()
        data2 = copy.copy(data)
        metadata2 = copy.copy(metadata)
        # If pycl_object is provided, combine its metadata 
        # with provided metadata
        if pycl_object is not None:
            generated_object = self.GENERATE_OBJECT_FACTORY_METHOD(uge_version, add_required_data=False)
            if not str(type(pycl_object)) == str(type(generated_object)):
                raise InvalidArgument(
                    'The pycl_object argument must be an instance of %s.' % generated_object.__class__.__name__)
            data2 = copy.copy(pycl_object.data)
            if data:
                data2 = copy.copy(data)
            metadata2 = copy.copy(pycl_object.metadata)
            if metadata:
                metadata2.update(metadata)
        result_object = self.GENERATE_OBJECT_FACTORY_METHOD(
            uge_version, data=data2, metadata=metadata2,
            json_string=json_string, add_required_data=add_required_data)
        result_object.check_user_provided_keys()
        return result_object

    def verify_object_before_add(self, pycl_object):
        return

    def add_object(self, pycl_object=None, data=None,
                   metadata=None, json_string=None):
        new_object = self.__prepare_object(
            pycl_object=pycl_object, data=data,
            metadata=metadata, json_string=json_string)
        try:
            old_object = self.get_object()
            raise ObjectAlreadyExists('%s already exists.' % (self.OBJECT_CLASS_NAME))
        except ObjectNotFound as ex:
            # ok
            pass
        self.verify_object_before_add(new_object)
        self.qconf_executor.execute_qconf_with_object('-A%s' % self.OBJECT_CLASS_UGE_NAME, new_object,
                                                      self.QCONF_ERROR_REGEX_LIST)
        new_object.set_add_metadata()
        return new_object

    def verify_object_before_modify(self, pycl_object):
        return

    def modify_object(self, pycl_object=None, data=None,
                      metadata=None, json_string=None):
        generated_object = self.__prepare_object(
            pycl_object=pycl_object, data=data,
            metadata=metadata, json_string=json_string,
            add_required_data=True)
        updated_object = self.get_object()
        updated_object.data = generated_object.data
        self.verify_object_before_modify(updated_object)
        self.qconf_executor.execute_qconf_with_object('-M%s' % self.OBJECT_CLASS_UGE_NAME, updated_object,
                                                      self.QCONF_ERROR_REGEX_LIST)
        updated_object.set_modify_metadata()
        return updated_object

    def replace_object(self, updated_object):
        self.qconf_executor.execute_qconf_with_object('-M%s' % self.OBJECT_CLASS_UGE_NAME, updated_object,
                                                      self.QCONF_ERROR_REGEX_LIST)
        updated_object.set_modify_metadata()
        return updated_object

    def get_object(self):
        uge_version = self.qconf_executor.get_uge_version()
        retrieved_object = self.GENERATE_OBJECT_FACTORY_METHOD(uge_version, add_required_data=False)
        qconf_output = self.qconf_executor.execute_qconf('-s%s' % (self.OBJECT_CLASS_UGE_NAME),
                                                         self.QCONF_ERROR_REGEX_LIST,
                                                         failure_regex_list=self.QCONF_FAILURE_REGEX_LIST).get_stdout()
        retrieved_object.set_data_dict_list_from_qconf_output(qconf_output)
        return retrieved_object

    def verify_object_before_delete(self, pycl_object):
        return

    def delete_object(self):
        deleted_object = self.get_object()
        self.verify_object_before_delete(deleted_object)
        self.qconf_executor.execute_qconf('-d%s' % (self.OBJECT_CLASS_UGE_NAME), self.QCONF_ERROR_REGEX_LIST)


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
