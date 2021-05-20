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
from nose import SkipTest

from .utils import needs_uge
from .utils import generate_random_string
from .utils import create_config_file

from uge.api.ar_api import AdvanceReservationApi
from uge.api.qconf_api import QconfApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
API = QconfApi()
PE_NAME = '%s.q' % generate_random_string(6)
QUEUE_NAME = '%s.q' % generate_random_string(6)
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


def test_ar_per_pe_request():
    hl = API.list_shosts()
    assert (hl is not None)
    h = hl[0]
    assert (h is not None)

    slots = str(99999)

    pe = API.add_pe(name=PE_NAME, data={'slots': slots})
    assert (pe.data['pe_name'] == PE_NAME)

    q = API.add_queue(name=QUEUE_NAME, data={'slots': slots, 'pe_list': PE_NAME, 'hostlist': '@allhosts'})
    assert (q.data['qname'] == QUEUE_NAME)

    request = "-d 3600 -pe {} 4 -fr y -petask 0 -l h={}".format(PE_NAME, h)
    ar_id = AR_API.request_ar(request)
    ar = AR_API.get_ar(ar_id)
    logger.info('AR: ', ar)
    assert (ar is not None)
    pe_range = ar['qrstat']['ar_summary'][0]['resource_descriptor_list'][0]['pe_range']
    assert(pe_range == '0')

    # Cleanup
    AR_API.delete_ar(ar_id)
    API.delete_queue(QUEUE_NAME)
    API.delete_pe(PE_NAME)
