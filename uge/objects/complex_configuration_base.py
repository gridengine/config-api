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
import types
from qconf_object import QconfObject
from uge.exceptions.invalid_argument import InvalidArgument

class ComplexConfigurationBase(QconfObject):
    """ This class serves as a base for UGE complex configuration objects. """

    DEFAULT_DICT_DELIMITER = ' '
    DICT_KEY_MAP = {
    }

    UGE_PYTHON_OBJECT_MAP = {
        'NONE'     : None,
        'YES'      : True,
        'NO'       : False,
    }

    UGE_PYTHON_TYPE_MAP = {
        'BOOL'     : int,
        'INT'      : int,
        'FLOAT'    : float,
        'DOUBLE'   : float,
    }

    OPTIONAL_KEYS_ALLOWED = True

    def __init__(self, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param data: Configuration data. If provided, it will override corresponding data from JSON string representation.
        :type data: dict

        :param metadata: Configuration metadata. If provided, it will override corresponding metadata from JSON string representation.
        :type metadata: dict

        :param json_string: Configuration JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing a ClusterConfiguration object.
        """

        QconfObject.__init__(self, data=data, metadata=metadata, json_string=json_string)

    def to_uge(self):
        """ 
        Converts object to string acceptable as input for UGE qconf command.

        :returns: Object's UGE-formatted string.
        """
        lines = ''
        lines += '#name               shortcut   type        relop requestable consumable default  urgency aapre\n'  
        lines += '#-----------------------------------------------------------------------------------------------\n'
        for (key, value_dict) in self.data.items():
            lines += '%s' % (key)
            for key2 in ['shortcut', 'type', 'relop', 'requestable', 'consumable', 'default', 'urgency', 'aapre']:
                lines += ' %s' % (self.py_to_uge(key2, value_dict[key2]))
            lines += '\n' 
        return lines

    def convert_data_to_uge_keywords(self, data):
        for (data_key, value_dict) in data.items():
            for (key, value) in value_dict.items():
                value_dict[key] = self.py_to_uge(key, value)

    def py_to_uge(self, key, value):
        for (uge_value, py_value) in self.UGE_PYTHON_OBJECT_MAP.items():
            if value == py_value and type(value) == type(py_value):
                return uge_value
        return value

    def uge_to_py(self, key, value, uge_type=None):
        uppercase_value = value.upper()
        for (uge_value, py_value) in self.UGE_PYTHON_OBJECT_MAP.items():
            if uge_value == uppercase_value:
                return py_value
        if uge_type and self.UGE_PYTHON_TYPE_MAP.has_key(uge_type):
            py_value = self.UGE_PYTHON_TYPE_MAP[uge_type](value)
            return py_value
        return value

    def to_dict(self, input_string):
        lines = input_string.split('\n')
        object_data = {}
        for line in lines:
            if not line:
                continue
            if line.startswith('#'):
                continue
            key_value = line.split()
            key = key_value[0]
            shortcut = key_value[1]
            uge_type = key_value[2]
            relop = key_value[3]
            requestable = self.uge_to_py(key, key_value[4])
            consumable = self.uge_to_py(key, key_value[5])
            default = self.uge_to_py(key, key_value[6], uge_type)
            urgency = self.uge_to_py(key, key_value[7], 'INT')
            aapre = self.uge_to_py(key, key_value[8])
            object_data[key] = { 
                'shortcut' : shortcut, 
                'type' : uge_type, 
                'relop' : relop, 
                'requestable' : requestable, 
                'consumable' : consumable, 
                'default' : default, 
                'urgency' : urgency, 
                'aapre' : aapre
            }
        return object_data

    def check_attribute_data(self, name, data):
        if not name:
            raise InvalidArgument('Invalid complex attribute name.')
        if type(data) != types.DictType:
            raise InvalidArgument('Complex attribute data must be a dictionary.')
        for key in ['shortcut', 'type', 'relop', 'requestable', 'consumable', 'default', 'urgency', 'aapre'] :
            if not data.has_key(key):
                raise InvalidArgument('Complex attribute data is missing the "%s" key.' % key)

