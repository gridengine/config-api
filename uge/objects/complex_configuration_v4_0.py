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
from uge.objects.complex_configuration_base import ComplexConfigurationBase


class ComplexConfiguration(ComplexConfigurationBase):
    """ This class encapsulates UGE complex configuration object. """

    #: Object version. 
    VERSION = '4.0'

    #: Object name key.
    NAME_KEY = None

    #: Object keys that must be provided by user.
    USER_PROVIDED_KEYS = []

    #: Default values for required data keys.
    REQUIRED_DATA_DEFAULTS = {
        'arch': {'shortcut': 'a', 'type': 'RESTRING', 'relop': '==', 'requestable': True, 'consumable': False,
                 'default': None, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                 'do_report': True, 'is_static': True},
        'calendar': {'shortcut': 'c', 'type': 'RESTRING', 'relop': '==', 'requestable': True, 'consumable': False,
                     'default': None, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                     'do_report': False, 'is_static': False},
        'cpu': {'shortcut': 'cpu', 'type': 'DOUBLE', 'relop': '>=', 'requestable': True, 'consumable': False,
                'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                'do_report': True, 'is_static': False},
        'd_rt': {'shortcut': 'd_rt', 'type': 'TIME', 'relop': '<=', 'requestable': True, 'consumable': False,
                 'default': '0:0:0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                 'do_report': False, 'is_static': False},
        'display_win_gui': {'shortcut': 'dwg', 'type': 'BOOL', 'relop': '==', 'requestable': True, 'consumable': False,
                            'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                            'do_report': False, 'is_static': False},
        'docker': {'shortcut': 'dock', 'type': 'BOOL', 'relop': '==', 'requestable': True, 'consumable': False,
                   'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': True, 'is_static': False},
        'docker_images': {'shortcut': 'dockimg', 'type': 'RESTRING', 'relop': '==', 'requestable': True,
                          'consumable': False, 'default': None, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                          'do_report': True, 'is_static': False},
        'h_core': {'shortcut': 'h_core', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                   'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': False, 'is_static': False},
        'h_cpu': {'shortcut': 'h_cpu', 'type': 'TIME', 'relop': '<=', 'requestable': True, 'consumable': False,
                  'default': '0:0:0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                  'do_report': False, 'is_static': False},
        'h_data': {'shortcut': 'h_data', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                   'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': False, 'is_static': False},
        'h_fsize': {'shortcut': 'h_fsize', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                    'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                    'do_report': False, 'is_static': False},
        'h_rss': {'shortcut': 'h_rss', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                  'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                  'do_report': False, 'is_static': False},
        'h_rt': {'shortcut': 'h_rt', 'type': 'TIME', 'relop': '<=', 'requestable': True, 'consumable': False,
                 'default': '0:0:0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                 'do_report': False, 'is_static': False},
        'h_stack': {'shortcut': 'h_stack', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                    'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                    'do_report': False, 'is_static': False},
        'h_vmem': {'shortcut': 'h_vmem', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                   'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': False, 'is_static': False},
        'hostname': {'shortcut': 'h', 'type': 'HOST', 'relop': '==', 'requestable': True, 'consumable': False,
                     'default': None, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                     'do_report': False, 'is_static': False},
        'load_avg': {'shortcut': 'la', 'type': 'DOUBLE', 'relop': '>=', 'requestable': False, 'consumable': False,
                     'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                     'do_report': True, 'is_static': False},
        'load_long': {'shortcut': 'll', 'type': 'DOUBLE', 'relop': '>=', 'requestable': False, 'consumable': False,
                      'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                      'do_report': True, 'is_static': False},
        'load_medium': {'shortcut': 'lm', 'type': 'DOUBLE', 'relop': '>=', 'requestable': False, 'consumable': False,
                        'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                        'do_report': True, 'is_static': False},
        'load_short': {'shortcut': 'ls', 'type': 'DOUBLE', 'relop': '>=', 'requestable': False, 'consumable': False,
                       'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                       'do_report': True, 'is_static': False},
        'm_cache_l1': {'shortcut': 'mcache1', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                       'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                       'do_report': True, 'is_static': True},
        'm_cache_l2': {'shortcut': 'mcache2', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                       'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                       'do_report': True, 'is_static': True},
        'm_cache_l3': {'shortcut': 'mcache3', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                       'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                       'do_report': True, 'is_static': True},
        'm_core': {'shortcut': 'core', 'type': 'INT', 'relop': '<=', 'requestable': True, 'consumable': False,
                   'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': True, 'is_static': True},
        'm_gpu': {'shortcut': 'mgpu', 'type': 'INT', 'relop': '<=', 'requestable': True, 'consumable': False,
                   'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': True, 'is_static': True},
        'm_mem_free': {'shortcut': 'mfree', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': True,
                       'default': '0', 'urgency': 0, 'aapre': True, 'affinity': 0.0,
                       'do_report': True, 'is_static': False},
        'm_mem_free_n0': {'shortcut': 'mfree0', 'type': 'MEMORY', 'relop': '<=', 'requestable': True,
                          'consumable': True, 'default': '0', 'urgency': 0, 'aapre': True, 'affinity': 0.0,
                          'do_report': True, 'is_static': False},
        'm_mem_free_n1': {'shortcut': 'mfree1', 'type': 'MEMORY', 'relop': '<=', 'requestable': True,
                          'consumable': True, 'default': '0', 'urgency': 0, 'aapre': True, 'affinity': 0.0,
                          'do_report': True, 'is_static': False},
        'm_mem_free_n2': {'shortcut': 'mfree2', 'type': 'MEMORY', 'relop': '<=', 'requestable': True,
                          'consumable': True, 'default': '0', 'urgency': 0, 'aapre': True, 'affinity': 0.0,
                          'do_report': True, 'is_static': False},
        'm_mem_free_n3': {'shortcut': 'mfree3', 'type': 'MEMORY', 'relop': '<=', 'requestable': True,
                          'consumable': True, 'default': '0', 'urgency': 0, 'aapre': True, 'affinity': 0.0,
                          'do_report': True, 'is_static': False},
        'm_mem_total': {'shortcut': 'mtotal', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': True,
                        'default': '0', 'urgency': 0, 'aapre': True, 'affinity': 0.0,
                        'do_report': True, 'is_static': True},
        'm_mem_total_n0': {'shortcut': 'mmem0', 'type': 'MEMORY', 'relop': '<=', 'requestable': True,
                           'consumable': True, 'default': '0', 'urgency': 0, 'aapre': True, 'affinity': 0.0,
                           'do_report': True, 'is_static': True},
        'm_mem_total_n1': {'shortcut': 'mmem1', 'type': 'MEMORY', 'relop': '<=', 'requestable': True,
                           'consumable': True, 'default': '0', 'urgency': 0, 'aapre': True, 'affinity': 0.0,
                           'do_report': True, 'is_static': True},
        'm_mem_total_n2': {'shortcut': 'mmem2', 'type': 'MEMORY', 'relop': '<=', 'requestable': True,
                           'consumable': True, 'default': '0', 'urgency': 0, 'aapre': True, 'affinity': 0.0,
                           'do_report': True, 'is_static': True},
        'm_mem_total_n3': {'shortcut': 'mmem3', 'type': 'MEMORY', 'relop': '<=', 'requestable': True,
                           'consumable': True, 'default': '0', 'urgency': 0, 'aapre': True, 'affinity': 0.0,
                           'do_report': True, 'is_static': True},
        'm_mem_used': {'shortcut': 'mused', 'type': 'MEMORY', 'relop': '>=', 'requestable': True, 'consumable': False,
                       'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                       'do_report': True, 'is_static': False},
        'm_mem_used_n0': {'shortcut': 'mused0', 'type': 'MEMORY', 'relop': '>=', 'requestable': True,
                          'consumable': False, 'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                          'do_report': True, 'is_static': False},
        'm_mem_used_n1': {'shortcut': 'mused1', 'type': 'MEMORY', 'relop': '>=', 'requestable': True,
                          'consumable': False, 'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                          'do_report': True, 'is_static': False},
        'm_mem_used_n2': {'shortcut': 'mused2', 'type': 'MEMORY', 'relop': '>=', 'requestable': True,
                          'consumable': False, 'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                          'do_report': True, 'is_static': False},
        'm_mem_used_n3': {'shortcut': 'mused3', 'type': 'MEMORY', 'relop': '>=', 'requestable': True,
                          'consumable': False, 'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                          'do_report': True, 'is_static': False},
        'm_numa_nodes': {'shortcut': 'nodes', 'type': 'INT', 'relop': '<=', 'requestable': True, 'consumable': False,
                         'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                         'do_report': True, 'is_static': True},
        'm_socket': {'shortcut': 'socket', 'type': 'INT', 'relop': '<=', 'requestable': True, 'consumable': False,
                     'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                     'do_report': True, 'is_static': True},
        'm_thread': {'shortcut': 'thread', 'type': 'INT', 'relop': '<=', 'requestable': True, 'consumable': False,
                     'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                     'do_report': True, 'is_static': True},
        'm_topology': {'shortcut': 'topo', 'type': 'RESTRING', 'relop': '==', 'requestable': True, 'consumable': False,
                       'default': None, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                       'do_report': True, 'is_static': True},
        'm_topology_inuse': {'shortcut': 'utopo', 'type': 'RESTRING', 'relop': '==', 'requestable': True,
                             'consumable': False, 'default': None, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                             'do_report': True, 'is_static': True},
        'm_topology_numa': {'shortcut': 'unuma', 'type': 'RESTRING', 'relop': '==', 'requestable': True,
                            'consumable': False, 'default': None, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                            'do_report': True, 'is_static': True},
        'mem_free': {'shortcut': 'mf', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                     'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                     'do_report': True, 'is_static': False},
        'mem_total': {'shortcut': 'mt', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                      'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                      'do_report': True, 'is_static': True},
        'mem_used': {'shortcut': 'mu', 'type': 'MEMORY', 'relop': '>=', 'requestable': True, 'consumable': False,
                     'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                     'do_report': True, 'is_static': False},
        'min_cpu_interval': {'shortcut': 'mci', 'type': 'TIME', 'relop': '<=', 'requestable': False,
                             'consumable': False, 'default': '0:0:0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                             'do_report': False, 'is_static': False},
        'np_load_avg': {'shortcut': 'nla', 'type': 'DOUBLE', 'relop': '>=', 'requestable': False, 'consumable': False,
                        'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                        'do_report': True, 'is_static': False},
        'np_load_long': {'shortcut': 'nll', 'type': 'DOUBLE', 'relop': '>=', 'requestable': False, 'consumable': False,
                         'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                         'do_report': True, 'is_static': False},
        'np_load_medium': {'shortcut': 'nlm', 'type': 'DOUBLE', 'relop': '>=', 'requestable': False,
                           'consumable': False, 'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                           'do_report': True, 'is_static': False},
        'np_load_short': {'shortcut': 'nls', 'type': 'DOUBLE', 'relop': '>=', 'requestable': False, 'consumable': False,
                          'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                          'do_report': True, 'is_static': False},
        'num_proc': {'shortcut': 'p', 'type': 'INT', 'relop': '==', 'requestable': True, 'consumable': False,
                     'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                     'do_report': True, 'is_static': True},
        'qname': {'shortcut': 'q', 'type': 'RESTRING', 'relop': '==', 'requestable': True, 'consumable': False,
                  'default': None, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                  'do_report': False, 'is_static': False},
        'rerun': {'shortcut': 're', 'type': 'BOOL', 'relop': '==', 'requestable': False, 'consumable': False,
                  'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                  'do_report': False, 'is_static': False},
        's_core': {'shortcut': 's_core', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                   'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': False, 'is_static': False},
        's_cpu': {'shortcut': 's_cpu', 'type': 'TIME', 'relop': '<=', 'requestable': True, 'consumable': False,
                  'default': '0:0:0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                  'do_report': False, 'is_static': False},
        's_data': {'shortcut': 's_data', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                   'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': False, 'is_static': False},
        's_fsize': {'shortcut': 's_fsize', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                    'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                    'do_report': False, 'is_static': False},
        's_rss': {'shortcut': 's_rss', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                  'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                  'do_report': False, 'is_static': False},
        's_rt': {'shortcut': 's_rt', 'type': 'TIME', 'relop': '<=', 'requestable': True, 'consumable': False,
                 'default': '0:0:0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                 'do_report': False, 'is_static': False},
        's_stack': {'shortcut': 's_stack', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                    'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                    'do_report': False, 'is_static': False},
        's_vmem': {'shortcut': 's_vmem', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                   'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': False, 'is_static': False},
        'seq_no': {'shortcut': 'seq', 'type': 'INT', 'relop': '==', 'requestable': False, 'consumable': False,
                   'default': 0, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': False, 'is_static': False},
        'slots': {'shortcut': 's', 'type': 'INT', 'relop': '<=', 'requestable': True, 'consumable': True, 'default': 1,
                  'urgency': 1000, 'aapre': True, 'affinity': 0.0,
                  'do_report': False, 'is_static': False},
        'swap_free': {'shortcut': 'sf', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                      'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                      'do_report': True, 'is_static': False},
        'swap_rate': {'shortcut': 'sr', 'type': 'MEMORY', 'relop': '>=', 'requestable': True, 'consumable': False,
                      'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                      'do_report': True, 'is_static': False},
        'swap_rsvd': {'shortcut': 'srsv', 'type': 'MEMORY', 'relop': '>=', 'requestable': True, 'consumable': False,
                      'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                      'do_report': True, 'is_static': False},
        'swap_total': {'shortcut': 'st', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                       'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                       'do_report': True, 'is_static': True},
        'swap_used': {'shortcut': 'su', 'type': 'MEMORY', 'relop': '>=', 'requestable': True, 'consumable': False,
                      'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                      'do_report': True, 'is_static': False},
        'tmpdir': {'shortcut': 'tmp', 'type': 'RESTRING', 'relop': '==', 'requestable': False, 'consumable': False,
                   'default': None, 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                   'do_report': False, 'is_static': False},
        'virtual_free': {'shortcut': 'vf', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                         'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                         'do_report': True, 'is_static': False},
        'virtual_total': {'shortcut': 'vt', 'type': 'MEMORY', 'relop': '<=', 'requestable': True, 'consumable': False,
                          'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                          'do_report': True, 'is_static': True},
        'virtual_used': {'shortcut': 'vu', 'type': 'MEMORY', 'relop': '>=', 'requestable': True, 'consumable': False,
                         'default': '0', 'urgency': 0, 'aapre': False, 'affinity': 0.0,
                         'do_report': True, 'is_static': False},
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

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing a ClusterConfiguration object.
        """

        ComplexConfigurationBase.__init__(self, data=data, metadata=metadata, json_string=json_string)
