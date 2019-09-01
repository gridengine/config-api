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
from .qconf_object import QconfObject


class Project(QconfObject):
    """ This class encapsulates UGE project object. """

    #: Object version. 
    VERSION = '1.0'

    #: Object name key.
    NAME_KEY = 'name'

    #: Object keys that must be provided by user.
    USER_PROVIDED_KEYS = ['name']

    #: Default values for required data keys.
    REQUIRED_DATA_DEFAULTS = {
        'oticket': 0,
        'fshare': 0,
        'acl': None,
        'xacl': None,
    }
    INT_KEY_MAP = QconfObject.get_int_key_map(REQUIRED_DATA_DEFAULTS)
    FLOAT_KEY_MAP = QconfObject.get_float_key_map(REQUIRED_DATA_DEFAULTS)
    DEFAULT_LIST_DELIMITER = ' '
    LIST_KEY_MAP = {
        'acl': ' ',
        'xacl': ' ',
    }

    def __init__(self, name=None, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param name: Project name. If provided, it will override project name from data or JSON string parameters ('name' key).
        :type name: str

        :param data: Project data. If provided, it will override corresponding data from project JSON string representation.
        :type data: dict

        :param metadata: Project metadata. If provided, it will override corresponding metadata from project JSON string representation.
        :type metadata: dict

        :param json_string: Project JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing an Project object.
        """
        QconfObject.__init__(self, name=name, data=data, metadata=metadata, json_string=json_string)
