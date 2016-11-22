#!/usr/bin/env python
# 
#___INFO__MARK_BEGIN__ 
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
#___INFO__MARK_END__ 
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

# 8.5.0
UGE_RELEASE_OBJECT_MAP['8.5.0'] = copy.copy(UGE_RELEASE_OBJECT_MAP['8.4.0'])
