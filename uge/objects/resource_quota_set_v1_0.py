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
from .qconf_object import QconfObject


class ResourceQuotaSet(QconfObject):
    """ This class encapsulates UGE resource quota set object. """

    #: Object version. 
    VERSION = '1.0'

    #: Object name key.
    NAME_KEY = 'name'

    #: Object keys that must be provided by set.
    USER_PROVIDED_KEYS = ['name']

    #: Default values for required data keys.
    REQUIRED_DATA_DEFAULTS = {
        'description': None,
        'enabled': False,
        'limit': ['to slots=0'],
    }

    BOOL_KEY_MAP = QconfObject.get_bool_key_map(REQUIRED_DATA_DEFAULTS)
    DEFAULT_LIST_DELIMITER = ','
    LIST_KEY_MAP = {
        'limit': ',',
    }

    def __init__(self, name=None, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param name: Resource quota set name. If provided, it will override set name from data or JSON string parameters ('name' key).
        :type name: str

        :param data: Resource quota set data. If provided, it will override corresponding data from set JSON string representation.
        :type data: dict

        :param metadata: Resource quota set metadata. If provided, it will override corresponding metadata from set JSON string representation.
        :type metadata: dict

        :param json_string: Resource quota set JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing an ResourceQuotaList object.
        """
        QconfObject.__init__(self, name=name, data=data, metadata=metadata, json_string=json_string)

    def to_uge(self):
        """ 
        Converts object to string acceptable as input for UGE qconf command.

        :returns: Object's UGE-formatted string.
        """
        lines = '{\n'
        for key in ['name', 'description', 'enabled']:
            value = self.data.get(key)
            lines += '%s %s\n' % (key, self.py_to_uge(key, value))
        limits = self.data.get('limit')
        for limit in limits:
            lines += 'limit %s\n' % limit
        lines += '}\n'
        return lines

    def py_to_uge(self, key, value):
        for (uge_value, py_value) in list(self.UGE_PYTHON_OBJECT_MAP.items()):
            if value == py_value and type(value) == type(py_value):
                return uge_value
        return value

    def to_dict(self, input_string):
        lines = input_string.split('\n')
        object_data = {}
        for line in lines:
            if not line:
                continue
            if line.startswith('{'):
                continue
            if line.startswith('}'):
                continue
            key_value = line.split()
            key = key_value[0]
            value = line.replace(key, '').strip()
            if key == 'limit':
                limits = object_data.get(key, [])
                limits.append(value)
                object_data[key] = limits
            else:
                object_data[key] = self.uge_to_py(key, value)
        return object_data

    def uge_to_py(self, key, value):
        uppercase_value = value.upper()
        for (uge_value, py_value) in list(self.UGE_PYTHON_OBJECT_MAP.items()):
            if uge_value == uppercase_value:
                return py_value
        return value
