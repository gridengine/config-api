#!/usr/bin/env python
# 
# ___INFO__MARK_BEGIN__
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
# ___INFO__MARK_END__
# 
import types
from .utils import needs_uge
from .utils import generate_random_string
from .utils import create_config_file

from uge.api.qconf_api import QconfApi

create_config_file()
API = QconfApi()


@needs_uge
def test_generate_conf():
    conf = API.generate_conf(name='global')
    assert ('max_u_jobs' in conf.data)


def test_get_conf():
    conf = API.get_conf()
    assert ('max_u_jobs' in conf.data)


def test_generate_conf_from_json():
    conf = API.get_conf(name='global')
    json = conf.to_json()
    conf2 = API.generate_object(json)
    assert (conf2.__class__.__name__ == conf.__class__.__name__)
    for key in list(conf.data.keys()):
        v = conf.data[key]
        v2 = conf2.data[key]
        if type(v) == list:
            assert (len(v) == len(v2))
            for s in v:
                assert (v2.count(s) == 1)
        elif type(v) == dict:
            for key in list(v.keys()):
                assert (str(v[key]) == str(v2[key]))
        else:
            assert (str(v) == str(v2))


def test_modify_conf():
    conf = API.get_conf()
    max_u_jobs = conf.data['max_u_jobs']
    conf = API.modify_conf(name='global', data={'max_u_jobs': max_u_jobs * 2})
    max_u_jobs2 = conf.data['max_u_jobs']
    assert (max_u_jobs2 == max_u_jobs * 2)
    conf = API.modify_conf(data={'max_u_jobs': max_u_jobs})
    max_u_jobs3 = conf.data['max_u_jobs']
    assert (max_u_jobs3 == max_u_jobs)
