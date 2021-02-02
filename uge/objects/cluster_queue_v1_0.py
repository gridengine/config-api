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


class ClusterQueue(QconfObject):
    """ This class encapsulates UGE cluster queue object. """

    #: Object version. 
    VERSION = '1.0'

    #: Object name key.
    NAME_KEY = 'qname'

    #: Object keys that must be provided by user.
    USER_PROVIDED_KEYS = ['qname']

    #: Default values for required data keys.
    REQUIRED_DATA_DEFAULTS = {
        'hostlist': None,
        'seq_no': 0,
        'load_thresholds': 'np_load_avg=1.75',
        'suspend_thresholds': None,
        'nsuspend': 1,
        'suspend_interval': '00:05:00',
        'priority': 0,
        'min_cpu_interval': '00:05:00',
        'qtype': 'BATCH INTERACTIVE',
        'ckpt_list': None,
        'pe_list': 'make',
        'jc_list': ['NO_JC', 'ANY_JC'],
        'rerun': False,
        'slots': 1,
        'tmpdir': '/tmp',
        'shell': '/bin/sh',
        'prolog': None,
        'epilog': None,
        'shell_start_mode': 'unix_behavior',
        'starter_method': None,
        'suspend_method': None,
        'resume_method': None,
        'terminate_method': None,
        'notify': '00:00:60',
        'owner_list': None,
        'user_lists': None,
        'xuser_lists': None,
        'subordinate_list': None,
        'complex_values': None,
        'projects': None,
        'xprojects': None,
        'calendar': None,
        'initial_state': 'default',
        's_rt': float('inf'),
        'h_rt': float('inf'),
        'd_rt': float('inf'),
        's_cpu': float('inf'),
        'h_cpu': float('inf'),
        's_fsize': float('inf'),
        'h_fsize': float('inf'),
        's_data': float('inf'),
        'h_data': float('inf'),
        's_stack': float('inf'),
        'h_stack': float('inf'),
        's_core': float('inf'),
        'h_core': float('inf'),
        's_rss': float('inf'),
        'h_rss': float('inf'),
        's_vmem': float('inf'),
        'h_vmem': float('inf')
    }

    INT_KEY_MAP = QconfObject.get_int_key_map(REQUIRED_DATA_DEFAULTS)
    FLOAT_KEY_MAP = QconfObject.get_float_key_map(REQUIRED_DATA_DEFAULTS)
    DEFAULT_LIST_DELIMITER = ','
    LIST_KEY_MAP = {
        'slots': ',',
        'load_thresholds': ',',
        'suspend_thresholds': ',',
        'ckpt_list': ',',
        'pe_list': ',',
        'jc_list': ',',
        'owner_list': ',',
        'user_lists': ',',
        'xuser_lists': ',',
        'subordinate_list': ',',
        'complex_values': ',',
        'projects': ',',
        'xprojects': ',',
    }

    def __init__(self, name=None, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param name: Queue name. If provided, it will override queue name from data or JSON string parameters ('qname' key).
        :type name: str

        :param data: Queue data. If provided, it will override corresponding data from queue JSON string representation.
        :type data: dict

        :param metadata: Queue metadata. If provided, it will override corresponding metadata from queue JSON string representation.
        :type metadata: dict

        :param json_string: Queue JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing a ClusterQueue object.
        """

        QconfObject.__init__(self, name=name, data=data, metadata=metadata, json_string=json_string)
