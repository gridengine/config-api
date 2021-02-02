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


class ExecutionHost(QconfObject):
    """ This class encapsulates UGE execution host object. """

    #: Object version. 
    VERSION = '1.0'

    #: Object name key.
    NAME_KEY = 'hostname'

    #: Object keys that must be provided by user.
    USER_PROVIDED_KEYS = ['hostname']

    #: Default values for required data keys.
    REQUIRED_DATA_DEFAULTS = {
        'load_scaling': None,
        'complex_values': None,
        'user_lists': None,
        'xuser_lists': None,
        'projects': None,
        'xprojects': None,
        'usage_scaling': None,
        'report_variables': None,
        'license_constraints': None,
        'license_oversubscription': None,
    }
    INT_KEY_MAP = QconfObject.get_int_key_map(REQUIRED_DATA_DEFAULTS)
    FLOAT_KEY_MAP = QconfObject.get_float_key_map(REQUIRED_DATA_DEFAULTS)
    DEFAULT_LIST_DELIMITER = ','
    LIST_KEY_MAP = {
        'complex_values': ',',
        'user_lists': ',',
        'xuser_lists': ',',
        'projects': ',',
        'xprojects': ',',
        'report_variables': ',',
    }

    def __init__(self, name=None, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param name: Execution host name. If provided, it will override execution host name from data or JSON string parameters ('hostname' key).
        :type name: str

        :param data: Execution host data. If provided, it will override corresponding data from execution host JSON string representation.
        :type data: dict

        :param metadata: Execution host metadata. If provided, it will override corresponding metadata from execution host JSON string representation.
        :type metadata: dict

        :param json_string: Execution host JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing an ExecutionHost object.
        """
        QconfObject.__init__(self, name=name, data=data, metadata=metadata, json_string=json_string)
