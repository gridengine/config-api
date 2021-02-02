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
from .qconf_dict_list import QconfDictList
from .qconf_object import QconfObject


class ShareTree(QconfDictList):
    """ This class encapsulates UGE share tree object. """

    #: Object version. 
    VERSION = '1.0'

    #: Key that designates start of an object in a list
    FIRST_KEY = 'id'

    #: Object name key.
    NAME_KEY = None

    #: Object keys that must be provided by user.
    USER_PROVIDED_KEYS = ['name']

    #: Default values for required dictionary data keys.
    REQUIRED_DATA_DEFAULTS = {
        'id': 0,
        'name': None,
        'type': 1,
        'shares': 0,
        'childnodes': None,

    }

    BOOL_KEY_MAP = QconfObject.get_bool_key_map(REQUIRED_DATA_DEFAULTS)
    INT_KEY_MAP = QconfObject.get_int_key_map(REQUIRED_DATA_DEFAULTS)
    FLOAT_KEY_MAP = QconfObject.get_float_key_map(REQUIRED_DATA_DEFAULTS)
    DEFAULT_LIST_DELIMITER = ','

    def __init__(self, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param data: Configuration data. If provided, it will override corresponding data from JSON string representation.
        :type data: dict

        :param metadata: Configuration metadata. If provided, it will override corresponding metadata from JSON string representation.
        :type metadata: dict

        :param json_string: Configuration JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not represent a ShareTree object.
        """
        QconfDictList.__init__(self, data=data, metadata=metadata, json_string=json_string)

    def to_uge(self):
        """ 
        Converts object to string acceptable as input for UGE qconf command.

        :returns: Object's UGE-formatted string.
        """
        lines = ''
        for d in self.data:
            for key in ['id', 'name', 'type', 'shares', 'childnodes']:
                value = d.get(key)
                lines += '%s%s%s\n' % (key, self.KEY_VALUE_DELIMITER, self.py_to_uge(key, value))
        return lines


#############################################################################
# Testing.
if __name__ == '__main__':
    pass
