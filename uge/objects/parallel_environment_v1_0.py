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


class ParallelEnvironment(QconfObject):
    """ This class encapsulates UGE parallel environment object. """

    #: Object version. 
    VERSION = '1.0'

    #: Object name key.
    NAME_KEY = 'pe_name'

    #: Object keys that must be provided by user.
    USER_PROVIDED_KEYS = ['pe_name']

    #: Default values for required data keys.
    REQUIRED_DATA_DEFAULTS = {
        'slots': 0,
        'user_lists': None,
        'xuser_lists': None,
        'start_proc_args': None,
        'stop_proc_args': None,
        'allocation_rule': '$pe_slots',
        'control_slaves': False,
        'job_is_first_task': True,
        'urgency_slots': 'min',
        'accounting_summary': False,
        'daemon_forks_slaves': False,
        'master_forks_slaves': False,
    }

    INT_KEY_MAP = QconfObject.get_int_key_map(REQUIRED_DATA_DEFAULTS)
    FLOAT_KEY_MAP = QconfObject.get_float_key_map(REQUIRED_DATA_DEFAULTS)
    DEFAULT_LIST_DELIMITER = ' '
    LIST_KEY_MAP = {
        'user_lists': ' ',
        'xuser_lists': ' ',
    }

    def __init__(self, name=None, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param name: PE name. If provided, it will override PE name from data or JSON string parameters ('pe_name' key).
        :type name: str

        :param data: PE data. If provided, it will override corresponding data from PE JSON string representation.  :type data: dict

        :param metadata: PE metadata. If provided, it will override corresponding metadata from PE JSON string representation.
        :type metadata: dict

        :param json_string: PE JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing a PE object.
        """
        QconfObject.__init__(self, name=name, data=data, metadata=metadata, json_string=json_string)
