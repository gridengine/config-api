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
from uge.objects.ar_object_factory import AdvanceReservationObjectFactory

__docformat__ = 'reStructuredText'

import os
from functools import wraps
from decorator import decorator
from uge.log.log_manager import LogManager
from uge.exceptions.ar_exception import AdvanceReservationException
from uge.exceptions.configuration_error import ConfigurationError
from uge.api.impl.qrstat_executor import QrstatExecutor
from uge.api.impl.qrsub_executor import QrsubExecutor
from uge.api.impl.qrdel_executor import QrdelExecutor
from uge.api.impl.ar_manager import AdvanceReservationManager
import collections


class AdvanceReservationApi(object):
    """ High-level advance reservation API class. """

    DEFAULT_SGE_CELL = 'default'
    DEFAULT_SGE_QMASTER_PORT = 6444
    DEFAULT_SGE_EXECD_PORT = 6445

    logger = None

    def __init__(self, sge_root=None, sge_cell=None,
                 sge_qmaster_port=None, sge_execd_port=None):
        """ 
        Class constructor. 

        :param sge_root: SGE root directory. It can be set via environment variable SGE_ROOT. 
        :type sge_root: str

        :param sge_cell: SGE cell name. It can be set via environment variable SGE_CELL. Default cell name is 'default'.
        :type sge_cell: str

        :param sge_qmaster_port: SGE Qmaster port. It can be set via environment variable SGE_QMASTER_PORT. Default port is 6444. 
        :type sge_qmaster_port: int

        :param sge_execd_port: SGE Execd port. It can be set via environment variable SGE_EXECD_PORT. Default port is 6445.
        :type sge_execd_port: int

        :raises ConfigurationError: in case sge_root is not provided, and environment variable SGE_ROOT is not defined.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises AdvanceReservationException: for any other errors.

        >>> api = AdvanceReservationApi(sge_root='/opt/uge')
        """
        self.__configure(sge_root, sge_cell, sge_qmaster_port, sge_execd_port)

    def __configure(self, sge_root, sge_cell, sge_qmaster_port,
                    sge_execd_port):
        self.get_logger()
        if not sge_root:
            sge_root = os.environ.get('SGE_ROOT')
            if not sge_root:
                raise ConfigurationError('SGE_ROOT is not defined.')
        if not sge_cell:
            sge_cell = os.environ.get('SGE_CELL', self.DEFAULT_SGE_CELL)
        if not sge_qmaster_port:
            sge_qmaster_port = os.environ.get('SGE_QMASTER_PORT', self.DEFAULT_SGE_QMASTER_PORT)
        if not sge_execd_port:
            sge_execd_port = os.environ.get('SGE_EXECD_PORT', self.DEFAULT_SGE_EXECD_PORT)

        self.logger.debug('Configuration: SGE_ROOT=%s, SGE_CELL=%s, SGE_QMASTER_PORT=%s, SGE_EXECD_PORT=%s' % (
        sge_root, sge_cell, sge_qmaster_port, sge_execd_port))
        self.qrstat_executor = QrstatExecutor(
            sge_root=sge_root, sge_cell=sge_cell,
            sge_qmaster_port=sge_qmaster_port,
            sge_execd_port=sge_qmaster_port)
        self.qrsub_executor = QrsubExecutor(
            sge_root=sge_root, sge_cell=sge_cell,
            sge_qmaster_port=sge_qmaster_port,
            sge_execd_port=sge_qmaster_port)
        self.qrdel_executor = QrdelExecutor(
            sge_root=sge_root, sge_cell=sge_cell,
            sge_qmaster_port=sge_qmaster_port,
            sge_execd_port=sge_qmaster_port)
        self.ar_manager = AdvanceReservationManager(self.qrstat_executor, self.qrsub_executor, self.qrdel_executor)

    @classmethod
    def get_logger(cls):
        if not cls.logger:
            cls.logger = LogManager.get_instance().get_logger(cls.__name__)
        return cls.logger

    def api_call2(func):
        @wraps(func)
        def wrapped_call(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except AdvanceReservationException as ex:
                raise
            except Exception as ex:
                raise AdvanceReservationException(exception=ex)

        return decorator(wrapped_call, func)

    # Make sure only ar specific exceptions are raised
    # Use two decorators to keep signature for documentation
    def api_call(*dargs, **dkwargs):
        def internal_call(func):
            @wraps(func)
            def wrapped_call(func, *args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    return result
                except AdvanceReservationException as ex:
                    raise
                except Exception as ex:
                    raise AdvanceReservationException(exception=ex)

            return decorator(wrapped_call, func)

        if len(dargs) == 1 and isinstance(dargs[0], collections.Callable):
            return internal_call(dargs[0])
        else:
            return internal_call

    def get_uge_version(self):
        """ Get version of UGE qmaster that API is connected to.

        :returns: UGE version string.

        :raises AdvanceReservationException: in case of any errors.
        """
        return self.qrstat_executor.get_uge_version()

    def generate_object(self, json_string, target_uge_version=None):
        """ Use specified JSON string to generate object for the target UGE version.
 
        :param json_string: input object's JSON string representation 
        :type json_string: str

        :param target_uge_version: target UGE version
        :type json_string: str

        :returns: Generated Qconf object.

        :raises AdvanceReservationException: in case of any errors.
        """
        return AdvanceReservationObjectFactory.generate_object(json_string, target_uge_version)

    @api_call
    def get_ar(self, name):
        """ Retrieve UGE advance reservation info.

        :param name: ar id.
        :type name: str

        :returns: ar as json string

        :raises ObjectNotFound: in case cluster queue object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises AdvanceReservationException: for any other errors.

        >>> ar = api.get_ar('123')
        >>> all_q.data['load_thresholds']
        'np_load_avg=2.0'
        """
        return self.qrstat_executor.get_ar(name)

    @api_call
    def get_ar_summary(self):
        """ List UGE advance reservations.

        :returns: advance reservation summary.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises AdvanceReservationException: for any other errors.

        >>> ar_summary = api.get_ar_summary()
        >>> ar_summary
        ['all.q']
        >>> ar_summary.__class__.__name__
        'QconfNameList'
        """
        return self.qrstat_executor.get_ar_summary()

    @api_call
    def get_ar_list(self):
        """ List UGE advance reservation ids.
        :returns: advance reservation id list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises AdvanceReservationException: for any other errors.

        >>> ar_summary = api.get_ar_list()
        >>> ar_summary
        ['all.q']
        >>> ar_summary.__class__.__name__
        'QconfNameList'
        """
        return self.qrstat_executor.get_ar_list()

    @api_call
    def request_ar(self, argstr):
        """ Request UGE advance reservation.

        :param pycl_object: Cluster queue object to be added.
        :type pycl_object: ClusterQueue 

        :param name: Cluster queue name; if provided, it will override queue name in the provided cluster queue object, data dictionary, or in the json string.
        :type name: str

        :param data: Queue data dictionary; if provided, dictionary values will override corresponding values from the cluster queue object, or from the JSON string.
        :type data: dict

        :param metadata: Queue metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the queue object to be added.
        :type json_string: str

        :returns: Newly added advance reservation id object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ClusterQueue, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify cluster queue name.
        :raises ObjectAlreadyExists: in case cluster queue object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the cluster queue data does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises AdvanceReservationException: for any other errors.

        >>> new_q = api.request_ar(name='new.q', data={'slots' : 3})
        >>> 123
        <uge.objects.cluster_queue_v1_0.ClusterQueue object at 0x7fc32e14ef50>
        >>> new_q.data['slots']
        3
        """
        return self.qrsub_executor.request_ar(argstr)

    @api_call
    def delete_ar(self, name):
        """ Delete UGE advance reservation.

        :param name: ar id.
        :type name: str

        :raises ObjectNotFound: in case advance reservation object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises AdvanceReservationException: for any other errors.

        >>> api.delete_ar('123')
        """
        return self.qrdel_executor.delete_ar(name)


#############################################################################
# Testing.
if __name__ == '__main__':
    lm = LogManager.get_instance()
    lm.set_console_log_level('trace')
    api = AdvanceReservationApi()
    print(api.get_uge_version())
    ar_id1 = api.request_ar('-d 3600 -fr y')
    ar1 = api.get_ar(ar_id1)
    print('AR 1: ', ar1)
    ar_id2 = api.request_ar('-cal_week mon-fri=8-16=on')
    ar2 = api.get_ar(ar_id2)
    print('AR 2: ', ar2)
    ar_summary = api.get_ar_summary()
    print('AR SUMMARY: ', ar_summary)
    print('AR LIST: ', api.get_ar_list())
    print(api.delete_ar(ar_id1))
    print(api.delete_ar(ar_id2))
