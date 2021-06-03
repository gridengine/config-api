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
__docformat__ = 'reStructuredText'

import os
from functools import wraps
from decorator import decorator
from uge.log.log_manager import LogManager
from uge.exceptions.qconf_exception import QconfException
from uge.exceptions.configuration_error import ConfigurationError
from uge.objects.qconf_object_factory import QconfObjectFactory
from uge.api.impl.qconf_executor import QconfExecutor
from uge.api.impl.cluster_queue_manager import ClusterQueueManager
from uge.api.impl.execution_host_manager import ExecutionHostManager
from uge.api.impl.host_group_manager import HostGroupManager
from uge.api.impl.submit_host_manager import SubmitHostManager
from uge.api.impl.admin_host_manager import AdminHostManager
from uge.api.impl.operator_manager import OperatorManager
from uge.api.impl.manager_manager import ManagerManager
from uge.api.impl.parallel_environment_manager import ParallelEnvironmentManager
from uge.api.impl.user_manager import UserManager
from uge.api.impl.project_manager import ProjectManager
from uge.api.impl.calendar_manager import CalendarManager
from uge.api.impl.checkpointing_environment_manager import CheckpointingEnvironmentManager
from uge.api.impl.access_list_manager import AccessListManager
from uge.api.impl.scheduler_configuration_manager import SchedulerConfigurationManager
from uge.api.impl.job_class_manager import JobClassManager
from uge.api.impl.cluster_configuration_manager import ClusterConfigurationManager
from uge.api.impl.complex_configuration_manager import ComplexConfigurationManager
from uge.api.impl.resource_quota_set_manager import ResourceQuotaSetManager
from uge.api.impl.share_tree_manager import ShareTreeManager

try:
    import UserList
except ImportError:
    import collections as UserList


