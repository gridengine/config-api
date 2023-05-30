#!/usr/bin/env python
# 
# ___INFO__MARK_BEGIN__ 
#######################################################################################
# Copyright 2016-2022 Altair Engineering Inc.
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
import copy

UGE_RELEASE_OBJECT_MAP = {}

# 8.3.1p9
UGE_RELEASE_OBJECT_MAP['8.3.1p9'] = {
    'AccessList'               : '1.0',
    'Calendar'                 : '1.0',
    'CheckpointingEnvironment' : '1.0',
    'ClusterConfiguration'     : '1.0',
    'ClusterQueue'             : '1.0',
    'ComplexConfiguration'     : '1.0',
    'ExecutionHost'            : '1.0',
    'HostGroup'                : '1.0',
    'JobClass'                 : '1.0',
    'ParallelEnvironment'      : '1.0',
    'Project'                  : '1.0',
    'ResourceQuotaSet'         : '1.0',
    'SchedulerConfiguration'   : '1.0',
    'ShareTree'                : '1.0',
    'User'                     : '1.0',
}

# 8.3.1p12
UGE_RELEASE_OBJECT_MAP['8.3.1p12'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.3.1p9'])

# 8.4.0
UGE_RELEASE_OBJECT_MAP['8.4.0'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.3.1p9'])
UGE_RELEASE_OBJECT_MAP['8.4.0']['ComplexConfiguration'] = '2.0'
    
# 8.4.3
UGE_RELEASE_OBJECT_MAP['8.4.3'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.4.0'])

# 8.4.4
UGE_RELEASE_OBJECT_MAP['8.4.4'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.4.0'])

# 8.4.5
UGE_RELEASE_OBJECT_MAP['8.4.5'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.4.0'])

# 8.5.0
UGE_RELEASE_OBJECT_MAP['8.5.0'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.4.0'])
UGE_RELEASE_OBJECT_MAP['8.5.0']['ClusterConfiguration'] = '2.0'
UGE_RELEASE_OBJECT_MAP['8.5.0']['JobClass'] = '2.0'

# 8.5.1
UGE_RELEASE_OBJECT_MAP['8.5.1'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.0'])

# 8.5.2
UGE_RELEASE_OBJECT_MAP['8.5.2'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.0'])

# 8.5.3
UGE_RELEASE_OBJECT_MAP['8.5.3'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.0'])

# 8.5.3_C104_1
UGE_RELEASE_OBJECT_MAP['8.5.3_C104_1'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.3'])
UGE_RELEASE_OBJECT_MAP['8.5.3_C104_1']['ParallelEnvironment'] = '2.0'

# 8.5.4
UGE_RELEASE_OBJECT_MAP['8.5.4'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.0'])

# 8.5.4_C104_1
UGE_RELEASE_OBJECT_MAP['8.5.4_C104_1'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.4'])
UGE_RELEASE_OBJECT_MAP['8.5.4_C104_1']['ParallelEnvironment'] = '2.0'

# 8.5.4_C104_2
UGE_RELEASE_OBJECT_MAP['8.5.4_C104_2'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.4_C104_1'])

# 8.5.4_C104_3
UGE_RELEASE_OBJECT_MAP['8.5.4_C104_3'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.4_C104_2'])

# 8.5.4_C104_4
UGE_RELEASE_OBJECT_MAP['8.5.4_C104_4'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.4_C104_3'])

# 8.5.4_C104_5
UGE_RELEASE_OBJECT_MAP['8.5.4_C104_5'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.4_C104_4'])

# 8.5.4_C104_6
UGE_RELEASE_OBJECT_MAP['8.5.4_C104_6'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.4_C104_5'])

# 8.5.5
UGE_RELEASE_OBJECT_MAP['8.5.5'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.0'])

# 8.5.6
UGE_RELEASE_OBJECT_MAP['8.5.6'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.0'])

# 8.6.0 (with affinity support)
UGE_RELEASE_OBJECT_MAP['8.6.0'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.5.0'])
UGE_RELEASE_OBJECT_MAP['8.6.0']['ClusterQueue'] = '2.0'
UGE_RELEASE_OBJECT_MAP['8.6.0']['ComplexConfiguration'] = '3.0'
UGE_RELEASE_OBJECT_MAP['8.6.0']['SchedulerConfiguration'] = '2.0'
UGE_RELEASE_OBJECT_MAP['8.6.0']['ParallelEnvironment'] = '2.0'
UGE_RELEASE_OBJECT_MAP['8.6.0']['JobClass'] = '3.0'

# 8.6.1
UGE_RELEASE_OBJECT_MAP['8.6.1'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.0'])

# 8.6.2
UGE_RELEASE_OBJECT_MAP['8.6.2'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.1'])

# 8.6.3
UGE_RELEASE_OBJECT_MAP['8.6.3'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.2'])

# 8.6.4
UGE_RELEASE_OBJECT_MAP['8.6.4'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.3'])

# 8.6.5
UGE_RELEASE_OBJECT_MAP['8.6.5'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.4'])

# 8.6.6
UGE_RELEASE_OBJECT_MAP['8.6.6'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.5'])

# 8.6.7
UGE_RELEASE_OBJECT_MAP['8.6.7prealpha'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.6'])
UGE_RELEASE_OBJECT_MAP['8.6.7alpha1'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.6'])
UGE_RELEASE_OBJECT_MAP['8.6.7'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.6'])

# 8.6.8
UGE_RELEASE_OBJECT_MAP['8.6.8prealpha'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.7'])
UGE_RELEASE_OBJECT_MAP['8.6.8'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.7'])

# 8.6.9
UGE_RELEASE_OBJECT_MAP['8.6.9prealpha'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.8'])
UGE_RELEASE_OBJECT_MAP['8.6.9'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.8'])

# 8.6.10
UGE_RELEASE_OBJECT_MAP['8.6.10prealpha'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.9'])

# 8.7.0
UGE_RELEASE_OBJECT_MAP['8.7.0alpha'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.6.0'])
UGE_RELEASE_OBJECT_MAP['8.7.0alpha']['SchedulerConfiguration'] = '3.0'
UGE_RELEASE_OBJECT_MAP['8.7.0alpha']['ComplexConfiguration'] = '4.0'
UGE_RELEASE_OBJECT_MAP['8.7.0alpha']['JobClass'] = '4.0'
UGE_RELEASE_OBJECT_MAP['8.7.0alpha2'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0alpha'])
UGE_RELEASE_OBJECT_MAP['8.7.0beta'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0alpha2'])
UGE_RELEASE_OBJECT_MAP['8.7.0beta2'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0beta'])
UGE_RELEASE_OBJECT_MAP['8.7.0beta3'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0beta2'])
UGE_RELEASE_OBJECT_MAP['8.7.0beta4'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0beta3'])
UGE_RELEASE_OBJECT_MAP['8.7.0beta5'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0beta4'])
UGE_RELEASE_OBJECT_MAP['8.7.0beta6'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0beta5'])
UGE_RELEASE_OBJECT_MAP['8.7.0beta7'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0beta6'])
UGE_RELEASE_OBJECT_MAP['8.7.0beta8'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0beta7'])
UGE_RELEASE_OBJECT_MAP['8.7.0beta9'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0beta8'])
UGE_RELEASE_OBJECT_MAP['8.7.0'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0beta9'])

# 8.7.1
UGE_RELEASE_OBJECT_MAP['8.7.1prealpha'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0'])
UGE_RELEASE_OBJECT_MAP['8.7.1'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.1prealpha'])

# 8.7.2
UGE_RELEASE_OBJECT_MAP['8.7.2prealpha'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.1'])
UGE_RELEASE_OBJECT_MAP['8.7.2prealpha2'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.1'])
UGE_RELEASE_OBJECT_MAP['8.7.2prealpha3'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.1'])
# if new version string shall be used (see uge/api/impl/*executor.py#get_uge_version)
# UGE_RELEASE_OBJECT_MAP['2022.1.0pre3'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0'])

UGE_RELEASE_OBJECT_MAP['8.7.2beta'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.1'])
UGE_RELEASE_OBJECT_MAP['8.7.2'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.1'])

# 8.7.3
UGE_RELEASE_OBJECT_MAP['8.7.3prealpha'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.2'])

# 8.8.0
UGE_RELEASE_OBJECT_MAP['8.8.0prealpha'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0'])
UGE_RELEASE_OBJECT_MAP['8.8.0prealpha2'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0'])
UGE_RELEASE_OBJECT_MAP['8.8.0'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.7.0'])
