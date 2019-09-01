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
from nose import SkipTest

from .utils import needs_uge
from .utils import generate_random_string
from .utils import create_config_file

from uge.api.ar_api import AdvanceReservationApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
AR_API = AdvanceReservationApi()
# AR_NAME = '%s' % generate_random_string(6)
# CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()
logger = LOG_MANAGER.get_logger('test_ar')


@needs_uge
def test_request_ar():
    ar_id = AR_API.request_ar('-d 3600 -fr y')
    ar = AR_API.get_ar(ar_id)
    logger.info('AR: ', ar)
    assert (ar_id is not None)


def test_request_sr():
    ar_id = AR_API.request_ar('-cal_week mon-fri=8-16=on')
    ar = AR_API.get_ar(ar_id)
    logger.info('SR: ', ar)
    assert (ar_id is not None)


def test_get_ar_summary():
    ar_summary = AR_API.get_ar_summary()
    logger.info(ar_summary)
    assert (ar_summary is not None)


def test_get_ar():
    for ar_id in AR_API.get_ar_list():
        ar = AR_API.get_ar(str(ar_id))
        assert (ar is not None)
    else:
        raise SkipTest('There are no UGE advance reservations.')


def test_delete_all_ar():
    for ar_id in AR_API.get_ar_list():
        AR_API.delete_ar(ar_id)
