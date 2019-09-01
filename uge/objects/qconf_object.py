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
import copy
import datetime
import json
import os
import tempfile

from uge.config.config_manager import ConfigManager
from uge.exceptions.invalid_argument import InvalidArgument
from uge.exceptions.invalid_request import InvalidRequest


class QconfObject(object):
    """ This class encapsulates data and functionality common to all Qconf API objects. """

    VERSION = '1.0'
    NAME_KEY = None
    UGE_PYTHON_OBJECT_MAP = {
        'NONE': None,
        'INFINITY': float('inf'),
        'TRUE': True,
        'FALSE': False,
    }
    UGE_CASE_SENSITIVE_KEYS = {}
    USER_PROVIDED_KEYS = []
    REQUIRED_DATA_DEFAULTS = {}
    BOOL_KEY_MAP = {}
    INT_KEY_MAP = {}
    FLOAT_KEY_MAP = {}
    LIST_KEY_MAP = {}
    DEFAULT_LIST_DELIMITER = ','
    DICT_KEY_MAP = {}
    DEFAULT_DICT_DELIMITER = ','
    DICT_VALUE_DELIMITER = '='
    OPTIONAL_KEYS_ALLOWED = False

    def __init__(self, name=None, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param name: Object name. If provided, it will override object's name from data or JSON string parameters.
        :type name: str

        :param data: Object data. If provided, it will override corresponding data from object's JSON string representation.
        :type data: varies

        :param metadata: Object metadata. If provided, it will override corresponding metadata from object's JSON string representation.
        :type metadata: dict

        :param json_string: Object's JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing a Qconf object.
        """
        self.name = name
        self.metadata = {}
        if not hasattr(self, 'data'):
            self.data = {}

        # Unpack and check json
        json_dict = self.unpack_input_json(json_string)
        if json_dict:
            if 'data' in json_dict:
                self.data = json_dict.get('data')
                del json_dict['data']
            self.metadata = json_dict

        # Merge json entries with provided metadata
        if metadata:
            self.check_input_metadata(metadata)
            self.metadata.update(metadata)

        # Merge json entries with provided data
        if data:
            self.check_input_data(data)
            if type(data) == dict:
                self.data.update(data)
            else:
                self.data = data

        if name and self.NAME_KEY:
            self.data[self.NAME_KEY] = name

        # Convert list and dict keys
        self.convert_list_keys()
        self.convert_dict_keys()

        # Add standard metadata
        self.metadata['object_version'] = self.VERSION
        self.metadata['object_class'] = self.__class__.__name__

    def unpack_input_json(self, json_string):
        if not json_string:
            return None
        try:
            json_dict = json.loads(json_string)
        except Exception as ex:
            raise InvalidArgument('Input is not a valid json string: %s (error: %s).' % (str(json_string), ex))
        if type(json_dict) != dict:
            raise InvalidArgument('Input json string does not contain dictionary: %s.' % str(json_string))
        return json_dict

    def check_user_provided_keys(self):
        """ 
        Checks for presence of all data keys that must be provided by user.

        :raises: **InvalidRequest** - in case object's data is not a dictionary, or if any of the required keys are missing.
        """
        if type(self.data) != dict:
            raise InvalidRequest('Data object is not a dictionary: %s.' % str(self.data))

        for key in self.USER_PROVIDED_KEYS:
            if not self.data.get(key):
                raise InvalidRequest('Input data is missing required object key: %s.' % str(key))

    def check_input_data(self, data):
        pass

    def check_input_metadata(self, metadata):
        if metadata:
            if type(metadata) != dict:
                raise InvalidArgument('Provided metadata is not a dictionary: %s.' % str(metadata))

    def remove_optional_keys(self):
        """ 
        Removes values for keys that are not required from object's data. 

        :raises: **InvalidRequest** - in case object's data is not a dictionary.
        """
        if self.OPTIONAL_KEYS_ALLOWED:
            return

        if type(self.data) != dict:
            raise InvalidRequest('Data object is not a dictionary: %s.' % str(self.data))

        removed_keys = []
        for (key, value) in list(self.data.items()):
            if key not in self.get_required_data_defaults():
                if key not in self.USER_PROVIDED_KEYS and not key.startswith('#'):
                    removed_keys.append(key)
        for key in removed_keys:
            del self.data[key]

    def update_with_required_data_defaults(self):
        """ 
        Updates object with default values for required data keys.

        :raises: **InvalidArgument** - in case object's data is not a dictionary.
        """
        if type(self.data) != dict:
            raise InvalidRequest('Data object is not a dictionary: %s.' % str(self.data))
        for (key, value) in list(self.get_required_data_defaults().items()):
            if key not in self.data:
                if type(value) == bytes:
                    for env_var in ['SGE_ROOT', 'SGE_CELL']:
                        value = value.replace(env_var, os.environ[env_var])
                self.data[key] = value

    def get_tmp_file(self):
        fd, tmp_file_path = tempfile.mkstemp(text=True)
        tmp_file = os.fdopen(fd, 'w')
        tmp_dir_path = None
        return (tmp_file, tmp_file_path, tmp_dir_path)

    def get_required_data_defaults(self):
        return self.REQUIRED_DATA_DEFAULTS

    def convert_list_keys(self):
        for key in list(self.LIST_KEY_MAP.keys()):
            value = self.data.get(key)
            if value is not None:
                if type(value) == bytes or type(value) == str:
                    delimiter = self.LIST_KEY_MAP.get(key, self.DEFAULT_LIST_DELIMITER)
                    self.data[key] = value.split(delimiter)
                elif type(value) != list:
                    raise InvalidArgument(
                        'Value for key %s must be provided either as a string, or as a python list of strings.' % key)

    def parse_value_as_dict(self, key, value):
        delimiter = self.DICT_KEY_MAP.get(key, self.DEFAULT_LIST_DELIMITER)
        items = value.split(delimiter)
        value_dict = {}
        for item in items:
            if item.find(self.DICT_VALUE_DELIMITER) < 0:
                raise InvalidArgument(
                    'Cannot parse dictionary value: Unexpected format of item %s for key %s.' % (item, key))
            item_tokens = item.split(self.DICT_VALUE_DELIMITER)
            item_key = item_tokens[0]
            item_value = self.DICT_VALUE_DELIMITER.join(item_tokens[1:])
            value_dict[item_key] = self.uge_to_py(item_key, item_value)
        return value_dict

    def convert_dict_keys(self):
        for key in list(self.DICT_KEY_MAP.keys()):
            value = self.data.get(key)
            if value is not None:
                if type(value) == bytes:
                    self.data[key] = self.parse_value_as_dict(key, value)
                elif type(value) != dict:
                    raise InvalidArgument(
                        'Value for key %s must be provided either as a string, or as a python dictionary.' % key)

    def set_data_dict_from_qconf_output(self, qconf_output):
        data = self.to_dict(qconf_output)
        self.data = data

    @classmethod
    def get_list_from_qconf_output(cls, qconf_output):
        qconf_output = qconf_output.strip()
        qconf_list = []
        if len(qconf_output):
            qconf_list = qconf_output.split('\n')
        return qconf_list

    @classmethod
    def get_bool_key_map(cls, key_map):
        bool_key_map = {}
        for (key, value) in list(key_map.items()):
            if type(value) == bool:
                bool_key_map[key] = value
            elif type(value) == dict:
                for (key2, value2) in list(value.items()):
                    if type(value2) == bool:
                        bool_key_map[key2] = value2
        return bool_key_map

    @classmethod
    def get_int_key_map(cls, key_map):
        int_key_map = {}
        for (key, value) in list(key_map.items()):
            if type(value) == int:
                int_key_map[key] = value
            elif type(value) == dict:
                for (key2, value2) in list(value.items()):
                    if type(value2) == int:
                        int_key_map[key2] = value2
        return int_key_map

    @classmethod
    def get_float_key_map(cls, key_map):
        float_key_map = {}
        for (key, value) in list(key_map.items()):
            if type(value) == float:
                float_key_map[key] = value
        return float_key_map

    @classmethod
    def get_list_key_map(cls, key_map):
        list_key_map = {}
        for (key, value) in list(key_map.items()):
            if type(value) == list:
                list_key_map[key] = value
        return list_key_map

    def uge_to_py(self, key, value):
        uppercase_value = value.upper()
        for (uge_value, py_value) in list(self.UGE_PYTHON_OBJECT_MAP.items()):
            if uge_value == uppercase_value:
                return py_value
        if key in self.LIST_KEY_MAP:
            # Key is designated as list key.
            # Try to split by corresponding delimiter.
            delimiter = self.LIST_KEY_MAP.get(key)
            if value.find(delimiter) > 0:
                return value.split(delimiter)
            else:
                return [value]
        elif key in self.DICT_KEY_MAP:
            # Key is designated as dict key.
            # Try to split by corresponding delimiter.
            return self.parse_value_as_dict(key, value)
        elif key in self.INT_KEY_MAP:
            try:
                return int(value)
            except:
                # We cannot convert this string to int
                pass
        elif key in self.FLOAT_KEY_MAP:
            try:
                return float(value)
            except:
                # We cannot convert this string to float
                pass
        elif value.find(self.DEFAULT_LIST_DELIMITER) > 0:
            return value.split(self.DEFAULT_LIST_DELIMITER)
        return value

    def py_to_uge(self, key, value):
        for (uge_value, py_value) in list(self.UGE_PYTHON_OBJECT_MAP.items()):
            if value == py_value and type(value) == type(py_value):
                if key in self.UGE_CASE_SENSITIVE_KEYS:
                    return self.UGE_CASE_SENSITIVE_KEYS[key](uge_value)
                return uge_value
        if type(value) == list:
            delimiter = self.LIST_KEY_MAP.get(key, self.DEFAULT_LIST_DELIMITER)
            return delimiter.join(value)
        elif type(value) == dict:
            delimiter = self.DICT_KEY_MAP.get(key, self.DEFAULT_DICT_DELIMITER)
            dict_tokens = []
            for (item_key, item_value) in list(value.items()):
                dict_tokens.append('%s%s%s' % (item_key, self.DICT_VALUE_DELIMITER, item_value))
            return delimiter.join(dict_tokens)
        return value

    def to_uge(self):
        """ 
        Converts object to string acceptable as input for UGE qconf command.

        :returns: Object's UGE-formatted string.
        """
        lines = ''
        for (key, value) in list(self.data.items()):
            lines += '%s %s\n' % (key, self.py_to_uge(key, value))
        return lines

    def convert_data_to_uge_keywords(self, data):
        for (key, value) in list(data.items()):
            data[key] = self.py_to_uge(key, value)

    def to_json(self, use_uge_keywords=False):
        """ 
        Converts object to JSON string.

        :param use_uge_keywords: if True, UGE keywords (e.g. 'NONE') are restored before conversion to JSON; otherwise, no changes are made to object's data. Default is False.
        :type mode: bool

        :returns: Object's JSON representation.
        """
        json_dict = copy.copy(self.metadata)
        data = copy.copy(self.data)
        if use_uge_keywords:
            self.convert_data_to_uge_keywords(data)
        json_dict['data'] = data
        return json.dumps(json_dict)

    def to_dict(self, input_string):
        lines = input_string.split('\n')
        object_data = {}
        for line in lines:
            if not line:
                continue
            key_value = line.split(' ')
            key = key_value[0]
            value = line.replace(key, '', 1).strip()
            object_data[key] = self.uge_to_py(key, value)
        return object_data

    def set_get_metadata(self):
        """ 
        Sets default object metadata (user/timestamp) for API get operations.
        """
        cm = ConfigManager.get_instance()
        retrieved_by = '%s@%s' % (cm['user'], cm['host'])
        self.metadata['retrieved_by'] = retrieved_by
        self.metadata['retrieved_on'] = datetime.datetime.now().isoformat()

    def set_modify_metadata(self):
        """ 
        Sets default object metadata (user/timestamp) for API modify operations.
        """
        cm = ConfigManager.get_instance()
        modified_by = '%s@%s' % (cm['user'], cm['host'])
        self.metadata['modified_by'] = modified_by
        self.metadata['modified_on'] = datetime.datetime.now().isoformat()

    def set_add_metadata(self):
        """ 
        Sets default object metadata (user/timestamp) for API add operations.
        """
        cm = ConfigManager.get_instance()
        created_by = '%s@%s' % (cm['user'], cm['host'])
        self.metadata['created_by'] = created_by
        self.metadata['created_on'] = datetime.datetime.now().isoformat()