class QconfApi(object):
    """ High-level qconf API class. """

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
        :raises QconfException: for any other errors.

        >>> api = QconfApi(sge_root='/opt/uge')
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
        self.qconf_executor = QconfExecutor(
            sge_root=sge_root, sge_cell=sge_cell,
            sge_qmaster_port=sge_qmaster_port,
            sge_execd_port=sge_qmaster_port)
        self.cluster_queue_manager = ClusterQueueManager(self.qconf_executor)
        self.execution_host_manager = ExecutionHostManager(self.qconf_executor)
        self.host_group_manager = HostGroupManager(self.qconf_executor)
        self.submit_host_manager = SubmitHostManager(self.qconf_executor)
        self.admin_host_manager = AdminHostManager(self.qconf_executor)
        self.operator_manager = OperatorManager(self.qconf_executor)
        self.manager_manager = ManagerManager(self.qconf_executor)
        self.parallel_environment_manager = ParallelEnvironmentManager(self.qconf_executor)
        self.user_manager = UserManager(self.qconf_executor)
        self.project_manager = ProjectManager(self.qconf_executor)
        self.calendar_manager = CalendarManager(self.qconf_executor)
        self.checkpointing_environment_manager = CheckpointingEnvironmentManager(self.qconf_executor)
        self.access_list_manager = AccessListManager(self.qconf_executor)
        self.scheduler_configuration_manager = SchedulerConfigurationManager(self.qconf_executor)
        self.job_class_manager = JobClassManager(self.qconf_executor)
        self.cluster_configuration_manager = ClusterConfigurationManager(self.qconf_executor)
        self.complex_configuration_manager = ComplexConfigurationManager(self.qconf_executor)
        self.resource_quota_set_manager = ResourceQuotaSetManager(self.qconf_executor)
        self.share_tree_manager = ShareTreeManager(self.qconf_executor)

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
            except QconfException as ex:
                raise
            except Exception as ex:
                raise QconfException(exception=ex)

        return decorator(wrapped_call, func)

    # Make sure only qconf exceptions are raised
    # Use two decorators to keep signature for documentation
    def api_call(*dargs, **dkwargs):
        def internal_call(func):
            @wraps(func)
            def wrapped_call(func, *args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    return result
                except QconfException as ex:
                    raise
                except Exception as ex:
                    raise QconfException(exception=ex)

            return decorator(wrapped_call, func)

        if len(dargs) == 1 and callable(dargs[0]):
            return internal_call(dargs[0])
        else:
            return internal_call

    def get_uge_version(self):
        """ Get version of UGE qmaster that API is connected to.

        :returns: UGE version string.

        :raises QconfException: in case of any errors.
        """
        return self.qconf_executor.get_uge_version()

    def generate_object(self, json_string, target_uge_version=None):
        """ Use specified JSON string to generate object for the target UGE version.
 
        :param json_string: input object's JSON string representation 
        :type json_string: str

        :param target_uge_version: target UGE version
        :type json_string: str

        :returns: Generated Qconf object.

        :raises QconfException: in case of any errors.
        """
        return QconfObjectFactory.generate_object(json_string, target_uge_version)

    #
    # ClusterQueue methods
    #

    @api_call
    def generate_queue(self, name=None, data=None, metadata=None,
                       json_string=None, uge_version=None,
                       add_required_data=True):
        """ Generate UGE cluster queue object.

        :param name: Cluster queue name; if provided, it will override queue name in the data dictionary, or in the json string.
        :type name: str

        :param data: Queue data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Queue metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the queue object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which cluster queue object should be generated. By default, generated queue object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated ClusterQueue object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_q = api.generate_queue(name='new.q')
        >>> new_q
        <uge.objects.cluster_queue_v1_0.ClusterQueue object at 0xf131d0>
        >>> new_q.data['qname']
        'new.q'
        >>> new_q.data['slots']
        1
        """
        return self.cluster_queue_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_queue(self, pycl_object=None, name=None, data=None,
                  metadata=None, json_string=None):
        """ Add UGE cluster queue. Default values for any missing required data keys will be added to queue configuration.

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

        :returns: Newly added ClusterQueue object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ClusterQueue, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify cluster queue name.
        :raises ObjectAlreadyExists: in case cluster queue object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the cluster queue data does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_q = api.add_queue(name='new.q', data={'slots' : 3})
        >>> new_q
        <uge.objects.cluster_queue_v1_0.ClusterQueue object at 0x7fc32e14ef50>
        >>> new_q.data['slots']
        3
        """
        return self.cluster_queue_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def add_queues(self, queue_list):
        """ Adds all UGE queues in queue_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_queues(queue_list)
        """
        return self.cluster_queue_manager.add_objects(queue_list)

    @api_call
    def add_queues_from_dir(self, dirname):
        """ Adds all UGE queues from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_queues_from_dir('/tmp/queue_test')
        """
        return self.cluster_queue_manager.add_objects_from_dir(dirname)

    @api_call
    def modify_queue(self, pycl_object=None, name=None, data=None,
                     metadata=None, json_string=None):
        """ Modify UGE cluster queue object.

        :param pycl_object: Cluster queue object to be modified.
        :type pycl_object: ClusterQueue

        :param name: Cluster queue name; if provided, it will override queue name in the provided cluster queue object, data dictionary, or in the json string.
        :type name: str

        :param data: Queue data dictionary; if provided, dictionary values will override corresponding values from the cluster queue object, or from the json string.
        :type data: dict

        :param metadata: Queue metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the queue object to be modified.
        :type json_string: str

        :returns: Modified ClusterQueue object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ClusterQueue, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify cluster queue name.
        :raises ObjectNotFound: in case cluster queue object with a given name does not exist, or an object contained in the cluster queue data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> all_q = api.modify_queue(name='all.q', data={'load_thresholds' : 'np_load_avg=2.0'})
        >>> all_q.data['load_thresholds']
        'np_load_avg=2.0'
        """
        return self.cluster_queue_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_queues(self, queue_list):
        """ Modifies all UGE queues in queue_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_queues(queue_list)
        """
        return self.cluster_queue_manager.modify_objects(queue_list)

    @api_call
    def modify_queues_from_dir(self, dirname):
        """ Modifies all UGE queues from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_queues_from_dir('/tmp/queue_test')
        """
        return self.cluster_queue_manager.modify_objects_from_dir(dirname)

    @api_call
    def get_queue(self, name):
        """ Retrieve UGE queue configuration.

        :param name: Cluster queue name.
        :type name: str

        :returns: ClusterQueue object.

        :raises ObjectNotFound: in case cluster queue object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> all_q = api.get_queue('all.q')
        >>> all_q.data['load_thresholds']
        'np_load_avg=2.0'
        """
        return self.cluster_queue_manager.get_object(name)

    @api_call
    def get_queues(self):
        """ Retrieve all UGE queues details.

        :returns: array of queue dict objects.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> cal_queue_list = api.get_queues()

        """
        return self.cluster_queue_manager.get_objects()

    @api_call
    def delete_queue(self, name):
        """ Delete UGE queue configuration.

        :param name: Cluster queue name.
        :type name: str

        :raises ObjectNotFound: in case cluster queue object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_queue('new.q')
        """
        return self.cluster_queue_manager.delete_object(name)

    @api_call
    def delete_queues(self, queue_list):
        """ Deletes all UGE queue in queue_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_queues(queue_list)
        """
        return self.cluster_queue_manager.delete_object_list(queue_list)

    @api_call
    def delete_queues_from_dir(self, dirname):
        """ Delete UGE queues from files in dir.

        :param dirname: Directory containing UGE queue object files.
        :type dirname: string

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_queues_from_dir('/tmp/queue_test')
        """
        return self.cluster_queue_manager.delete_objects_from_dir(dirname)

    @api_call
    def list_queues(self):
        """ List UGE queue names.

        :returns: QconfNameList object containing cluster queue names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> q_list = api.list_queues()
        >>> q_list
        ['all.q']
        >>> q_list.__class__.__name__
        'QconfNameList'
        """
        return self.cluster_queue_manager.list_objects()

    @api_call
    def mk_queues_dir(self, dirname):
        """ Make a temporary directory to write queue data.

        >>> api.mk_queues_dir('/tmp/queues_test')
        """
        self.cluster_queue_manager.mk_object_dir(dirname)

    @api_call
    def rm_queues_dir(self, dirname):
        """ Remove temporary queue directory.

        >>> api.rm_queues_dir('/tmp/queues_test')
        """
        self.cluster_queue_manager.rm_object_dir(dirname)

    @api_call
    def write_queues(self, queue_list, dirname):
        """ Write each queue in queue_list to a seperate file in dir.

        >>> api.write_queues(queue_list, '/tmp/queues_test')
        """
        self.cluster_queue_manager.write_objects(queue_list, dirname)

    #
    # ParallelEnvironment methods
    #

    @api_call
    def generate_pe(self, name=None, data=None, metadata=None,
                    json_string=None, uge_version=None,
                    add_required_data=True):
        """ Generate UGE parallel environment object.

        :param name: Parallel environment name; if provided, it will override PE name in the data dictionary, or in the json string.
        :type name: str

        :param data: Parallel environment data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Parallel environment metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the PE object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which parallel environment object should be generated. By default, generated PE object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated ParallelEnvironment object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> pe = api.generate_pe(name='pe1')
        >>> pe
        <uge.objects.parallel_environment_v1_0.ParallelEnvironment object at 0x7f990c3ede90>
        >>> pe.data['pe_name']
        'pe1'
        >>> pe.data['urgency_slots']
        'min'
        """
        return self.parallel_environment_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_pe(self, pycl_object=None, name=None, data=None,
               metadata=None, json_string=None):
        """ Add UGE parallel environment. Default values for any missing required data keys will be added to PE configuration.

        :param pycl_object: Parallel environment object to be added.
        :type pycl_object: ParallelEnvironment

        :param name: Parallel environment name; if provided, it will override PE name in the provided parallel environment object, data dictionary, or in the json string.
        :type name: str

        :param data: Parallel environment data dictionary; if provided, dictionary values will override corresponding values from the parallel environment object, or from the json string.
        :type data: dict

        :param metadata: Parallel environment metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the PE object to be added.
        :type json_string: str

        :returns: Newly added ParallelEnvironment object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ParallelEnvironment, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify parallel environment name.
        :raises ObjectAlreadyExists: in case parallel environment object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the parallel environment data does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_pe = api.add_pe(name='new_pe', data={'slots' : 10})
        >>> new_pe.data
        {'allocation_rule': '$pe_slots',..., 'slots': 10,...}
        """
        return self.parallel_environment_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def add_pes(self, pe_list):
        """ Adds all UGE parallel environment objects in pe_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_pes(pe_list)
        """
        return self.parallel_environment_manager.add_objects(pe_list)

    @api_call
    def add_pes_from_dir(self, dirname):
        """ Adds all UGE parallel environment objects from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_pes_from_dir('/tmp/pe_test')
        """
        return self.parallel_environment_manager.add_objects_from_dir(dirname)

    @api_call
    def modify_pe(self, pycl_object=None, name=None, data=None,
                  metadata=None, json_string=None):
        """ Modify UGE parallel environment object.

        :param pycl_object: Parallel environment object to be modified.
        :type pycl_object: ParallelEnvironment

        :param name: Parallel environment name; if provided, it will override PE name in the provided parallel environment object, data dictionary, or in the json string.
        :type name: str

        :param data: Parallel environment data dictionary; if provided, dictionary values will override corresponding values from the parallel environment object, or from the json string.
        :type data: dict

        :param metadata: Parallel environment metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the PE object to be modified.
        :type json_string: str

        :returns: Modified ParallelEnvironment object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ParallelEnvironment, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify parallel environment name.
        :raises ObjectNotFound: in case parallel environment object with a given name does not exist, or an object contained in the parallel environment data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_pe = api.get_pe('new_pe')
        >>> new_pe.data['accounting_summary']
        False
        >>> new_pe.data['accounting_summary'] = True
        >>> new_pe = api.modify_pe(pycl_object=new_pe)
        >>> new_pe.data['accounting_summary']
        True
        """
        return self.parallel_environment_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_pes(self, pe_list):
        """ Modify all UGE parallel environment objects in pe_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_pes(pe_list)
        """
        return self.parallel_environment_manager.modify_objects(pe_list)

    @api_call
    def modify_pes_from_dir(self, dirname):
        """ Modify all UGE parallel environment objects from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_pes_from_dir('/tmp/pe_test')
        """
        return self.parallel_environment_manager.modify_objects_from_dir(dirname)

    @api_call
    def get_pe(self, name):
        """ Retrieve UGE PE configuration.

        :param name: Parallel environment name.
        :type name: str

        :returns: ParallelEnvironment object.

        :raises ObjectNotFound: in case parallel environment object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_pe = api.get_pe('new_pe')
        >>> new_pe.data
        {'allocation_rule': '$pe_slots', 'used_slots': '0', 'user_lists': None, 'pe_name': 'new_pe',...}
        """
        return self.parallel_environment_manager.get_object(name)

    @api_call
    def get_pes(self):
        """ Retrieve all UGE parallel environment objects details.

        :returns: array of parallel environment dict objects.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> pe_dict_list = api.get_pes()
        """
        return self.parallel_environment_manager.get_objects()

    @api_call
    def delete_pe(self, name):
        """ Delete UGE pe configuration.

        :param name: Parallel environment name.
        :type name: str

        :raises ObjectNotFound: in case parallel environment object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_pe('new_pe')
        """
        return self.parallel_environment_manager.delete_object(name)

    @api_call
    def delete_pes(self, pe_list):
        """ Deletes all UGE parallel environments in pe_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_pes(pe_list)
        """
        return self.parallel_environment_manager.delete_object_list(pe_list)

    @api_call
    def delete_pes_from_dir(self, dirname):
        """ Delete all UGE parallel environments from files in dir.

        :param dirname: Directory containing UGE parallel environment object files.
        :type dirname: string

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_pes_from_dir('/tmp/pe_test')
        """
        return self.parallel_environment_manager.delete_objects_from_dir(dirname)

    @api_call
    def list_pes(self):
        """ List UGE PE names.

        :returns: QconfNameList object containing parallel environment names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> pe_list = api.list_pes()
        >>> pe_list
        ['pe1']
        """
        return self.parallel_environment_manager.list_objects()

    @api_call
    def mk_pes_dir(self, dirname):
        """ Make a temporary directory to write UGE parallel environment data.

        >>> api.mk_pes_dir('/tmp/pes_test')
        """
        self.parallel_environment_manager.mk_object_dir(dirname)

    @api_call
    def rm_pes_dir(self, dirname):
        """ Remove temporary UGE parallel environments directory.

        >>> api.rm_pes_dir('/tmp/pes_test')
        """
        self.parallel_environment_manager.rm_object_dir(dirname)

    @api_call
    def write_pes(self, pe_list, dirname):
        """ Write each UGE parallel environment in pe_list to a seperate file in dir.

        >>> api.write_pes(pe_list, '/tmp/pes_test')
        """
        self.parallel_environment_manager.write_objects(pe_list, dirname)

    #
    # ExecutionHost methods
    #

    @api_call
    def generate_ehost(self, name=None, data=None, metadata=None,
                       json_string=None, uge_version=None,
                       add_required_data=True):
        """ Generate UGE execution host object.

        :param name: Execution host name; if provided, it will override host name in the data dictionary, or in the json string.
        :type name: str

        :param data: Host data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Host metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the host object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which execution host object should be generated. By default, generated host object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated ExecutionHost object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_ehost = api.generate_ehost(name='newhost')
        >>> new_ehost
        <uge.objects.execution_host_v1_0.ExecutionHost object at 0xa54e90>
        >>> new_ehost.data['hostname']
        'newhost'
        >>> print new_ehost.data['user_lists']
        None
        """
        return self.execution_host_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_ehost(self, pycl_object=None, name=None, data=None,
                  metadata=None, json_string=None):
        """ Add UGE execution host. Default values for any missing required data keys will be added to host configuration.

        :param pycl_object: Execution host object to be added.
        :type pycl_object: ExecutionHost 

        :param name: Execution host name; if provided, it will override host name in the provided execution host object, data dictionary, or in the json string.
        :type name: str

        :param data: Host data dictionary; if provided, dictionary values will override corresponding values from the execution host object, or from the json string.
        :type data: dict

        :param metadata: Host metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the host object to be added.
        :type json_string: str

        :returns: Newly added ExecutionHost object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ExecutionHost, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify execution host name.
        :raises ObjectAlreadyExists: in case execution host object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the execution host data does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_host = api.add_ehost(name='univa2', data={'complex_values' : 'slots=10'})
        >>> new_host
        <uge.objects.execution_host_v1_0.ExecutionHost object at 0xa54ed0>
        >>> new_host.data['complex_values']
        'slots=10'
        """
        return self.execution_host_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def add_ehosts(self, ehost_list):
        """ Adds all UGE execution hosts from ehost_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_ehosts(ehost_list)
        """
        return self.execution_host_manager.add_objects(ehost_list)

    @api_call
    def modify_ehost(self, pycl_object=None, name=None, data=None,
                     metadata=None, json_string=None):
        """ Modify UGE execution host object.

        :param pycl_object: Execution host object to be modified.
        :type pycl_object: ExecutionHost 

        :param name: Execution host name; if provided, it will override host name in the provided execution host object, data dictionary, or in the json string.
        :type name: str

        :param data: Host data dictionary; if provided, dictionary values will override corresponding values from the execution host object, or from the json string.
        :type data: dict

        :param metadata: Host metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the host object to be modified.
        :type json_string: str

        :returns: Modified ExecutionHost object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ExecutionHost, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify execution host name.
        :raises ObjectNotFound: in case execution host object with a given name does not exist, or an object contained in the execution host data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> host = api.modify_ehost(name='univa2',data={'complex_values' : 'slots=100'})
        >>> host.data['complex_values']
        'slots=100'
        """
        return self.execution_host_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_ehosts(self, ehost_list):
        """ Modifies all UGE execution hosts from ehost_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_ehosts(ehost_list)
        """
        return self.execution_host_manager.modify_objects(ehost_list)

    @api_call
    def get_ehost(self, name):
        """ Retrieve UGE execution host configuration.

        :param name: Execution host name.
        :type name: str

        :returns: ExecutionHost object.

        :raises ObjectNotFound: in case execution host object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> host = api.get_ehost('univa')
        >>> host.data['hostname']
        'univa.skaisoft.net'
        >>> host.data['complex_values']
        'slots=10'
        >>> host.data['load_values']
        ['arch=lx-amd64', 'cpu=22.500000', 'load_avg=0.450000',...] 
        """
        return self.execution_host_manager.get_object(name)

    @api_call
    def get_ehosts(self):
        """ Retrieve all UGE execution hosts configuration details.

        :returns: array of ExecutionHost dict objects.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> ehost_dict_list = api.get_ehosts()
        """
        return self.execution_host_manager.get_objects()

    @api_call
    def delete_ehost(self, name):
        """ Delete UGE execution host.

        :param name: Execution host name.
        :type name: str

        :raises ObjectNotFound: in case execution host object with a given name does not exist.
        :raises InvalidRequest: if execution host is still referenced in other objects (e.g., hostlists).
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_ehost('univa2')
        """
        return self.execution_host_manager.delete_object(name)

    @api_call
    def delete_ehosts(self, name_list):
        """ Delete UGE execution host.

        :param name: Execution host name list.
        :type name: string list

        :raises ObjectNotFound: in case execution host object with a given name does not exist.
        :raises InvalidRequest: if execution host is still referenced in other objects (e.g., hostlists).
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_ehosts(['univa1', 'univa2'])
        """
        return self.execution_host_manager.delete_objects(name_list)

    @api_call
    def list_ehosts(self):
        """ List UGE execution host names.

        :returns: QconfNameList object containing execution host names (including the 'global' host).

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> host_list = api.list_ehosts()
        >>> host_list
        ['univa.skaisoft.net', 'global']
        >>> host_list.__class__.__name__
        'QconfNameList'
        """
        return self.execution_host_manager.list_objects()

    @api_call
    def mk_ehosts_dir(self, dirname):
        """ Make a temporary directory to write ehost data.

        >>> api.mk_ehosts_dir('/tmp/ehosts_test')
        """
        self.execution_host_manager.mk_object_dir(dirname)

    @api_call
    def rm_ehosts_dir(self, dirname):
        """ Remove temporary ehosts directory.

        >>> api.rm_ehosts_dir('/tmp/ehosts_test')
        """
        self.execution_host_manager.rm_object_dir(dirname)

    @api_call
    def write_ehosts(self, ehost_list, dirname):
        """ Write each ehost in ehost_list to a seperate file in dir.

        >>> api.write_ehosts(ehost_list, '/tmp/ehosts_test')
        """
        self.execution_host_manager.write_objects(ehost_list, dirname)

    @api_call
    def add_ehosts_from_dir(self, dirname):
        """ Adds all UGE execution hosts from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_ehosts_from_dir('/tmp/ehosts_test')
        """
        return self.execution_host_manager.add_objects_from_dir(dirname)

    @api_call
    def modify_ehosts_from_dir(self, dirname):
        """ Modifies all UGE execution hosts from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_ehosts_from_dir('/tmp/ehosts_test')
        """
        return self.execution_host_manager.modify_objects_from_dir(dirname)

    #
    # HostGroup methods
    #

    @api_call
    def generate_hgrp(self, name=None, data=None, metadata=None,
                      json_string=None, uge_version=None,
                      add_required_data=True):
        """ Generate UGE host group object.

        :param name: Host group name; if provided, it will override host name in the data dictionary, or in the json string.
        :type name: str

        :param data: Host data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Host metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the host object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which host group object should be generated. By default, generated host object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated HostGroup object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_hgrp = api.generate_hgrp(name='@myhosts')
        >>> new_hgrp
        <uge.objects.host_group_v1_0.HostGroup object at 0x1ee5110>
        >>> new_hgrp.data
        {'hostlist': None, 'group_name': '@myhosts'}
        """
        return self.host_group_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_hgrp(self, pycl_object=None, name=None, data=None,
                 metadata=None, json_string=None):
        """ Add UGE host group. Default values for any missing required data keys will be added to host configuration.

        :param pycl_object: Host group object to be added.
        :type pycl_object: HostGroup 

        :param name: Host group name; if provided, it will override name in the provided host group object, data dictionary, or in the json string.
        :type name: str

        :param data: Host group data dictionary; if provided, dictionary values will override corresponding values from the host group object, or from the json string.
        :type data: dict

        :param metadata: Host group metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the host group object to be added.
        :type json_string: str

        :returns: Newly added HostGroup object.

        :raises InvalidArgument: if provided PYCL object is not an instance of HostGroup, or data is not a dictionary, or if json_string does not represent a valid JSON object. 
        :raises InvalidRequest: if provided arguments do not specify host group name.
        :raises ObjectAlreadyExists: in case host group object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the host group data does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_hgrp = api.add_hgrp(name='@myhosts', data={'hostlist' : ['univa', 'univa2']})
        >>> print new_hgrp.data
        {'hostlist': ['univa', 'univa2'], 'group_name': '@myhosts3'}
        """
        return self.host_group_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def add_hgrps(self, hgrp_list):
        """ Adds all UGE host groups in hgrp_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_hgrps(hgrp_list)
        """
        return self.host_group_manager.add_objects(hgrp_list)

    @api_call
    def add_hgrps_from_dir(self, dirname):
        """ Adds all UGE host groups from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_hgrps_from_dir('/tmp/hgrp_test')
        """
        return self.host_group_manager.add_objects_from_dir(dirname)

    @api_call
    def modify_hgrp(self, pycl_object=None, name=None, data=None,
                    metadata=None, json_string=None):
        """ Modify UGE host group object.

        :param pycl_object: Host group object to be modified.
        :type pycl_object: HostGroup

        :param name: Host group name; if provided, it will override host name in the provided host group object, data dictionary, or in the json string.
        :type name: str

        :param data: Host group data dictionary; if provided, dictionary values will override corresponding values from the host group object, or from the json string.
        :type data: dict

        :param metadata: Host group metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the host object to be modified.
        :type json_string: str

        :returns: Modified HostGroup object.

        :raises InvalidArgument: if provided PYCL object is not an instance of HostGroup, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify host group name.
        :raises ObjectNotFound: in case host group object with a given name does not exist, or an object contained in the host group data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> hgrp = api.modify_hgrp(name='@myhosts',data={'hostlist' : 'univa univa2 univa3'})
        >>> print hgrp.to_json()
        {"object_class": "HostGroup", ..., "data": {"hostlist": ["univa", "univa2", "univa3"], "group_name": "@myhosts"}}
        """
        return self.host_group_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_hgrps(self, hgrp_list):
        """ Modifies all UGE host groups in hgrp_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_hgrps(hgrp_list)
        """
        return self.host_group_manager.modify_objects(hgrp_list)

    @api_call
    def modify_hgrps_from_dir(self, dirname):
        """ Modifies all UGE host groups from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_hgrps_from_dir('/tmp/hgrp_test')
        """
        return self.host_group_manager.modify_objects_from_dir(dirname)

    @api_call
    def get_hgrp(self, name):
        """ Retrieve UGE host group configuration.

        :param name: Host group name.
        :type name: str

        :returns: HostGroup object.

        :raises ObjectNotFound: in case host group object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> hgrp = api.get_hgrp('@myhosts')
        >>> hgrp.data['hostlist']
        ['univa.skaisoft.net', 'univa2.skaisoft.net', 'univa3.skaisoft.net']
        """
        return self.host_group_manager.get_object(name)

    @api_call
    def get_hgrps(self):
        """ Retrieve all UGE host groups details.

        :returns: array of host group objects.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> hgrp_dict_list = api.get_hgrps()

        """
        return self.host_group_manager.get_objects()

    @api_call
    def delete_hgrp(self, name):
        """ Delete UGE host group.

        :param name: Host group name.
        :type name: str

        :raises ObjectNotFound: in case host group object with a given name does not exist.
        :raises InvalidRequest: if host group is still referenced in other objects (e.g., hostlists).
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_hgrp('@myhosts')
        """
        return self.host_group_manager.delete_object(name)

    @api_call
    def delete_hgrps(self, hgrp_list):
        """ Deletes all UGE host groups in hgrp_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_hgrps(hgrp_list)
        """
        return self.host_group_manager.delete_object_list(hgrp_list)

    @api_call
    def delete_hgrps_from_dir(self, dirname):
        """ Delete UGE host groups from files in dir.

        :param dirname: Directory containing UGE host group object files.
        :type dirname: string

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_hgrps_from_dir('/tmp/hgrp_test')
        """
        return self.host_group_manager.delete_objects_from_dir(dirname)

    @api_call
    def list_hgrps(self):
        """ List UGE host group names.

        :returns: QconfNameList object containing host group names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> hgrp_list = api.list_hgrps()
        >>> hgrp_list
        ['@allhosts', '@myhosts']
        >>> hgrp_list.__class__.__name__
        'QconfNameList'
        """
        return self.host_group_manager.list_objects()

    @api_call
    def mk_hgrps_dir(self, dirname):
        """ Make a temporary directory to write host group data.

        >>> api.mk_hgrps_dir('/tmp/hgrps_test')
        """
        self.host_group_manager.mk_object_dir(dirname)

    @api_call
    def rm_hgrps_dir(self, dirname):
        """ Remove temporary host group directory.

        >>> api.rm_hgrps_dir('/tmp/hgrps_test')
        """
        self.host_group_manager.rm_object_dir(dirname)

    @api_call
    def write_hgrps(self, hgrp_list, dirname):
        """ Write each host group in hgrp_list to a seperate file in dir.

        >>> api.write_hgrps(hgrp_list, '/tmp/hgrps_test')
        """
        self.host_group_manager.write_objects(hgrp_list, dirname)

    #
    # SubmitHost methods
    #

    @api_call
    def add_shosts(self, host_names):
        """ Add UGE submit hosts.

        :param name: List of host names to be added.
        :type name: list

        :returns: QconfNameList object containing all submit host names after addition.

        :raises ObjectAlreadyExists: in case some of the names provided are already designated submit hosts.
        :raises ObjectNotFound: in case some of the host names provided cannot be resolved.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> host_list = api.add_shosts(['univa3', 'univa4', 'univa5'])
        >>> print host_list.data
        ['univa.skaisoft.net',..., 'univa4.skaisoft.net', 'univa5.skaisoft.net']
        """
        return self.submit_host_manager.add_names(host_names)

    @api_call
    def delete_shosts(self, host_names):
        """ Delete UGE submit hosts.

        :param name: List of host names to be deleted.
        :type name: list

        :returns: QconfNameList object containing all submit host names after deletion.

        :raises ObjectNotFound: in case some of the host names provided are not designated as submit hosts.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> host_list = api.delete_shosts(['univa3', 'univa4', 'univa5'])
        >>> print host_list.data
        ['univa.skaisoft.net', 'univa2.skaisoft.net']
        """
        return self.submit_host_manager.delete_names(host_names)

    @api_call
    def list_shosts(self):
        """ List UGE submit host names.

        :returns: QconfNameList object containing submit host names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> host_list = api.list_shosts()
        >>> print host_list
        {"data": ["univa.skaisoft.net", ...],..., "object_class": "QconfNameList", "description": "list of submission hosts"}
        """
        return self.submit_host_manager.list_names()

    #
    # AdminHost methods
    #

    @api_call
    def add_ahosts(self, host_names):
        """ Add UGE admin hosts.

        :param name: List of host names to be added.
        :type name: list

        :returns: QconfNameList object containing all admin host names after addition.

        :raises ObjectAlreadyExists: in case some of the names provided are already designated admin hosts.
        :raises ObjectNotFound: in case some of the host names provided cannot be resolved.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> host_list = api.add_ahosts(['univa3', 'univa4', 'univa5'])
        >>> print host_list.data
        ['univa.skaisoft.net',..., 'univa4.skaisoft.net', 'univa5.skaisoft.net']
        """
        return self.admin_host_manager.add_names(host_names)

    @api_call
    def delete_ahosts(self, host_names):
        """ Delete UGE admin hosts.

        :param name: List of host names to be deleted.
        :type name: list

        :returns: QconfNameList object containing all admin host names after deletion.

        :raises ObjectNotFound: in case some of the host names provided are not designated as admin hosts.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> host_list = api.delete_ahosts(['univa3', 'univa4', 'univa5'])
        >>> print host_list.data
        ['univa.skaisoft.net', 'univa2.skaisoft.net']
        """
        return self.admin_host_manager.delete_names(host_names)

    @api_call
    def list_ahosts(self):
        """ List UGE admin host names.

        :returns: QconfNameList object containing admin host names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> host_list = api.list_ahosts()
        >>> print host_list
        {"data": ["univa.skaisoft.net", ...],..., "object_class": "QconfNameList", "description": "list of administrative hosts"}
        """
        return self.admin_host_manager.list_names()

    #
    # Operator methods
    #

    @api_call
    def add_operators(self, operator_names):
        """ Add UGE operators.

        :param name: List of operator names to be added.
        :type name: list

        :returns: QconfNameList object containing all operator names after addition.

        :raises ObjectAlreadyExists: in case some of the names provided are already designated operators.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> operator_list = api.add_operators(['bbryce'])
        >>> print operator_list.data
        ['uge', 'bbryce']
        """
        return self.operator_manager.add_names(operator_names)

    @api_call
    def delete_operators(self, operator_names):
        """ Delete UGE operators.

        :param name: List of operator names to be deleted.
        :type name: list

        :returns: QconfNameList object containing all operator names after deletion.

        :raises ObjectNotFound: in case some of the operator names provided are not designated as operators.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> operator_list = api.delete_operators(['bbryce'])
        >>> print operator_list.data
        ['uge']
        """
        return self.operator_manager.delete_names(operator_names)

    @api_call
    def list_operators(self):
        """ List UGE operator names.

        :returns: QconfNameList object containing operator names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> operator_list = api.list_operators()
        >>> print operator_list
        {"data": ["uge", ...],..., "object_class": "QconfNameList", "description": "list of operators"}
        """
        return self.operator_manager.list_names()

    #
    # Manager methods
    #

    @api_call
    def add_managers(self, manager_names):
        """ Add UGE managers.

        :param name: List of manager names to be added.
        :type name: list

        :returns: QconfNameList object containing all manager names after addition.

        :raises ObjectAlreadyExists: in case some of the names provided are already designated managers.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> manager_list = api.add_managers(['aschwierskott'])
        >>> print manager_list.data
        ['uge', 'aschwierskott']
        """
        return self.manager_manager.add_names(manager_names)

    @api_call
    def delete_managers(self, manager_names):
        """ Delete UGE managers.

        :param name: List of manager names to be deleted.
        :type name: list

        :returns: QconfNameList object containing all manager names after deletion.

        :raises ObjectNotFound: in case some of the manager names provided are not designated as managers.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> manager_list = api.delete_managers(['aschwierskott'])
        >>> print manager_list.data
        ['uge']
        """
        return self.manager_manager.delete_names(manager_names)

    @api_call
    def list_managers(self):
        """ List UGE manager names.

        :returns: QconfNameList object containing manager names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> manager_list = api.list_managers()
        >>> print manager_list
        {"data": ["uge", ...],..., "object_class": "QconfNameList", "description": "list of managers"}
        """
        return self.manager_manager.list_names()

    #
    # User methods
    #

    @api_call
    def generate_user(self, name=None, data=None, metadata=None,
                      json_string=None, uge_version=None,
                      add_required_data=True):
        """ Generate UGE user object.

        :param name: User name; if provided, it will override user name in the data dictionary, or in the json string.
        :type name: str

        :param data: User data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: User metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the user object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which user object should be generated. By default, generated user object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated User object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> user = api.generate_user(name='bbryce')
        >>> print user.to_json()
        {"data": {"oticket": 0,..., "name": "bbryce", "fshare": 0}, "object_version": "1.0", "object_class": "User"}
        """
        return self.user_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_user(self, pycl_object=None, name=None, data=None,
                 metadata=None, json_string=None):
        """ Add UGE user. Default values for any missing required data keys will be added to user configuration.

        :param pycl_object: User object to be added.
        :type pycl_object: User

        :param name: User name; if provided, it will override user name in the provided user object, data dictionary, or in the json string.
        :type name: str

        :param data: User data dictionary; if provided, dictionary values will override corresponding values from the user object, or from the json string.
        :type data: dict

        :param metadata: User metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the user object to be added.
        :type json_string: str

        :returns: Newly added User object.

        :raises InvalidArgument: if provided PYCL object is not an instance of an User object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify user name.
        :raises ObjectAlreadyExists: in case user object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the user data does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> user = api.add_user(name='bbryce')
        >>> print user.to_json()
        {"data": {"oticket": 0,..., "name": "bbryce", "fshare": 0},..., "created_by": "sinisa@univa.skaisoft.net"}
        """
        return self.user_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def add_users(self, user_list):
        """ Adds all UGE users in user_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_users(user_list)
        """
        return self.user_manager.add_objects(user_list)

    @api_call
    def add_users_from_dir(self, dirname):
        """ Adds all UGE users from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_users_from_dir('/tmp/user_test')
        """
        return self.user_manager.add_objects_from_dir(dirname)

    @api_call
    def modify_user(self, pycl_object=None, name=None, data=None,
                    metadata=None, json_string=None):
        """ Modify UGE user object.

        :param pycl_object: User object to be modified.
        :type pycl_object: User

        :param name: User name; if provided, it will override user name in the provided user object, data dictionary, or in the json string.
        :type name: str

        :param data: User data dictionary; if provided, dictionary values will override corresponding values from the user object, or from the json string.
        :type data: dict

        :param metadata: User metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the user object to be modified.
        :type json_string: str

        :returns: Modified User object.

        :raises InvalidArgument: if provided PYCL object is not an instance of User, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify user name.
        :raises ObjectNotFound: in case user object with a given name does not exist, or an object contained in the user data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> user = api.modify_user(name='bbryce', data={'oticket' : 100})
        >>> print user.to_json()
        {"modified_on": "2016-06-17T22:45:46.428816",..., "data": {"name": "bbryce", "oticket": 100,...}}
        """
        return self.user_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_users(self, user_list):
        """ Modifies all UGE users in user_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_users(user_list)
        """
        return self.user_manager.modify_objects(user_list)

    @api_call
    def modify_users_from_dir(self, dirname):
        """ Modifies all UGE users from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_users_from_dir('/tmp/user_test')
        """
        return self.user_manager.modify_objects_from_dir(dirname)

    @api_call
    def get_user(self, name):
        """ Retrieve UGE user configuration.

        :param name: User name.
        :type name: str

        :returns: User object.

        :raises ObjectNotFound: in case user object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> user = api.get_user('bbryce')
        >>> print user.data['oticket']
        100
        """
        return self.user_manager.get_object(name)

    @api_call
    def get_users(self):
        """ Retrieve all UGE user details.

        :returns: array of user dict objects.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> user_dict_list = api.get_users()

        """
        return self.user_manager.get_objects()

    @api_call
    def delete_user(self, name):
        """ Delete UGE user.

        :param name: User name.
        :type name: str

        :raises ObjectNotFound: in case user object with a given name does not exist.
        :raises InvalidRequest: if user is still referenced in other objects.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_user('testuser')
        """
        return self.user_manager.delete_object(name)

    @api_call
    def delete_users(self, user_list):
        """ Deletes all UGE users in user_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_users(user_list)
        """
        return self.user_manager.delete_object_list(user_list)

    @api_call
    def delete_users_from_dir(self, dirname):
        """ Delete UGE users from files in dir.

        :param dirname: Directory containing UGE user object files.
        :type dirname: string

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_users_from_dir('/tmp/user_test')
        """
        return self.user_manager.delete_objects_from_dir(dirname)

    @api_call
    def list_users(self):
        """ List UGE user names.

        :returns: QconfNameList object containing user names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> user_list = api.list_users()
        >>> user_list
        ['bbryce']
        """
        return self.user_manager.list_objects()

    @api_call
    def mk_users_dir(self, dirname):
        """ Make a temporary directory to write user data.

        >>> api.mk_users_dir('/tmp/users_test')
        """
        self.user_manager.mk_object_dir(dirname)

    @api_call
    def rm_users_dir(self, dirname):
        """ Remove temporary user directory.

        >>> api.rm_users_dir('/tmp/users_test')
        """
        self.user_manager.rm_object_dir(dirname)

    @api_call
    def write_users(self, user_list, dirname):
        """ Write each user in user_list to a seperate file in dir.

        >>> api.write_users(user_list, '/tmp/users_test')
        """
        self.user_manager.write_objects(user_list, dirname)

    #
    # Project methods
    #

    @api_call
    def generate_prj(self, name=None, data=None, metadata=None,
                     json_string=None, uge_version=None,
                     add_required_data=True):
        """ Generate UGE project object.

        :param name: Project name; if provided, it will override project name in the data dictionary, or in the json string.
        :type name: str

        :param data: Project data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Project metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the project object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which project object should be generated. By default, generated project object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated Project object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> project = api.generate_prj(name='project1')
        >>> print project.to_json()
        {"data": {"oticket": 0,..., "name": "project1", "fshare": 0}, "object_version": "1.0", "object_class": "Project"}
        """
        return self.project_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_prj(self, pycl_object=None, name=None, data=None,
                metadata=None, json_string=None):
        """ Add UGE project. Default values for any missing required data keys will be added to project configuration.

        :param pycl_object: Project object to be added.
        :type pycl_object: Project 

        :param name: Project name; if provided, it will override project name in the provided project object, data dictionary, or in the json string.
        :type name: str

        :param data: Project data dictionary; if provided, dictionary values will override corresponding values from the project object, or from the json string.
        :type data: dict

        :param metadata: Project metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the project object to be added.
        :type json_string: str

        :returns: Newly added Project object.

        :raises InvalidArgument: if provided PYCL object is not an instance of an Project object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify project name.
        :raises ObjectAlreadyExists: in case project object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the project data does not exist.
        :raises AuthorizationError: if project is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> project = api.add_prj(name='project1')
        >>> print project.to_json()
        {"data": {"oticket": 0,..., "name": "project1", "fshare": 0},..., "created_by": "sinisa@univa.skaisoft.net"}
        """
        return self.project_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def add_prjs(self, prj_list):
        """ Adds all projects in prj_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_prjs(prj_list)
        """
        return self.project_manager.add_objects(prj_list)

    @api_call
    def modify_prj(self, pycl_object=None, name=None, data=None,
                   metadata=None, json_string=None):
        """ Modify UGE project object.

        :param pycl_object: Project object to be modified.
        :type pycl_object: Project 

        :param name: Project name; if provided, it will override project name in the provided project object, data dictionary, or in the json string.
        :type name: str

        :param data: Project data dictionary; if provided, dictionary values will override corresponding values from the project object, or from the json string.
        :type data: dict

        :param metadata: Project metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the project object to be modified.
        :type json_string: str

        :returns: Modified Project object.

        :raises InvalidArgument: if provided PYCL object is not an instance of Project, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify project name.
        :raises ObjectNotFound: in case project object with a given name does not exist, or an object contained in the project data cannot be found.
        :raises AuthorizationError: if project is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> project = api.modify_prj(name='project1', data={'oticket' : 100})
        >>> print project.to_json()
        {"modified_on": "2016-06-17T22:45:46.428816",..., "data": {"name": "project1", "oticket": 100,...}}
        """
        return self.project_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_prjs(self, prj_list):
        """ Modifies all projects in prj_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_prjs(prj_list)
        """
        return self.project_manager.modify_objects(prj_list)

    @api_call
    def get_prj(self, name):
        """ Retrieve UGE project configuration.

        :param name: Project name.
        :type name: str

        :returns: Project object.

        :raises ObjectNotFound: in case project object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> project = api.get_prj('project1')
        >>> print project.data['oticket']
        100
        """
        return self.project_manager.get_object(name)

    @api_call
    def get_prjs(self):
        """ Retrieve all UGE projects.

        :returns: array of project dict objects.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> prjs_list = api.get_prjs()
        """
        return self.project_manager.get_objects()

    @api_call
    def delete_prj(self, name):
        """ Delete UGE project.

        :param name: Project name.
        :type name: str

        :raises ObjectNotFound: in case project object with a given name does not exist.
        :raises InvalidRequest: if project is still referenced in other objects.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_prj('testproject')
        """
        return self.project_manager.delete_object(name)

    @api_call
    def delete_prjs(self, prjname_list):
        """ Delete UGE projects in prj_list.

        :param name: Project name list.
        :type name: string list

        :raises ObjectNotFound: in case project object with a given name does not exist.
        :raises InvalidRequest: if project is still referenced in other objects.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_prjs(['testproject1', 'testproject2'])
        """
        return self.project_manager.delete_objects(prjname_list)

    @api_call
    def list_prjs(self):
        """ List UGE project names.

        :returns: QconfNameList object containing project names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> project_list = api.list_prjs()
        >>> project_list
        ['project1']
        """
        return self.project_manager.list_objects()

    @api_call
    def mk_prjs_dir(self, dirname):
        """ Make a temporary directory to write project data.

        >>> api.mk_prjs_dir('/tmp/prjs_test')
        """
        self.project_manager.mk_object_dir(dirname)

    @api_call
    def rm_prjs_dir(self, dirname):
        """ Remove temporary projects directory.

        >>> api.rm_prjs_dir('/tmp/prjs_test')
        """
        self.project_manager.rm_object_dir(dirname)

    @api_call
    def write_prjs(self, prjs, dirname):
        """ Write each project in prjs to a seperate file in dir.

        >>> api.write_prjs(prjs, '/tmp/prjs_test')
        """
        self.project_manager.write_objects(prjs, dirname)

    @api_call
    def add_prjs_from_dir(self, dirname):
        """ Adds all projects from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_prjs('/tmp/prjs_test')
        """
        return self.project_manager.add_objects_from_dir(dirname)

    @api_call
    def modify_prjs_from_dir(self, dirname):
        """ Modify all projects from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_prjs_from_dir('/tmp/prjs_test')
        """
        return self.project_manager.modify_objects_from_dir(dirname)

    #
    # Calendar methods
    #

    @api_call
    def generate_cal(self, name=None, data=None, metadata=None,
                     json_string=None, uge_version=None,
                     add_required_data=True):
        """ Generate UGE calendar object.

        :param name: Calendar name; if provided, it will override calendar name in the data dictionary, or in the json string.
        :type name: str

        :param data: Calendar data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Calendar metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the calendar object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which calendar object should be generated. By default, generated calendar object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated Calendar object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> calendar = api.generate_cal(name='calendar1')
        >>> print calendar.to_json()
        {"data": {"week": null, "calendar_name": "calendar1", "year": null}, "object_version": "1.0", "object_class": "Calendar"}
        """
        return self.calendar_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_cal(self, pycl_object=None, name=None, data=None,
                metadata=None, json_string=None):
        """ Add UGE calendar. Default values for any missing required data keys will be added to calendar configuration.

        :param pycl_object: Calendar object to be added.
        :type pycl_object: Calendar

        :param name: Calendar name; if provided, it will override calendar name in the provided calendar object, data dictionary, or in the json string.
        :type name: str

        :param data: Calendar data dictionary; if provided, dictionary values will override corresponding values from the calendar object, or from the json string.
        :type data: dict

        :param metadata: Calendar metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the calendar object to be added.
        :type json_string: str

        :returns: Newly added Calendar object.

        :raises InvalidArgument: if provided PYCL object is not an instance of an Calendar object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify calendar name.
        :raises ObjectAlreadyExists: in case calendar object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the calendar data does not exist.
        :raises AuthorizationError: if calendar is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> calendar = api.add_cal(name='calendar1', data={'week' : '1-5'})
        >>> print calendar.to_json()
        {"data": {"week": "1-5", "calendar_name": "calendar1", "year": null}, "object_version": "1.0", "object_class": "Calendar", "created_on": "2016-06-20T23:23:05.594769", "created_by": "sinisa@univa.skaisoft.net"}
        """
        return self.calendar_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def add_cals(self, cal_list):
        """ Adds all UGE calendars in cal_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_cals(cal_list)
        """
        return self.calendar_manager.add_objects(cal_list)

    @api_call
    def add_cals_from_dir(self, dirname):
        """ Adds all UGE calendars from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_cals_from_dir('/tmp/cal_test')
        """
        return self.calendar_manager.add_objects_from_dir(dirname)

    @api_call
    def modify_cal(self, pycl_object=None, name=None, data=None,
                   metadata=None, json_string=None):
        """ Modify UGE calendar object.

        :param pycl_object: Calendar object to be modified.
        :type pycl_object: Calendar

        :param name: Calendar name; if provided, it will override calendar name in the provided calendar object, data dictionary, or in the json string.
        :type name: str

        :param data: Calendar data dictionary; if provided, dictionary values will override corresponding values from the calendar object, or from the json string.
        :type data: dict

        :param metadata: Calendar metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the calendar object to be modified.
        :type json_string: str

        :returns: Modified Calendar object.

        :raises InvalidArgument: if provided PYCL object is not an instance of Calendar, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify calendar name.
        :raises ObjectNotFound: in case calendar object with a given name does not exist, or an object contained in the calendar data cannot be found.
        :raises AuthorizationError: if calendar is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> calendar = api.modify_cal(name='calendar1', data={'year' : '1.2.2001'})
        >>> print calendar.to_json()
        {"modified_on": "2016-06-20T23:26:09.390538", "object_class": "Calendar", "object_version": "1.0", "modified_by": "sinisa@univa.skaisoft.net", "data": {"week": "1-5", "calendar_name": "calendar1", "year": "1.2.2001"}}
        """
        return self.calendar_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_cals(self, cal_list):
        """ Modifies all UGE calendars in cal_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_cals(cal_list)
        """
        return self.calendar_manager.modify_objects(cal_list)

    @api_call
    def modify_cals_from_dir(self, dirname):
        """ Modifies all UGE calendars from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_cals_from_dir('/tmp/cal_test')
        """
        return self.calendar_manager.modify_objects_from_dir(dirname)

    @api_call
    def get_cal(self, name):
        """ Retrieve UGE calendar configuration.

        :param name: Calendar name.
        :type name: str

        :returns: Calendar object.

        :raises ObjectNotFound: in case calendar object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> calendar = api.get_cal('calendar1')
        >>> print calendar.data['week']
        1-5
        """
        return self.calendar_manager.get_object(name)

    @api_call
    def get_cals(self):
        """ Retrieve all UGE calendars details.

        :returns: array of calendar dict objects.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> cal_dict_list = api.get_cals()

        """
        return self.calendar_manager.get_objects()

    @api_call
    def delete_cal(self, name):
        """ Delete UGE calendar.

        :param name: Calendar name.
        :type name: str

        :raises ObjectNotFound: in case calendar object with a given name does not exist.
        :raises InvalidRequest: if calendar is still referenced in other objects.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_cal('testcal')
        """
        return self.calendar_manager.delete_object(name)

    @api_call
    def delete_cals(self, cal_list):
        """ Deletes all UGE calendars in cal_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_cals(cal_list)
        """
        return self.calendar_manager.delete_object_list(cal_list)

    @api_call
    def delete_cals_from_dir(self, dirname):
        """ Delete UGE calendars from files in dir.

        :param dirname: Directory containing UGE calender object files.
        :type dirname: string

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_cals_from_dir('/tmp/cal_test')
        """
        return self.calendar_manager.delete_objects_from_dir(dirname)

    @api_call
    def list_cals(self):
        """ List UGE calendar names.

        :returns: QconfNameList object containing calendar names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> calendar_list = api.list_cals()
        >>> calendar_list
        ['calendar1']
        """
        return self.calendar_manager.list_objects()

    @api_call
    def mk_cals_dir(self, dirname):
        """ Make a temporary directory to write calendar data.

        >>> api.mk_cals_dir('/tmp/cals_test')
        """
        self.calendar_manager.mk_object_dir(dirname)

    @api_call
    def rm_cals_dir(self, dirname):
        """ Remove temporary calendar directory.

        >>> api.rm_cals_dir('/tmp/cals_test')
        """
        self.calendar_manager.rm_object_dir(dirname)

    @api_call
    def write_cals(self, cal_list, dirname):
        """ Write each calendar in cal_list to a seperate file in dir.

        >>> api.write_cals(cal_list, '/tmp/cals_test')
        """
        self.calendar_manager.write_objects(cal_list, dirname)

    #
    # CheckpointingEnvironment methods
    #

    @api_call
    def generate_ckpt(self, name=None, data=None, metadata=None,
                      json_string=None, uge_version=None,
                      add_required_data=True):
        """ Generate UGE checkpointing environment object.

        :param name: Checkpointing environment name; if provided, it will override environment name in the data dictionary, or in the json string.
        :type name: str

        :param data: Checkpointing environment data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Checkpointing environment metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the checkpointing environment object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which checkpointing environment object should be generated. By default, generated object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated CheckpointingEnvironment object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> ce = api.generate_ckpt(name='ckpt1')
        >>> ce.data['ckpt_name']
        'ckpt1'
        >>> ckpt.data['when']
        'sx'
        """
        return self.checkpointing_environment_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_ckpt(self, pycl_object=None, name=None, data=None,
                 metadata=None, json_string=None):
        """ Add UGE checkpointing environment. Default values for any missing required data keys will be added to the environment configuration.

        :param pycl_object: Checkpointing environment object to be added.
        :type pycl_object: CheckpointingEnvironment

        :param name: Checkpointing environment name; if provided, it will override environment name in the provided checkpointing environment object, data dictionary, or in the json string.
        :type name: str

        :param data: Checkpointing environment data dictionary; if provided, dictionary values will override corresponding values from the checkpointing environment object, or from the json string.
        :type data: dict

        :param metadata: Checkpointing environment metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the checkpointing environment object to be added.
        :type json_string: str

        :returns: Newly added CheckpointingEnvironment object.

        :raises InvalidArgument: if provided PYCL object is not an instance of CheckpointingEnvironment object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify checkpointing environment name.
        :raises ObjectAlreadyExists: in case checkpointing environment object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the checkpointing environment data does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_ckpt = api.add_ckpt(name='new_ckpt', data={'ckpt_dir' : '/storage'})
        >>> new_ckpt.data
        {'ckpt_command': None, 'clean_command': None, 'ckpt_dir': '/storage',...}
        """
        return self.checkpointing_environment_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def add_ckpts(self, ckpt_list):
        """ Adds all UGE checkpointing environment objects in ckpt_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_ckpts(ckpt_list)
        """
        return self.checkpointing_environment_manager.add_objects(ckpt_list)

    @api_call
    def add_ckpts_from_dir(self, dirname):
        """ Adds all UGE checkpointing environment objects from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_ckpts_from_dir('/tmp/ckpt_test')
        """
        return self.checkpointing_environment_manager.add_objects_from_dir(dirname)

    @api_call
    def modify_ckpt(self, pycl_object=None, name=None, data=None,
                    metadata=None, json_string=None):
        """ Modify UGE checkpointing environment object.

        :param pycl_object: Checkpointing environment object to be modified.
        :type pycl_object: CheckpointingEnvironment

        :param name: Checkpointing environment name; if provided, it will override environment name in the provided checkpointing environment object, data dictionary, or in the json string.
        :type name: str

        :param data: Checkpointing environment data dictionary; if provided, dictionary values will override corresponding values from the checkpointing environment object, or from the json string.
        :type data: dict

        :param metadata: Checkpointing environment metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the checkpointing environment object to be modified.
        :type json_string: str

        :returns: Modified CheckpointingEnvironment object.

        :raises InvalidArgument: if provided PYCL object is not an instance of CheckpointingEnvironment object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify checkpointing environment name.
        :raises ObjectNotFound: in case checkpointing environment object with a given name does not exist, or an object contained in the checkpointing environment data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_ckpt = api.get_ckpt('new_ckpt')
        >>> new_ckpt.data['ckpt_dir']
        '/storage'
        >>> new_ckpt.data['ckpt_dir'] = '/disk1'
        >>> new_ckpt = api.modify_ckpt(pycl_object=new_ckpt)
        >>> new_ckpt.data['ckpt_dir']
        '/disk1'
        """
        return self.checkpointing_environment_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_ckpts(self, ckpt_list):
        """ Modify all UGE checkpointing environment objects in ckpt_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_ckpts(ckpt_list)
        """
        return self.checkpointing_environment_manager.modify_objects(ckpt_list)

    @api_call
    def modify_ckpts_from_dir(self, dirname):
        """ Modify all UGE checkpointing environment objects from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_ckpts_from_dir('/tmp/ckpt_test')
        """
        return self.checkpointing_environment_manager.modify_objects_from_dir(dirname)

    @api_call
    def get_ckpt(self, name):
        """ Retrieve UGE checkpointing environment configuration.

        :param name: Checkpointing environment name.
        :type name: str

        :returns: CheckpointingEnvironment object.

        :raises ObjectNotFound: in case checkpointing environment object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> new_ckpt = api.get_ckpt('new_ckpt')
        >>> new_ckpt.data
        {'ckpt_command': None, 'when': 'xs', 'ckpt_dir': '/disk1',..., 'ckpt_name': 'new_ckpt',...}
        """
        return self.checkpointing_environment_manager.get_object(name)

    @api_call
    def get_ckpts(self):
        """ Retrieve all UGE checkpointing environment objects details.

        :returns: array of checkpointing environment dict objects.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> ckpt_dict_list = api.get_ckpts()
        """
        return self.checkpointing_environment_manager.get_objects()

    @api_call
    def delete_ckpt(self, name):
        """ Delete UGE checkpointing environment configuration.

        :param name: Checkpointing environment name.
        :type name: str

        :raises ObjectNotFound: in case checkpointing environment object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_ckpt('new_ckpt')
        """
        return self.checkpointing_environment_manager.delete_object(name)

    @api_call
    def delete_ckpts(self, ckpt_list):
        """ Deletes all UGE checkpointing environment objects in ckpt_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_ckpts(ckpt_list)
        """
        return self.checkpointing_environment_manager.delete_object_list(ckpt_list)

    @api_call
    def delete_ckpts_from_dir(self, dirname):
        """ Delete all UGE checkpointing environments from files in dir.

        :param dirname: Directory containing UGE checkpointing environment object files.
        :type dirname: string

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_ckpts_from_dir('/tmp/ckpt_test')
        """
        return self.checkpointing_environment_manager.delete_objects_from_dir(dirname)

    @api_call
    def list_ckpts(self):
        """ List UGE checkpointing environment names.

        :returns: QconfNameList object containing checkpointing environment names.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> ckpt_list = api.list_ckpts()
        >>> ckpt_list
        ['ckpt1']
        """
        return self.checkpointing_environment_manager.list_objects()

    @api_call
    def mk_ckpts_dir(self, dirname):
        """ Make a temporary directory to write UGE checkpointing environment data.

        >>> api.mk_ckpts_dir('/tmp/ckpts_test')
        """
        self.checkpointing_environment_manager.mk_object_dir(dirname)

    @api_call
    def rm_ckpts_dir(self, dirname):
        """ Remove temporary UGE checkpointing environments directory.

        >>> api.rm_ckpts_dir('/tmp/ckpts_test')
        """
        self.checkpointing_environment_manager.rm_object_dir(dirname)

    @api_call
    def write_ckpts(self, ckpt_list, dirname):
        """ Write each UGE checkpointing environment in ckpt_list to a seperate file in dir.

        >>> api.write_ckpts(ckpt_list, '/tmp/ckpts_test')
        """
        self.checkpointing_environment_manager.write_objects(ckpt_list, dirname)

    #
    # AccessList methods
    #

    @api_call
    def generate_acl(self, name=None, data=None, metadata=None,
                     json_string=None, uge_version=None,
                     add_required_data=True):
        """ Generate UGE access list object.

        :param name: Access list name; if provided, it will override ACL name in the data dictionary, or in the json string.
        :type name: str

        :param data: Access list data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Access list metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the access list object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which access list object should be generated. By default, generated object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated AccessList object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> acl = api.generate_acl(name='acl1')
        >>> acl.data['name']
        'acl1'
        >>> acl.data['type']
        'ACL'
        """
        return self.access_list_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_acl(self, pycl_object=None, name=None, data=None,
                metadata=None, json_string=None):
        """ Add UGE access list. Default values for any missing required data keys will be added to the ACL configuration.

        :param pycl_object: Access list object to be added.
        :type pycl_object: AccessList

        :param name: Access list name; if provided, it will override ACL name in the provided access list object, data dictionary, or in the json string.
        :type name: str

        :param data: Access list data dictionary; if provided, dictionary values will override corresponding values from the access list object, or from the json string.
        :type data: dict

        :param metadata: Access list metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the access list object to be added.
        :type json_string: str

        :returns: Newly added AccessList object.

        :raises InvalidArgument: if provided PYCL object is not an instance of AccessList object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify access list name.
        :raises ObjectAlreadyExists: in case access list object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the access list data does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> acl = api.add_acl(name='acl2', data={'entries' : 'user1,user2'})
        >>> print acl.data
        {'oticket': 0, 'fshare': 0, 'type': 'ACL', 'name': 'acl2', 'entries': ['user1', 'user2']}
        """
        return self.access_list_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def add_acls(self, acl_list):
        """ Adds all UGE access list objects in acl_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_acls(acl_list)
        """
        return self.access_list_manager.add_objects(acl_list)

    @api_call
    def add_acls_from_dir(self, dirname):
        """ Adds all UGE access list objects from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.add_acls_from_dir('/tmp/acl_test')
        """
        return self.access_list_manager.add_objects_from_dir(dirname)

    @api_call
    def modify_acl(self, pycl_object=None, name=None, data=None,
                   metadata=None, json_string=None):
        """ Modify UGE access list object.

        :param pycl_object: Access list object to be modified.
        :type pycl_object: AccessList

        :param name: Access list name; if provided, it will override ACL name in the provided access list object, data dictionary, or in the json string.
        :type name: str

        :param data: Access list data dictionary; if provided, dictionary values will override corresponding values from the access list object, or from the json string.
        :type data: dict

        :param metadata: Access list metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the access list object to be modified.
        :type json_string: str

        :returns: Modified AccessList object.

        :raises InvalidArgument: if provided PYCL object is not an instance of AccessList object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify access list name.
        :raises ObjectNotFound: in case access list object with a given name does not exist, or an object contained in the access list data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> acl = api.get_acl('acl2')
        >>> acl.data['entries']
        ['user1', 'user2']
        >>> acl.data['entries'] = ['user1', 'user2', 'user3']
        >>> acl = api.modify_acl(pycl_object=acl)
        >>> acl.data['entries']
        ['user1', 'user2', 'user3']
        """
        return self.access_list_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_acls(self, acl_list):
        """ Modify all UGE access list objects in acl_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_acls(acl_list)
        """
        return self.access_list_manager.modify_objects(acl_list)

    @api_call
    def modify_acls_from_dir(self, dirname):
        """ Modify all UGE access list objects from files in dir.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.modify_acls_from_dir('/tmp/acl_test')
        """
        return self.access_list_manager.modify_objects_from_dir(dirname)

    @api_call
    def get_acl(self, name):
        """ Retrieve UGE access list configuration.

        :param name: Access list name.
        :type name: str

        :returns: AccessList object.

        :raises ObjectNotFound: in case access list object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> acl = api.get_acl('acl2')
        >>> acl.data
        {'oticket': 0, 'entries': ['user1', 'user2', 'user3'], 'type': 'ACL', 'name': 'acl2', 'fshare': 0}
        """
        return self.access_list_manager.get_object(name)

    @api_call
    def get_acls(self):
        """ Retrieve all UGE access list objects details.

        :returns: array of access list dict objects.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> acl_dict_list = api.get_acls()
        """
        return self.access_list_manager.get_objects()

    @api_call
    def delete_acl(self, name):
        """ Delete UGE access list configuration.

        :param name: access list name.
        :type name: str

        :raises ObjectNotFound: in case access list object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_acl('acl2')
        """
        return self.access_list_manager.delete_object(name)

    @api_call
    def delete_acls(self, acl_list):
        """ Deletes all UGE access lists in acl_list.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_acls(acl_list)
        """
        return self.access_list_manager.delete_object_list(acl_list)

    @api_call
    def delete_acls_from_dir(self, dirname):
        """ Delete all UGE access lists from files in dir.

        :param dirname: Directory containing UGE access list object files.
        :type dirname: string

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_acls_from_dir('/tmp/acl_test')
        """
        return self.access_list_manager.delete_objects_from_dir(dirname)

    @api_call
    def list_acls(self):
        """ List UGE access list names.

        :returns: QconfNameList object containing names of existing access lists.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> acl_list = api.list_acls()
        >>> acl_list
        ['acl1', 'arusers', 'deadlineusers', 'defaultdepartment']
        """
        return self.access_list_manager.list_objects()

    @api_call
    def mk_acls_dir(self, dirname):
        """ Make a temporary directory to write UGE access list data.

        >>> api.mk_acls_dir('/tmp/acls_test')
        """
        self.access_list_manager.mk_object_dir(dirname)

    @api_call
    def rm_acls_dir(self, dirname):
        """ Remove temporary UGE access lists directory.

        >>> api.rm_acls_dir('/tmp/acls_test')
        """
        self.access_list_manager.rm_object_dir(dirname)

    @api_call
    def write_acls(self, acl_list, dirname):
        """ Write each UGE access list in acl_list to a seperate file in dir.

        >>> api.write_acls(acl_list, '/tmp/acls_test')
        """
        self.access_list_manager.write_objects(acl_list, dirname)

    def add_users_to_acls(self, user_names, access_list_names):
        """ Add users to UGE access lists.

        :param user_names: Comma-separated list of user names.
        :type name: str

        :param access_list_names: Comma-separated list of access list names.
        :type name: str

        :returns: List of modified AccessList objects.

        :raises ObjectNotFound: in case one of the specified access lists is not found.
        :raises ObjectAlreadyExists: in case some users are already members of one or more specified access lists.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> acl_list = api.add_users_to_acls('user1,user2,user3', 'acl1,acl2')
        """
        return self.access_list_manager.add_users_to_acls(user_names, access_list_names)

    def delete_users_from_acls(self, user_names, access_list_names):
        """ Delete users from UGE access lists.

        :param user_names: Comma-separated list of user names.
        :type name: str

        :param access_list_names: Comma-separated list of access list names.
        :type name: str

        :returns: List of modified AccessList objects.

        :raises ObjectNotFound: in case one of the specified access lists is not found, or some users are not in specified access lists.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> acl_list = api.delete_users_from_acls('user1,user2,user3', 'acl1,acl2')
        """
        return self.access_list_manager.delete_users_from_acls(user_names, access_list_names)

    #
    # SchedulerConfiguration methods
    #

    @api_call
    def generate_sconf(self, data=None, metadata=None,
                       json_string=None, uge_version=None,
                       add_required_data=True):
        """ Generate UGE scheduler configuration object.

        :param data: Scheduler configuration data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Scheduler configuration metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the scheduler configuration object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which scheduler configuration object should be generated. By default, generated object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated SchedulerConfiguration object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> sconf = api.generate_sconf()
        >>> sconf.data['algorithm']
        'default'
        """
        return self.scheduler_configuration_manager.generate_object(
            data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def modify_sconf(self, pycl_object=None, data=None,
                     metadata=None, json_string=None):
        """ Modify UGE scheduler configuration object.

        :param pycl_object: Scheduler configuration object to be modified.
        :type pycl_object: SchedulerConfiguration 

        :param data: Scheduler configuration data dictionary; if provided, dictionary values will override corresponding values from the scheduler configuration object, or from the json string.
        :type data: dict

        :param metadata: Scheduler configuration metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the scheduler configuration object to be modified.
        :type json_string: str

        :returns: Modified SchedulerConfiguration object.

        :raises InvalidArgument: if provided PYCL object is not an instance of SchedulerConfiguration object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises ObjectNotFound: in case an object contained in the scheduler configuration data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> sconf = api.get_sconf()
        >>> sconf.data['weight_department']
        0.25
        >>> sconf.data['weight_department'] = 0.5
        >>> sconf = api.modify_sconf(pycl_object=sconf)
        >>> sconf.data['weight_department']
        0.50
        """
        return self.scheduler_configuration_manager.modify_object(
            pycl_object=pycl_object, name='', data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def get_sconf(self):
        """ Retrieve UGE scheduler configuration.

        :returns: SchedulerConfiguration object.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> sconf = api.get_sconf()
        >>> sconf.data
        {'queue_sort_method': 'load', 'job_load_adjustments': ['np_load_avg=0.50'], 'flush_submit_sec': 2,...}
        """
        return self.scheduler_configuration_manager.get_object('')

    #
    # JobClass methods
    #

    @api_call
    def generate_jc(self, name=None, data=None, metadata=None,
                    json_string=None, uge_version=None,
                    add_required_data=True):
        """ Generate UGE job class object.

        :param name: Job class name; if provided, it will override job class name in the data dictionary, or in the json string.
        :type name: str

        :param data: Job class data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Job class metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the job class object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which job class object should be generated. By default, generated object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated JobClass object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> jc = api.generate_jc(name='jc1')
        >>> print jc.data
        {'ac': '{+}UNSPECIFIED', 'c_occasion': '{+}UNSPECIFIED',...}
        """
        return self.job_class_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_jc(self, pycl_object=None, name=None, data=None,
               metadata=None, json_string=None):
        """ Add UGE job class. Default values for any missing required data keys will be added to the job class configuration.

        :param pycl_object: Job class object to be added.
        :type pycl_object: JobClass 

        :param name: Job class name; if provided, it will override job class name in the provided job class object, data dictionary, or in the json string.
        :type name: str

        :param data: Job class data dictionary; if provided, dictionary values will override corresponding values from the job class object, or from the json string.
        :type data: dict

        :param metadata: Job class metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the job class object to be added.
        :type json_string: str

        :returns: Newly added JobClass object.

        :raises InvalidArgument: if provided PYCL object is not an instance of JobClass object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify job class name.
        :raises ObjectAlreadyExists: in case job class object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the job class data does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> jc = api.add_jc(name='jc2', data = {'user_lists' : 'acl1,acl2'})
        >>> print jc.data
        {'ac': '{+}UNSPECIFIED', 'c_occasion': '{+}UNSPECIFIED',...} 
        >>> print jc.data['user_lists']
        ['acl1', 'acl2']
        """
        return self.job_class_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_jc(self, pycl_object=None, name=None, data=None,
                  metadata=None, json_string=None):
        """ Modify UGE job class object.

        :param pycl_object: Job class object to be modified.
        :type pycl_object: JobClass 

        :param name: Job class name; if provided, it will override job class name in the provided job class object, data dictionary, or in the json string.
        :type name: str

        :param data: Job class data dictionary; if provided, dictionary values will override corresponding values from the job class object, or from the json string.
        :type data: dict

        :param metadata: Job class metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the job class object to be modified.
        :type json_string: str

        :returns: Modified JobClass object.

        :raises InvalidArgument: if provided PYCL object is not an instance of JobClass object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify job class name.
        :raises ObjectNotFound: in case job class object with a given name does not exist, or an object contained in the job class data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> jc = api.get_jc('jc2')
        >>> jc.data['user_lists' ] 
        ['acl1', 'acl2']
        >>> jc.data['user_lists' ] = 'acl1'
        >>> jc = api.modify_jc(pycl_object=jc)
        >>> jc.data['user_lists' ] 
        ['acl1']
        """
        return self.job_class_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def get_jc(self, name):
        """ Retrieve UGE job class configuration.

        :param name: Job class name.
        :type name: str

        :returns: JobClass object.

        :raises ObjectNotFound: in case job class object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> jc = api.get_jc('jc2')
        >>> jc.data
        {'ac': '{+}UNSPECIFIED', 'c_occasion': '{+}UNSPECIFIED',...}
        """
        return self.job_class_manager.get_object(name)

    @api_call
    def delete_jc(self, name):
        """ Delete UGE job class configuration.

        :param name: Job class name.
        :type name: str

        :raises ObjectNotFound: in case job class object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_jc('jc2')
        """
        return self.job_class_manager.delete_object(name)

    @api_call
    def list_jcs(self):
        """ List UGE job class names.

        :returns: QconfNameList object containing names of existing job classs.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> jc_list = api.list_jcs()
        >>> jc_list
        ['jc1', 'template']
        """
        return self.job_class_manager.list_objects()

    #
    # ClusterConfiguration methods
    #

    @api_call
    def generate_conf(self, name=None, data=None, metadata=None,
                      json_string=None, uge_version=None,
                      add_required_data=True):
        """ Generate UGE cluster configuration object.

        :param name: Cluster configuration name (must be either 'global' or valid host name); if provided, it will override configuration name in the data dictionary, or in the json string. 
        :type name: str

        :param data: Cluster configuration data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Cluster configuration metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the cluster configuration object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which cluster configuration object should be generated. By default, generated object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated ClusterConfiguration object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> conf = api.generate_conf(name='univa')
        >>> print conf.name
        univa
        >>> print conf.data
        {'mailer': '/bin/mail', 'xterm': '/usr/bin/xterm'}
        """
        return self.cluster_configuration_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_conf(self, pycl_object=None, name=None, data=None,
                 metadata=None, json_string=None):
        """ Add UGE cluster configuration object. Default values for any missing required data keys will be added to the configuration configuration.

        :param pycl_object: Cluster configuration object to be added.
        :type pycl_object: ClusterConfiguration 

        :param name: Cluster configuration name (must be valid host name); if provided, it will override configuration name in the provided cluster configuration object, data dictionary, or in the json string.
        :type name: str

        :param data: Cluster configuration data dictionary; if provided, dictionary values will override corresponding values from the cluster configuration object, or from the json string.
        :type data: dict

        :param metadata: Cluster configuration metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the cluster configuration object to be added.
        :type json_string: str

        :returns: Newly added ClusterConfiguration object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ClusterConfiguration object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify cluster configuration name.
        :raises ObjectAlreadyExists: in case cluster configuration object with a given name already exists.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> conf = api.add_conf(name='univa2')
        >>> print conf.data
        {'mailer': '/bin/mail', 'xterm': '/usr/bin/xterm'}
        >>> print conf.name
        univa2
        """
        return self.cluster_configuration_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_conf(self, pycl_object=None, name=None, data=None,
                    metadata=None, json_string=None):
        """ Modify UGE cluster configuration object.

        :param pycl_object: Cluster configuration object to be modified.
        :type pycl_object: ClusterConfiguration 

        :param name: Cluster configuration name (must be either 'global' or valid host name); if provided, it will override configuration name in the provided cluster configuration object, data dictionary, or in the json string.
        :type name: str

        :param data: Cluster configuration data dictionary; if provided, dictionary values will override corresponding values from the cluster configuration object, or from the json string.
        :type data: dict

        :param metadata: Cluster configuration metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the cluster configuration object to be modified.
        :type json_string: str

        :returns: Modified ClusterConfiguration object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ClusterConfiguration object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify cluster configuration name.
        :raises ObjectNotFound: in case cluster configuration object with a given name does not exist, or an object contained in the cluster configuration data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> c = api.get_conf()
        >>> c.data['max_jobs']
        0
        >>> c.data['max_jobs'] = 10
        >>> c = api.modify_conf(pycl_object=c)
        >>> c.data['max_jobs']
        10
        """
        return self.cluster_configuration_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def get_conf(self, name='global'):
        """ Retrieve UGE cluster configuration configuration.

        :param name: Cluster configuration name (must be either 'global' or a valid host name; default: 'global').
        :type name: str

        :returns: ClusterConfiguration object.

        :raises ObjectNotFound: in case cluster configuration object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> conf = api.get_conf()
        >>> print conf.data
        {'rlogin_command': 'builtin', 'enforce_jc': False, 'rlogin_daemon': 'builtin',...}
        >>> print c.name
        global
        """
        return self.cluster_configuration_manager.get_object(name)

    @api_call
    def delete_conf(self, name):
        """ Delete UGE cluster configuration configuration.

        :param name: Cluster configuration name (must be valid host name).
        :type name: str

        :raises ObjectNotFound: in case cluster configuration object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_conf('univa2')
        """
        return self.cluster_configuration_manager.delete_object(name)

    @api_call
    def list_confs(self):
        """ List UGE cluster configuration names.

        :returns: QconfNameList object containing names of existing cluster configurations.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> conf_list = api.list_confs()
        >>> conf_list
        ['univa.skaisoft.net', 'univa2.skaisoft.net']
        """
        return self.cluster_configuration_manager.list_objects()

    #
    # ComplexConfiguration methods
    #

    @api_call
    def generate_cconf(self, data=None, metadata=None,
                       json_string=None, uge_version=None,
                       add_required_data=True):
        """ Generate UGE complex configuration object.

        :param data: Complex configuration data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Complex configuration metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the complex configuration object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which complex configuration object should be generated. By default, generated object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated ComplexConfiguration object.

        :raises InvalidArgument: if provided data is not a dictionary, json_string does not represent a valid JSON object, or if attribute data is not valid.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> cconf = api.generate_cconf()
        >>> cconf.data['slots']
        {'requestable': True,..., 'urgency': 1000, 'consumable': True, 'type': 'INT', 'shortcut': 's'}
        """
        return self.complex_configuration_manager.generate_object(
            data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def modify_cconf(self, pycl_object=None, data=None,
                     metadata=None, json_string=None):
        """ Modify UGE complex configuration object.

        :param pycl_object: Complex configuration object to be modified.
        :type pycl_object: ComplexConfiguration 

        :param data: Complex configuration data dictionary; if provided, dictionary values will override corresponding values from the complex configuration object, or from the json string.
        :type data: dict

        :param metadata: Complex configuration metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the complex configuration object to be modified.
        :type json_string: str

        :returns: Modified ComplexConfiguration object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ComplexConfiguration object, or data is not a dictionary, if json_string does not represent a valid JSON object, or if attribute data is not valid.
        :raises ObjectNotFound: in case an object contained in the complex configuration data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> cconf = api.get_cconf()
        >>> cconf.data['slots']
        {'requestable': True,..., 'urgency': 900, 'consumable': True, 'type': 'INT', 'shortcut': 's'}
        >>> cconf.data['slots']['urgency'] = 800
        >>> cconf = api.modify_cconf(cconf)
        >>> cconf.data['slots']
        {'requestable': True,..., 'urgency': 800, 'consumable': True, 'type': 'INT', 'shortcut': 's'}
        """
        return self.complex_configuration_manager.modify_object(
            pycl_object=pycl_object, name='', data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def get_cconf(self):
        """ Retrieve UGE complex configuration.

        :returns: ComplexConfiguration object.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> cconf = api.get_cconf()
        >>> cconf.data
        {'s_stack': {'requestable': True,..., 'urgency': 0, 'consumable': False, 'type': 'MEMORY', 'shortcut': 's_stack'},...}
        """
        return self.complex_configuration_manager.get_object('')

    @api_call
    def add_cattr(self, name, data):
        """ Add attribute to UGE complex configuration.

        :param name: Complex attribute name.
        :type name: str

        :param data: Complex attribute data. It must be a dictionary with all required keys (shortcut, type, relop, requestable, consumable, default, urgency, aapre).
        :type data: dict

        :returns: ComplexConfiguration object.

        :raises ObjectAlreadyExists: in case attribute with specified name already exists.
        :raises InvalidArgument: in case of invalid attribute data.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> cconf = api.add_cattr('xyz', {'shortcut' : 'xyz', 'type' : 'INT', 'relop' : '<=', 'requestable' : True,
        ... 'consumable' : True, 'default' : 10, 'urgency' : 50, 'aapre' : False})
        >>> print cconf.data['xyz']
        {'requestable': True,..., 'urgency': 50, 'consumable': True, 'type': 'INT', 'shortcut': 'xyz'}
        """
        return self.complex_configuration_manager.add_cattr(name, data)

    @api_call
    def modify_cattr(self, name, data):
        """ Modify attribute for UGE complex configuration.

        :param name: Complex attribute name.
        :type name: str

        :param data: Complex attribute data. It must be a dictionary containing all attribute keys that will be modified.
        :type data: dict

        :returns: ComplexConfiguration object.

        :raises ObjectNotFound: in case attribute with specified name does not exist.
        :raises InvalidArgument: in case of invalid attribute data.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> cconf = api.get_cconf()
        >>> attr_data = cconf.data['xyz']
        >>> attr_data['default']
        10
        >>> cconf = api.modify_cattr('xyz', {'default' : 15})
        >>> print cconf.data['xyz']['default']
        15
        """
        return self.complex_configuration_manager.modify_cattr(name, data)

    @api_call
    def delete_cattr(self, name):
        """ Delete attribute for UGE complex configuration.

        :param name: Complex attribute name.
        :type name: str

        :returns: ComplexConfiguration object.

        :raises ObjectNotFound: in case attribute with specified name does not exist.
        :raises InvalidRequest: in case attribute with specified name cannot be deleted.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> cconf = api.delete_cattr('xyz')
        """
        return self.complex_configuration_manager.delete_cattr(name)

    #
    # ResourceQuotaSet methods
    #

    @api_call
    def generate_rqs(self, name=None, data=None, metadata=None,
                     json_string=None, uge_version=None,
                     add_required_data=True):
        """ Generate UGE resource quota set object.

        :param name: Resource quota set name; if provided, it will override resource quota set name in the data dictionary, or in the json string.
        :type name: str

        :param data: Resource quota set data dictionary; if provided, dictionary values will override corresponding values from the json string.
        :type data: dict

        :param metadata: Resource quota set metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the resource quota set object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which resource quota set object should be generated. By default, generated object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from the provided data dictionary (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated ResourceQuotaSet object.

        :raises InvalidArgument: if provided data is not a dictionary, or json_string does not represent a valid JSON object.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> rqs = api.generate_rqs(name='rqs1')
        >>> print rqs.data
        {'enabled': False, 'limit': ['to slots=0'], 'name': 'rqs1', 'description': None}
        """
        return self.resource_quota_set_manager.generate_object(
            name=name, data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_rqs(self, pycl_object=None, name=None, data=None,
                metadata=None, json_string=None):
        """ Add UGE resource quota set. Default values for any missing required data keys will be added to the resource quota set configuration.

        :param pycl_object: Resource quota set object to be added.
        :type pycl_object: ResourceQuotaSet 

        :param name: Resource quota set name; if provided, it will override resource quota set name in the provided resource quota set object, data dictionary, or in the json string.
        :type name: str

        :param data: Resource quota set data dictionary; if provided, dictionary values will override corresponding values from the resource quota set object, or from the json string.
        :type data: dict

        :param metadata: Resource quota set metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the resource quota set object to be added.
        :type json_string: str

        :returns: Newly added ResourceQuotaSet object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ResourceQuotaSet object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify resource quota set name.
        :raises ObjectAlreadyExists: in case resource quota set object with a given name already exists.
        :raises ObjectNotFound: in case an object contained in the resource quota set data does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> rqs = api.add_rqs(name='rqs1')
        >>> print rqs.data
        {'enabled': False, 'limit': ['to slots=0'], 'name': 'rqs1', 'description': None}
        """
        return self.resource_quota_set_manager.add_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_rqs(self, pycl_object=None, name=None, data=None,
                   metadata=None, json_string=None):
        """ Modify UGE resource quota set object.

        :param pycl_object: Resource quota set object to be modified.
        :type pycl_object: ResourceQuotaSet

        :param name: Resource quota set name; if provided, it will override resource quota set name in the provided resource quota set object, data dictionary, or in the json string.
        :type name: str

        :param data: Resource quota set data dictionary; if provided, dictionary values will override corresponding values from the resource quota set object, or from the json string.
        :type data: dict

        :param metadata: Resource quota set metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the resource quota set object to be modified.
        :type json_string: str

        :returns: Modified ResourceQuotaSet object.

        :raises InvalidArgument: if provided PYCL object is not an instance of ResourceQuotaSet object, or data is not a dictionary, or if json_string does not represent a valid JSON object.
        :raises InvalidRequest: if provided arguments do not specify resource quota set name.
        :raises ObjectNotFound: in case resource quota set object with a given name does not exist, or an object contained in the resource quota set data cannot be found.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> rqs = api.get_rqs('rqs1')
        >>> print rqs.data['enabled']
        False
        >>> rqs.data['enabled'] = True
        >>> rqs = api.modify_rqs(pycl_object=rqs)
        >>> print rqs.data['enabled']
        True
        """
        return self.resource_quota_set_manager.modify_object(
            pycl_object=pycl_object, name=name, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def get_rqs(self, name):
        """ Retrieve UGE resource quota set configuration.

        :param name: Resource quota set name.
        :type name: str

        :returns: ResourceQuotaSet object.

        :raises ObjectNotFound: in case resource quota set object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> rqs = api.get_rqs('rqs1')
        >>> print rqs.data
        {'limit': ['to slots=0'], 'enabled': True, 'name': 'rqs1', 'description': None}
        """
        return self.resource_quota_set_manager.get_object(name)

    @api_call
    def delete_rqs(self, name):
        """ Delete UGE resource quota set configuration.

        :param name: Resource quota set name.
        :type name: str

        :raises ObjectNotFound: in case resource quota set object with a given name does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_rqs('rqs2')
        """
        return self.resource_quota_set_manager.delete_object(name)

    @api_call
    def list_rqss(self):
        """ List UGE resource quota set names.

        :returns: QconfNameList object containing names of existing resource quota sets.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> rqs_list = api.list_rqss()
        >>> rqs_list
        ['rqs1']
        """
        return self.resource_quota_set_manager.list_objects()

    #
    # ShareTree methods
    #

    @api_call
    def generate_stree(self, data=None, metadata=None,
                       json_string=None, uge_version=None,
                       add_required_data=True):
        """ Generate UGE share tree object.

        :param data: Share tree data; if provided, list will override json string.
        :type data: list

        :param metadata: Share tree metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the share tree object to be generated.
        :type json_string: str

        :param uge_version: UGE version for which share tree object should be generated. By default, generated object will correspond to UGE version used by the QconfApi instance.
        :type uge_version: str

        :param add_required_data: If true, default values for any required keys missing from dictionaries in the provided list (or from the provided JSON object) will be added to the generated object.
        :type add_required_data: bool

        :returns: Generated ShareTree object.

        :raises InvalidArgument: if provided data is not a list of dictionaries, json_string does not represent a valid JSON object, or if attribute data is not valid.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> stree = api.generate_stree(data=[{'name' : 'P1'}])
        >>> print stree.data
        [{'childnodes': None, 'type': 1, 'name': 'P1', 'shares': 0, 'id': 0}]
        >>> print stree.to_uge()
        id=0
        name=P1
        type=1
        shares=0
        childnodes=NONE
        """
        return self.share_tree_manager.generate_object(
            data=data, metadata=metadata,
            json_string=json_string, uge_version=uge_version,
            add_required_data=add_required_data)

    @api_call
    def add_stree(self, pycl_object=None, data=None,
                  metadata=None, json_string=None):
        """ Add UGE share tree object.

        :param pycl_object: Share tree object to be added.
        :type pycl_object: ShareTree 

        :param data: Share tree data; if provided, list will override json string.
        :type data: list

        :param metadata: Share tree metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the share tree object.
        :type json_string: str

        :returns: Newly added ShareTree object.

        :raises InvalidArgument: if provided data is not a list of dictionaries, json_string does not represent a valid JSON object, or if attribute data is not valid.
        :raises ObjectAlreadyExists: in case share tree object already exists.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> stree = api.add_stree(data=[
        ... {'id' : 0, 'name' : 'Root', 'type' : 0, 'shares' : 1, 'childnodes' : '1,2'}, 
        ... {'id' : 1, 'name' : 'P1', 'shares' : 70}, 
        ... {'id' : 2, 'name' : 'P2', 'shares' : 30}])
        >>> print stree.data[1]['shares']
        70
        """
        return self.share_tree_manager.add_object(
            pycl_object=pycl_object, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_stree(self, pycl_object=None, data=None,
                     metadata=None, json_string=None):
        """ Modify UGE share tree object.

        :param pycl_object: Share tree object to be modified.
        :type pycl_object: ShareTree 

        :param data: Share tree data; if provided, list will override json string.
        :type data: list

        :param metadata: Share tree metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the share tree object.
        :type json_string: str

        :returns: Modified ShareTree object.

        :raises InvalidArgument: if provided data is not a list of dictionaries, json_string does not represent a valid JSON object, or if attribute data is not valid.
        :raises ObjectNotFound: in case share tree object does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> stree = api.get_stree()
        >>> print stree.data[1]
        {'childnodes': None, 'type': 1, 'id': 1, 'shares': 70, 'name': 'P1'}
        >>> print stree.data[2]
        {'childnodes': None, 'type': 1, 'id': 2, 'shares': 30, 'name': 'P2'}
        >>> stree.data[1]['shares'] = 80 
        >>> stree.data[2]['shares'] = 20;
        >>> stree = api.modify_stree(stree)
        >>> print stree.data[1]
        {'childnodes': None, 'type': 1, 'id': 1, 'shares': 80, 'name': 'P1'}
        >>> print stree.data[2]
        {'childnodes': None, 'type': 1, 'id': 2, 'shares': 20, 'name': 'P2'}
        """
        return self.share_tree_manager.modify_object(
            pycl_object=pycl_object, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def modify_or_add_stree(self, pycl_object=None, data=None,
                            metadata=None, json_string=None):
        """ Modify UGE share tree object, or add it if it does not exist.

        :param pycl_object: Share tree object to be modified.
        :type pycl_object: ShareTree 

        :param data: Share tree data; if provided, list will override json string.
        :type data: list

        :param metadata: Share tree metadata dictionary.
        :type metadata: dict

        :param json_string: JSON string representation of the share tree object.
        :type json_string: str

        :returns: Modified or added ShareTree object.

        :raises InvalidArgument: if provided data is not a list of dictionaries, json_string does not represent a valid JSON object, or if attribute data is not valid.
        :raises ObjectNotFound: in case one of the nodes in the share tree object does not exist.
        :raises AuthorizationError: if user is not authorized to make changes to UGE configuration.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> stree = api.get_stree_if_exists()
        >>> print stree.data
        []
        >>> stree = api.modify_or_add_stree(data=[
        ... {'id' : 0, 'name' : 'Root', 'type' : 0, 'shares' : 1, 'childnodes' : '1,2'}, 
        ... {'id' : 1, 'name' : 'P1', 'shares' : 70}, 
        ... {'id' : 2, 'name' : 'P2', 'shares' : 30}])
        >>> print stree.data[2]
        {'childnodes': None, 'type': 1, 'id': 2, 'shares': 20, 'name': 'P2'}
        """
        return self.share_tree_manager.modify_or_add_object(
            pycl_object=pycl_object, data=data,
            metadata=metadata, json_string=json_string)

    @api_call
    def get_stree(self):
        """ Retrieve UGE share tree object.

        :returns: ShareTree object.

        :raises ObjectNotFound: in case share tree object does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> stree = api.get_stree()
        >>> print stree.data[0]
        {'childnodes': ['1', '2'], 'type': 0, 'id': 0, 'shares': 1, 'name': 'Root'}
        """
        return self.share_tree_manager.get_object()

    @api_call
    def get_stree_if_exists(self):
        """ Retrieve UGE share tree object if it exists.

        :returns: ShareTree object, or empty list if share tree is not defined.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> stree = api.get_stree_if_exists()
        >>> print stree
        []
        """
        return self.share_tree_manager.get_object_if_exists()

    @api_call
    def delete_stree(self):
        """ Delete UGE share tree object.

        :raises ObjectNotFound: in case share tree object does not exist.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_stree()
        """
        return self.share_tree_manager.delete_object()

    @api_call
    def delete_stree_if_exists(self):
        """ Delete UGE share tree object if it exists.

        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> api.delete_stree_if_exists()
        """
        return self.share_tree_manager.delete_object_if_exists()

    @api_call
    def add_stnode(self, path, shares):
        """ Add UGE share tree node.

        :param path: Node path.
        :type path: str

        :param shares: Number of shares to be assigned to the node.
        :type path: int

        :returns: Modified ShareTree object.

        :raises ObjectNotFound: in case share tree object does not exist, or specified path cannot be found.
        :raises InvalidArgument: in case number of shares is not a positive number.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> stree = api.add_stnode('/P3', 25)
        >>> print stree.data[-1]
        {'childnodes': None, 'type': 1, 'id': 3, 'shares': 25, 'name': 'P3'}
        """
        return self.share_tree_manager.add_stnode(path, shares)

    @api_call
    def delete_stnode(self, path):
        """ Delete UGE share tree node.

        :param path: Node path.
        :type path: str

        :returns: Modified ShareTree object.

        :raises ObjectNotFound: in case share tree object does not exist, or specified path cannot be found.
        :raises QmasterUnreachable: in case UGE Qmaster cannot be reached.
        :raises QconfException: for any other errors.

        >>> stree = api.delete_stnode('/P3')
        >>> print stree.data[-1]
        {'childnodes': None, 'type': 1, 'id': 2, 'shares': 0, 'name': 'P2'}
        """
        return self.share_tree_manager.delete_stnode(path)


#############################################################################
# Testing.
if __name__ == '__main__':
    lm = LogManager.get_instance()
    lm.set_console_log_level('trace')
    # api = QconfApi(sge_root='/opt/uge-8.3.1p9')
    api = QconfApi()
    new_q = api.generate_queue('new.q')
    print(new_q.to_json())
    # all_q = api.get_queue('all.q2')
    all_q = api.get_queue('all.q')
    print(all_q.to_json())
    print()
    print(api.modify_queue(name='all2.q', data={'load_thresholds': 'np_load_avg=1.65'}).to_json())
    # api.delete_queue('all2.q')
    queue_list = api.list_queues()
    print('QUEUE LIST: ', queue_list)
    print('QUEUE LIST JSON: ', queue_list.to_json())

    # ehosts = api.get_ehosts()
    # api.mk_ehosts_dir('/tmp/uge/ehosts')
    # api.write_ehosts(ehosts, '/tmp/uge/ehosts')

    # prjs = api.get_prjs()
    # api.mk_prjs_dir('/tmp/uge/proj')
    # api.write_prjs(prjs, '/tmp/uge/proj')

    # api.add_ehosts_from_dir('/tmp/uge/ehosts')
    # api.modify_ehosts_from_dir('/tmp/uge/ehosts')
    # api.delete_ehosts(['passat', 'elmsfeuer', 'kugelblitz'])

    # api.add_prjs_from_dir('/tmp/uge/proj')
    # api.modify_prjs_from_dir('/tmp/uge/proj')
    # api.delete_prjs(['test1', 'test2', 'test3', 'test4'])

    # api.rm_ehosts_dir('/tmp/uge/ehosts')
    # api.rm_prjs_dir('/tmp/uge/prjs')
