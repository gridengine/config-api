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

from uge.exceptions import InvalidRequest

try:
    import UserList
except ImportError:
    import collections as UserList
from .qconf_object import QconfObject
from uge.exceptions.invalid_argument import InvalidArgument


class QconfDictList(QconfObject, UserList.UserList):
    """ This class encapsulates data and functionality common to all Qconf objects based on a list of dictionaries. """

    FIRST_KEY = None
    NAME_KEY = None
    USER_PROVIDED_KEYS = []
    REQUIRED_DATA_DEFAULTS = {}
    KEY_VALUE_DELIMITER = '='

    def __init__(self, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param data: Configuration data. If provided, it will override corresponding data from JSON string representation.
        :type data: dict

        :param metadata: Configuration metadata. If provided, it will override corresponding metadata from JSON string representation.
        :type metadata: dict

        :param json_string: Configuration JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not represent a list of dictionaries object.
        """
        UserList.UserList.__init__(self)
        QconfObject.__init__(self, data=data, metadata=metadata, json_string=json_string)

    def check_input_data(self, data):
        if type(data) != list:
            raise InvalidArgument('Provided data is not a list: %s.' % str(data))
        for d in data:
            if type(d) != dict:
                raise InvalidArgument('List member is not a dictionary: %s.' % str(d))

    def update_with_required_data_defaults(self):
        """ 
        Updates list objects with default values for required data keys.

        :raises: **InvalidArgument** - in case object's data is not a list, or one of the list members is not a dictionary.
        """
        if type(self.data) != list:
            raise InvalidRequest('Data object is not a list: %s.' % str(self.data))
        for d in self.data:
            if type(d) != dict:
                raise InvalidArgument('List member is not a dictionary: %s.' % str(d))
            for (key, value) in list(self.get_required_data_defaults().items()):
                if key not in d:
                    d[key] = value

    def check_user_provided_keys(self):
        """ 
        Checks for presence of all data keys that must be provided by user.

        :raises: **InvalidRequest** - in case object's data is not a dictionary, or if any of the required keys are missing.
        """
        for d in self.data:
            if type(d) != dict:
                raise InvalidRequest('List member is not a dictionary: %s.' % str(d))
            for key in self.USER_PROVIDED_KEYS:
                if not d.get(key):
                    raise InvalidRequest('Input data %s is missing required object key: %s.' % (str(d), str(key)))

    def to_uge(self):
        """ 
        Converts object to string acceptable as input for UGE qconf command.

        :returns: Object's UGE-formatted string.
        """
        lines = ''
        for d in self.data:
            for (key, value) in list(d.items()):
                lines += '%s%s%s\n' % (key, self.KEY_VALUE_DELIMITER, self.py_to_uge(key, value))
        return lines

    def convert_data_to_uge_keywords(self, data):
        for d in data:
            for (key, value) in list(d.items()):
                d[key] = self.py_to_uge(key, value)

    def set_data_dict_list_from_qconf_output(self, qconf_output):
        data = self.to_dict_list(qconf_output)
        self.data = data

    def to_dict_list(self, input_string):
        lines = input_string.split('\n')
        dict_list = []
        object_data = {}
        # Parse lines until first object key is found, and then
        # create new dictionary object
        for line in lines:
            if not line:
                continue
            key_value = line.split(self.KEY_VALUE_DELIMITER)
            key = key_value[0]
            value = self.KEY_VALUE_DELIMITER.join(key_value[1:]).strip()
            if key == self.FIRST_KEY:
                object_data = {}
                dict_list.append(object_data)
            object_data[key] = self.uge_to_py(key, value)
        return dict_list


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
