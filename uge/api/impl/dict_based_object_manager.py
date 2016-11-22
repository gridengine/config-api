#!/usr/bin/env python
# 
#___INFO__MARK_BEGIN__ 
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
#___INFO__MARK_END__ 
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

class DictBasedObjectManager(object):

    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*is still referenced in.*'),InvalidRequest),
        (re.compile('.*does not exist.*'),ObjectNotFound),
        (re.compile('.*no .* list defined.*'),ObjectNotFound),
        (re.compile('.*is not known as.*'),ObjectNotFound),
    ]

    # Failure incorrectly classified as successful outcome
    QCONF_FAILURE_REGEX_LIST = []

    GENERATE_OBJECT_FACTORY_METHOD = None
    OBJECT_NAME_KEY = None
    OBJECT_CLASS_NAME = None
    OBJECT_CLASS_UGE_NAME = None

    def __init__(self, qconf_executor):
        self.logger = LogManager.get_instance().get_logger(self.__class__.__name__)
        self.qconf_executor = qconf_executor

    def generate_object(self, name=None, data=None, metadata=None, 
                        json_string=None, uge_version=None, 
                        add_required_data=True):
        if not uge_version:
            uge_version = self.qconf_executor.get_uge_version()
        generated_object = self.GENERATE_OBJECT_FACTORY_METHOD(
            uge_version, name=name, data=data, metadata=metadata, 
            json_string=json_string, add_required_data=add_required_data)
        return generated_object

    def __prepare_object(self, pycl_object=None, name=None, data=None,
                         metadata=None, json_string=None, 
                         add_required_data=True):
        uge_version = self.qconf_executor.get_uge_version()
        data2 = copy.copy(data)
        metadata2 = copy.copy(metadata)
        name2 = name
        # If pycl_object is provided, combine its data/metadata 
        # with provided data/metadata
        if pycl_object is not None:
            generated_object = self.GENERATE_OBJECT_FACTORY_METHOD(uge_version, add_required_data=False)
            if not str(type(pycl_object)) == str(type(generated_object)):
                raise InvalidArgument('The pycl_object argument must be an instance of %s.' % generated_object.__class__.__name__)
            data2 = copy.copy(pycl_object.data)
            if data: 
                data2.update(data)
            metadata2 = copy.copy(pycl_object.metadata)
            if metadata: 
                metadata2.update(metadata)
            if not name2:
                name2 = pycl_object.name
        result_object = self.GENERATE_OBJECT_FACTORY_METHOD(
            uge_version, name=name2, data=data2, metadata=metadata2, 
            json_string=json_string, add_required_data=add_required_data)
        result_object.check_user_provided_keys()
        return result_object

    def verify_object_before_add(self, pycl_object):
        return

    def add_object(self, pycl_object=None, name=None, data=None,
                   metadata=None, json_string=None):
        new_object = self.__prepare_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)
        if self.OBJECT_NAME_KEY:
            object_name = new_object.data.get(self.OBJECT_NAME_KEY)
        elif new_object.name:
            object_name = new_object.name
        else:
            object_name = ''
        try:
            old_object = self.get_object(object_name)
            raise ObjectAlreadyExists('%s %s already exists.' % (self.OBJECT_CLASS_NAME, object_name))
        except ObjectNotFound, ex:
            # ok
            pass
        new_object.remove_optional_keys()
        self.verify_object_before_add(new_object)
        self.qconf_executor.execute_qconf_with_object('-A%s' % self.OBJECT_CLASS_UGE_NAME, new_object, self.QCONF_ERROR_REGEX_LIST)
        new_object.set_add_metadata()
        return new_object

    def verify_object_before_modify(self, pycl_object):
        return

    def modify_object(self, pycl_object=None, name=None, data=None,
                     metadata=None, json_string=None):
        generated_object = self.__prepare_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string, 
            add_required_data=False)
        if self.OBJECT_NAME_KEY:
            object_name = generated_object.data.get(self.OBJECT_NAME_KEY)
        elif generated_object.name:
            object_name = generated_object.name
        else:
            object_name = ''
        updated_object = self.get_object(object_name)
        updated_object.data.update(generated_object.data)
        updated_object.remove_optional_keys()
        self.verify_object_before_modify(updated_object)
        self.qconf_executor.execute_qconf_with_object('-M%s' % self.OBJECT_CLASS_UGE_NAME, updated_object, self.QCONF_ERROR_REGEX_LIST)
        updated_object.set_modify_metadata()
        return updated_object

    def replace_object(self, updated_object):
        self.qconf_executor.execute_qconf_with_object('-M%s' % self.OBJECT_CLASS_UGE_NAME, updated_object, self.QCONF_ERROR_REGEX_LIST)
        updated_object.set_modify_metadata()
        return updated_object

    def get_object(self, name):
        uge_version = self.qconf_executor.get_uge_version()
        retrieved_object = self.GENERATE_OBJECT_FACTORY_METHOD(uge_version, add_required_data=False)
        qconf_output = self.qconf_executor.execute_qconf('-s%s %s' % (self.OBJECT_CLASS_UGE_NAME, name), self.QCONF_ERROR_REGEX_LIST, failure_regex_list=self.QCONF_FAILURE_REGEX_LIST).get_stdout()
        retrieved_object.set_data_dict_from_qconf_output(qconf_output)
        retrieved_object.name = name
        return retrieved_object

    def verify_object_before_delete(self, pycl_object):
        return

    def delete_object(self, name):
        deleted_object = self.get_object(name)
        self.verify_object_before_delete(deleted_object)
        self.qconf_executor.execute_qconf('-d%s %s' % (self.OBJECT_CLASS_UGE_NAME, name), self.QCONF_ERROR_REGEX_LIST)

    def list_objects(self):
        try:
            qconf_output = self.qconf_executor.execute_qconf('-s%sl' % (self.OBJECT_CLASS_UGE_NAME), self.QCONF_ERROR_REGEX_LIST).get_stdout()
            object_list = QconfNameList(metadata={'description' : 'List of %s object names' % (self.OBJECT_CLASS_NAME)}, data=QconfObject.get_list_from_qconf_output(qconf_output))
        except ObjectNotFound, ex:
            object_list = QconfNameList(metadata={'description' : 'List of %s object names' % (self.OBJECT_CLASS_NAME)}, data=[])
        return object_list
        
#############################################################################
# Testing.
if __name__ == '__main__':
    pass

