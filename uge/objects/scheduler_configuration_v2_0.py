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
from uge.objects.qconf_object import QconfObject


class SchedulerConfiguration(QconfObject):
    """ This class encapsulates UGE scheduler configuration object. """

    #: Object version. 
    VERSION = '2.0'

    #: Object name key.
    NAME_KEY = None

    #: Object keys that must be provided by user.
    USER_PROVIDED_KEYS = []

    #: Default values for required data keys.
    REQUIRED_DATA_DEFAULTS = {
        'algorithm': 'default',
        'schedule_interval': '0:0:15',
        'maxujobs': 0,
        'job_load_adjustments': 'np_load_avg=0.50',
        'load_adjustment_decay_time': '0:7:30',
        'host_sort_formula': 'np_load_avg',
        'schedd_job_info': False,
        'flush_submit_sec': 1,
        'flush_finish_sec': 1,
        'params': None,
        'reprioritize_interval': '0:0:0',
        'halftime': 168,
        'usage_weight_list': ['wallclock=0.000000', 'cpu=1.000000', 'mem=0.000000', 'io=0.000000'],
        'compensation_factor': 5.0,
        'weight_user': 0.25,
        'weight_project': 0.25,
        'weight_department': 0.25,
        'weight_job': 0.25,
        'weight_tickets_functional': 0,
        'weight_tickets_share': 0,
        'share_override_tickets': True,
        'share_functional_shares': True,
        'max_functional_jobs_to_schedule': 200,
        'report_pjob_tickets': True,
        'max_pending_tasks_per_job': 50,
        'halflife_decay_list': None,
        'policy_hierarchy': 'OFS',
        'weight_ticket': 0.01,
        'weight_waiting_time': 0.0,
        'weight_deadline': 3600000.0,
        'weight_urgency': 0.1,
        'weight_priority': 1.0,
        'fair_urgency_list': None,
        'max_reservation': 0,
        'default_duration': float('inf'),
        'backfilling': 'ON',
        'prioritize_preemptees': False,
        'preemptees_keep_resources': False,
        'max_preemptees': 0,
        'preemption_distance': '00:15:00',
        'preemption_priority_adjustments': None,
        'weight_host_affinity': 100.0,
        'weight_host_sort': 1.0,
        'weight_queue_affinity': 100.0,
        'weight_queue_host_sort': 10.0,
        'weight_queue_seqno': 1.0,
    }

    BOOL_KEY_MAP = QconfObject.get_bool_key_map(REQUIRED_DATA_DEFAULTS)
    INT_KEY_MAP = QconfObject.get_int_key_map(REQUIRED_DATA_DEFAULTS)
    FLOAT_KEY_MAP = QconfObject.get_float_key_map(REQUIRED_DATA_DEFAULTS)
    DEFAULT_LIST_DELIMITER = ','
    LIST_KEY_MAP = {
        'job_load_adjustments': ',',
        'fair_urgency_list': ',',
    }
    DEFAULT_DICT_DELIMITER = ','
    DICT_KEY_MAP = {
        'usage_weight_list': ',',
        'halflife_decay_list': ':',
    }

    UGE_CASE_SENSITIVE_KEYS = {
        'schedd_job_info': str.lower,
    }

    def __init__(self, data=None, metadata=None, json_string=None):
        """ 
        Class constructor. 

        :param data: Configuration data. If provided, it will override corresponding data from JSON string representation.
        :type data: dict

        :param metadata: Configuration metadata. If provided, it will override corresponding metadata from JSON string representation.
        :type metadata: dict

        :param json_string: Configuration JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing a SchedulerConfiguration object.
        """

        QconfObject.__init__(self, data=data, metadata=metadata, json_string=json_string)
