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
from .utils import needs_uge
from .utils import generate_random_string
from .utils import create_config_file

from uge.api.qconf_api import QconfApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
API = QconfApi()
CALENDAR_NAME = '%s' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()


@needs_uge
def test_object_not_found():
    try:
        calendar = API.get_cal('__non_existent_calendar__')
        assert (False)
    except ObjectNotFound as ex:
        # ok
        pass


def test_generate_cal():
    calendar = API.generate_cal(CALENDAR_NAME)
    assert (calendar.data['calendar_name'] == CALENDAR_NAME)


def test_add_cal():
    try:
        calendar_list = API.list_cals()
    except ObjectNotFound as ex:
        # no calendars defined
        calendar_list = []
    calendar = API.add_cal(name=CALENDAR_NAME)
    assert (calendar.data['calendar_name'] == CALENDAR_NAME)
    calendar_list2 = API.list_cals()
    assert (len(calendar_list2) == len(calendar_list) + 1)
    assert (calendar_list2.count(CALENDAR_NAME) == 1)


def test_list_cals():
    calendar_list = API.list_cals()
    assert (calendar_list is not None)


def test_object_already_exists():
    try:
        calendar = API.add_cal(name=CALENDAR_NAME)
        assert (False)
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_get_cal():
    calendar = API.get_cal(CALENDAR_NAME)
    assert (calendar.data['calendar_name'] == CALENDAR_NAME)


def test_generate_cal_from_json():
    cal = API.get_cal(CALENDAR_NAME)
    assert (cal.data['calendar_name'] == CALENDAR_NAME)
    json = cal.to_json()
    cal2 = API.generate_object(json)
    assert (cal2.__class__.__name__ == cal.__class__.__name__)
    for key in list(cal.data.keys()):
        v = cal.data[key]
        v2 = cal2.data[key]
        assert (str(v) == str(v2))


def test_modify_cal():
    calendar = API.get_cal(CALENDAR_NAME)
    week = calendar.data['week']
    calendar = API.modify_cal(name=CALENDAR_NAME, data={'week': '1-2'})
    week2 = calendar.data['week']
    assert (week2 == '1-2')


def test_delete_cal():
    calendar_list = API.list_cals()
    API.delete_cal(CALENDAR_NAME)
    try:
        calendar_list2 = API.list_cals()
    except ObjectNotFound as ex:
        # no calendars defined
        calendar_list2 = []
    assert (len(calendar_list2) == len(calendar_list) - 1)
    assert (calendar_list2.count(CALENDAR_NAME) == 0)
