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
import types
import random
from .utils import needs_uge
from .utils import generate_random_string
from .utils import create_config_file
from uge.exceptions.object_not_found import ObjectNotFound

from uge.api.qconf_api import QconfApi

create_config_file()
API = QconfApi()
ORIGINAL_STREE = None
PRJ1_NAME = 'prj%s' % generate_random_string(6)
PRJ1_SHARES = int(random.uniform(1,100))
PRJ2_NAME = 'prj%s' % generate_random_string(6)
PRJ2_SHARES = int(random.uniform(1,100))
PRJ3_NAME = 'prj%s' % generate_random_string(6)
PRJ3_SHARES = int(random.uniform(1,100))

@needs_uge
def test_stree_setup():
    try:
        ORIGINAL_STREE = API.get_stree()
        API.delete_stree()
    except ObjectNotFound:
        pass
    API.add_prj(name=PRJ1_NAME)
    API.add_prj(name=PRJ2_NAME)
    API.add_prj(name=PRJ3_NAME)

def test_generate_stree():
    stree = API.generate_stree(data=[
        {'id' : 0, 'name' : 'Root', 'type' : 0, 'shares' : 1, 'childnodes' : '1,2'}, 
        {'id' : 1, 'name' : PRJ1_NAME, 'shares' : PRJ1_SHARES}, 
        {'id' : 2, 'name' : PRJ2_NAME, 'shares' : PRJ2_SHARES}])
    assert(len(stree.data) == 3)
    assert(stree.data[1]['shares'] == PRJ1_SHARES)
    assert(stree.data[2]['shares'] == PRJ2_SHARES)

def test_add_stree():
    stree = API.add_stree(data=[
        {'id' : 0, 'name' : 'Root', 'type' : 0, 'shares' : 1, 'childnodes' : '1,2'}, 
        {'id' : 1, 'name' : PRJ1_NAME, 'shares' : PRJ1_SHARES}, 
        {'id' : 2, 'name' : PRJ2_NAME, 'shares' : PRJ2_SHARES}])
    assert(len(stree.data) == 3)
    assert(stree.data[0]['id'] == 0)
    assert(stree.data[1]['id'] == 1)
    assert(stree.data[1]['shares'] == PRJ1_SHARES)
    assert(stree.data[2]['id'] == 2)
    assert(stree.data[2]['shares'] == PRJ2_SHARES)

def test_get_stree():
    stree = API.get_stree()
    assert(len(stree.data) == 3)
    assert(stree.data[0]['id'] == 0)
    assert(stree.data[1]['id'] == 1)
    assert(stree.data[1]['shares'] == PRJ1_SHARES)
    assert(stree.data[2]['id'] == 2)
    assert(stree.data[2]['shares'] == PRJ2_SHARES)

def test_generate_stree_from_json():
    stree = API.get_stree()
    json = stree.to_json()
    stree2 = API.generate_object(json)
    assert(stree2.__class__.__name__ == stree.__class__.__name__)
    assert(len(stree.data) == len(stree2.data))
    for i in range(0,len(stree.data)):
        v = stree.data[i]
        v2 = stree2.data[i]
        assert(type(v) == dict)
        assert(type(v2) == dict)
        for key in list(v.keys()):
            x = v[key]
            x2 = v2[key]
            if type(x) == list:
                assert(len(x) == len(x2))
                for y in x:
                    assert(x2.count(y) == 1)
            else:
                assert(str(x) == str(x2))

def test_modify_stree():
    stree = API.get_stree()
    prj1_shares = stree.data[1]['shares']
    assert(prj1_shares == PRJ1_SHARES)
    stree.data[1]['shares'] = prj1_shares*2
    stree2 = API.modify_stree(stree)
    prj2_shares = stree2.data[1]['shares']
    assert(prj2_shares == 2*PRJ1_SHARES)

def test_add_stnode():
    stree = API.get_stree()
    stree_len = len(stree.data)
    stree2 = API.add_stnode('/%s' % PRJ3_NAME, PRJ3_SHARES)
    stree_len2 = len(stree2.data)
    assert(stree_len2 == stree_len+1)
    prj3_shares = stree2.data[-1]['shares']
    assert(prj3_shares == PRJ3_SHARES)

def test_delete_stnode():
    stree = API.get_stree()
    stree_len = len(stree.data)
    stree2 = API.delete_stnode('/%s' % PRJ3_NAME)
    stree_len2 = len(stree2.data)
    assert(stree_len2 == stree_len-1)

def test_delete_stree():
    API.delete_stree()
    try:
        stree = API.get_stree()
        assert(False)
    except ObjectNotFound as ex:
        pass

def test_modify_or_add_stree():
    stree = API.modify_or_add_stree(data=[
        {'id' : 0, 'name' : 'Root', 'type' : 0, 'shares' : 1, 'childnodes' : '1,2'}, 
        {'id' : 1, 'name' : PRJ1_NAME, 'shares' : PRJ1_SHARES}, 
        {'id' : 2, 'name' : PRJ2_NAME, 'shares' : PRJ2_SHARES}])
    assert(len(stree.data) == 3)
    assert(stree.data[0]['id'] == 0)
    assert(stree.data[1]['id'] == 1)
    assert(stree.data[1]['shares'] == PRJ1_SHARES)
    assert(stree.data[2]['id'] == 2)
    assert(stree.data[2]['shares'] == PRJ2_SHARES)

    stree = API.get_stree()
    prj1_shares = stree.data[1]['shares']
    assert(prj1_shares == PRJ1_SHARES)
    stree.data[1]['shares'] = prj1_shares*2
    stree2 = API.modify_or_add_stree(stree)
    prj2_shares = stree2.data[1]['shares']
    assert(prj2_shares == 2*PRJ1_SHARES)

def test_delete_stree_if_exists():
    # Delete share tree twice so we test case
    # when there is no share three defined
    API.delete_stree_if_exists()
    API.delete_stree_if_exists()

def test_get_stree_if_exists():
    stree = API.get_stree_if_exists()
    assert(len(stree.data) == 0)

def test_stree_cleanup():
    if ORIGINAL_STREE:
        API.add_stree(ORIGINAL_STREE)
    API.delete_prj(name=PRJ1_NAME)
    API.delete_prj(name=PRJ2_NAME)
    API.delete_prj(name=PRJ3_NAME)

