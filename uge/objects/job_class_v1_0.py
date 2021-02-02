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


class JobClass(QconfObject):
    """ This class encapsulates UGE job class object. """

    #: Object version. 
    VERSION = '1.0'

    #: Object name key.
    NAME_KEY = 'jcname'

    #: Object keys that must be provided by user.
    USER_PROVIDED_KEYS = ['jcname']

    #: Default values for required data keys.
    REQUIRED_DATA_DEFAULTS = {
        'variant_list': None,
        'owner': None,
        'user_lists': None,
        'xuser_lists': None,
        'A': '{+}UNSPECIFIED',
        'a': '{+}UNSPECIFIED',
        'ar': '{+}UNSPECIFIED',
        'b': '{+}UNSPECIFIED',
        'binding': '{+}UNSPECIFIED',
        'c_interval': '{+}UNSPECIFIED',
        'c_occasion': '{+}UNSPECIFIED',
        'CMDNAME': '{+}UNSPECIFIED',
        'CMDARG': '{+}UNSPECIFIED',
        'ckpt': '{+}UNSPECIFIED',
        'ac': '{+}UNSPECIFIED',
        'cwd': '{+}UNSPECIFIED',
        'dl': '{+}UNSPECIFIED',
        'e': '{+}UNSPECIFIED',
        'h': '{+}UNSPECIFIED',
        'hold_jid': '{+}UNSPECIFIED',
        'hold_jid_ad': '{+}UNSPECIFIED',
        'i': '{+}UNSPECIFIED',
        'j': '{+}UNSPECIFIED',
        'js': '{+}UNSPECIFIED',
        'l_hard': '{+}UNSPECIFIED',
        'l_soft': '{+}UNSPECIFIED',
        'masterl': '{+}UNSPECIFIED',
        'm': '{+}UNSPECIFIED',
        'mbind': '{+}UNSPECIFIED',
        'M': '{+}UNSPECIFIED',
        'masterq': '{+}UNSPECIFIED',
        'N': '{+}UNSPECIFIED',
        'notify': '{+}UNSPECIFIED',
        'now': '{+}UNSPECIFIED',
        'o': '{+}UNSPECIFIED',
        'P': '{+}UNSPECIFIED',
        'p': '{+}UNSPECIFIED',
        'pe_name': '{+}UNSPECIFIED',
        'pe_range': '{+}UNSPECIFIED',
        'q_hard': '{+}UNSPECIFIED',
        'q_soft': '{+}UNSPECIFIED',
        'R': '{+}UNSPECIFIED',
        'r': '{+}UNSPECIFIED',
        'rou': '{+}UNSPECIFIED',
        'S': '{+}UNSPECIFIED',
        'shell': '{+}UNSPECIFIED',
        't': '{+}UNSPECIFIED',
        'tc': '{+}UNSPECIFIED',
        'V': '{+}UNSPECIFIED',
        'v': '{+}UNSPECIFIED',
    }

    INT_KEY_MAP = QconfObject.get_int_key_map(REQUIRED_DATA_DEFAULTS)
    FLOAT_KEY_MAP = QconfObject.get_float_key_map(REQUIRED_DATA_DEFAULTS)
    DEFAULT_LIST_DELIMITER = ','
    LIST_KEY_MAP = {
        'variant_list': ',',
        'user_lists': ',',
        'xuser_lists': ',',
    }

    def __init__(self, name=None, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param name: Job class name. If provided, it will override job class name from data or JSON string parameters ('jcname' key).
        :type name: str

        :param data: Job class data. If provided, it will override corresponding data from job class JSON string representation.
        :type data: dict

        :param metadata: Job class metadata. If provided, it will override corresponding metadata from job class JSON string representation.
        :type metadata: dict

        :param json_string: Job class JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing a JobClass object.
        """

        QconfObject.__init__(self, name=name, data=data, metadata=metadata, json_string=json_string)
