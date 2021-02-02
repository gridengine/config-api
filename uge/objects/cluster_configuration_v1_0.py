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
import os
import tempfile
import string
from .qconf_object import QconfObject


class ClusterConfiguration(QconfObject):
    """ This class encapsulates UGE cluster configuration object. """

    #: Object version. 
    VERSION = '1.0'

    #: Object name key.
    NAME_KEY = None

    #: Object keys that must be provided by user.
    USER_PROVIDED_KEYS = []

    #: Default values for required data keys for the global configuration. 
    #: Value for execd_spool_dir key will depend on $SGE_ROOT and $SGE_CELL.
    REQUIRED_GLOBAL_DATA_DEFAULTS = {
        'execd_spool_dir': 'SGE_ROOT/SGE_CELL/spool',
        'mailer': '/bin/mail',
        'xterm': '/usr/bin/xterm',
        'load_sensor': None,
        'prolog': None,
        'epilog': None,
        'shell_start_mode': 'unix_behavior',
        'login_shells': ['sh', 'bash', 'ksh', 'csh', 'tcsh'],
        'min_uid': 0,
        'min_gid': 0,
        'user_lists': None,
        'xuser_lists': None,
        'projects': None,
        'xprojects': None,
        'default_jc': None,
        'enforce_jc': False,
        'enforce_project': False,
        'enforce_user': 'auto',
        'load_report_time': '00:00:40',
        'max_unheard': '00:04:00',
        'reschedule_unknown': '00:00:00',
        'loglevel': 'log_warning',
        'administrator_mail': None,
        'set_token_cmd': None,
        'pag_cmd': None,
        'token_extend_time': None,
        'shepherd_cmd': None,
        'qmaster_params': None,
        'execd_params': ['KEEP_ACTIVE=ERROR'],
        'reporting_params': {'accounting': True, 'reporting': False, 'flush_time': '00:00:13', 'joblog': False,
                             'sharelog': '00:00:00'},
        'finished_jobs': 0,
        'gid_range': '20000-20100',
        'qlogin_command': 'builtin',
        'qlogin_daemon': 'builtin',
        'rlogin_command': 'builtin',
        'rlogin_daemon': 'builtin',
        'rsh_command': 'builtin',
        'rsh_daemon': 'builtin',
        'max_aj_instances': 2000,
        'max_aj_tasks': 75000,
        'max_u_jobs': 0,
        'max_jobs': 0,
        'max_advance_reservations': 0,
        'auto_user_oticket': 0,
        'auto_user_fshare': 0,
        'auto_user_default_project': None,
        'auto_user_delete_time': 86400,
        'delegated_file_staging': False,
        'reprioritize': 0,
        'jsv_url': None,
        'jsv_allowed_mod': ['ac', 'h', 'i', 'e', 'o', 'j', 'M', 'N', 'p', 'w'],
        'cgroups_params': {'cgroup_path': None, 'cpuset': False, 'mount': False, 'freezer': False,
                           'freeze_pe_tasks': False, 'killing': False, 'forced_numa': False, 'h_vmem_limit': False,
                           'm_mem_free_hard': False, 'm_mem_free_soft': False, 'min_memory_limit': 0},
        'lost_job_timeout': '00:00:00',
        'enable_lost_job_reschedule': False,
    }

    #: Default values for required data keys for the host configuration. 
    REQUIRED_HOST_DATA_DEFAULTS = {
        'mailer': '/bin/mail',
        'xterm': '/usr/bin/xterm',
    }

    BOOL_KEY_MAP = QconfObject.get_bool_key_map(REQUIRED_GLOBAL_DATA_DEFAULTS)
    INT_KEY_MAP = QconfObject.get_int_key_map(REQUIRED_GLOBAL_DATA_DEFAULTS)
    FLOAT_KEY_MAP = QconfObject.get_float_key_map(REQUIRED_GLOBAL_DATA_DEFAULTS)
    DEFAULT_LIST_DELIMITER = ','
    LIST_KEY_MAP = {
        'login_shells': ',',
        'user_lists': ',',
        'xuser_lists': ',',
        'projects': ',',
        'xprojects': ',',
        'qmaster_params': ',',
        'execd_params': ',',
        'jsv_allowed_mod': ',',
    }
    DEFAULT_DICT_DELIMITER = ' '
    DICT_KEY_MAP = {
        'reporting_params': ' ',
        'cgroups_params': ' ',
    }

    UGE_CASE_SENSITIVE_KEYS = {
    }

    def __init__(self, name='global', data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param name: Configuration name (default: 'global').
        :type name: str

        :param data: Configuration data. If provided, it will override corresponding data from JSON string representation.
        :type data: dict

        :param metadata: Configuration metadata. If provided, it will override corresponding metadata from JSON string representation.
        :type metadata: dict

        :param json_string: Configuration JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing a ClusterConfiguration object.
        """

        QconfObject.__init__(self, name=name, data=data, metadata=metadata, json_string=json_string)
        if not self.name:
            self.name = self.get_name_from_data()
            if not self.name:
                self.name = 'global'

    def get_name_from_data(self):
        for (key, value) in list(self.data.items()):
            if key.startswith('#'):
                return key[1:-1]  # remove comment and ending column characters
        return None

    def get_required_data_defaults(self):
        if self.name == 'global':
            return self.REQUIRED_GLOBAL_DATA_DEFAULTS
        else:
            return self.REQUIRED_HOST_DATA_DEFAULTS

    def get_tmp_file(self):
        tmp_dir_path = tempfile.mkdtemp()
        tmp_file_path = os.path.join(tmp_dir_path, self.name)
        tmp_file = open(tmp_file_path, 'w')
        return tmp_file, tmp_file_path, tmp_dir_path
