.. automodule:: uge.objects

.. currentmodule:: uge.objects

QconfObject
-----------

.. autoclass:: uge.objects.qconf_object.QconfObject()
    :members: __init__,
              check_user_provided_keys, remove_optional_keys, 
              update_with_required_data_defaults, to_uge, to_json,
              set_get_metadata, set_modify_metadata, set_add_metadata
    :show-inheritance:

QconfDictList
-------------

.. autoclass:: uge.objects.qconf_dict_list.QconfDictList()
    :members: __init__,
              check_user_provided_keys, update_with_required_data_defaults,
              to_uge
    :show-inheritance:

QconfNameList
-------------

.. autoclass:: uge.objects.qconf_name_list.QconfNameList()
    :members: __init__
    :show-inheritance:

AccessList v1.0
---------------

.. autoclass:: uge.objects.access_list_v1_0.AccessList()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.access_list_v1_0.AccessList.VERSION 
    .. autoattribute:: uge.objects.access_list_v1_0.AccessList.NAME_KEY
    .. autoattribute:: uge.objects.access_list_v1_0.AccessList.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.access_list_v1_0.AccessList.REQUIRED_DATA_DEFAULTS

Calendar v1.0
-------------

.. autoclass:: uge.objects.calendar_v1_0.Calendar()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.calendar_v1_0.Calendar.VERSION 
    .. autoattribute:: uge.objects.calendar_v1_0.Calendar.NAME_KEY
    .. autoattribute:: uge.objects.calendar_v1_0.Calendar.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.calendar_v1_0.Calendar.REQUIRED_DATA_DEFAULTS

CheckpointingEnvironment v1.0
-----------------------------

.. autoclass:: uge.objects.checkpointing_environment_v1_0.CheckpointingEnvironment()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.checkpointing_environment_v1_0.CheckpointingEnvironment.VERSION 
    .. autoattribute:: uge.objects.checkpointing_environment_v1_0.CheckpointingEnvironment.NAME_KEY
    .. autoattribute:: uge.objects.checkpointing_environment_v1_0.CheckpointingEnvironment.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.checkpointing_environment_v1_0.CheckpointingEnvironment.REQUIRED_DATA_DEFAULTS

ClusterConfiguration v1.0
-------------------------

.. autoclass:: uge.objects.cluster_configuration_v1_0.ClusterConfiguration()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.cluster_configuration_v1_0.ClusterConfiguration.VERSION 
    .. autoattribute:: uge.objects.cluster_configuration_v1_0.ClusterConfiguration.NAME_KEY
    .. autoattribute:: uge.objects.cluster_configuration_v1_0.ClusterConfiguration.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.cluster_configuration_v1_0.ClusterConfiguration.REQUIRED_GLOBAL_DATA_DEFAULTS
    .. autoattribute:: uge.objects.cluster_configuration_v1_0.ClusterConfiguration.REQUIRED_HOST_DATA_DEFAULTS

ClusterConfiguration v2.0
-------------------------

.. autoclass:: uge.objects.cluster_configuration_v2_0.ClusterConfiguration()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.cluster_configuration_v2_0.ClusterConfiguration.VERSION 
    .. autoattribute:: uge.objects.cluster_configuration_v2_0.ClusterConfiguration.NAME_KEY
    .. autoattribute:: uge.objects.cluster_configuration_v2_0.ClusterConfiguration.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.cluster_configuration_v2_0.ClusterConfiguration.REQUIRED_GLOBAL_DATA_DEFAULTS
    .. autoattribute:: uge.objects.cluster_configuration_v2_0.ClusterConfiguration.REQUIRED_HOST_DATA_DEFAULTS

ClusterQueue v1.0
-----------------

.. autoclass:: uge.objects.cluster_queue_v1_0.ClusterQueue()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.cluster_queue_v1_0.ClusterQueue.VERSION 
    .. autoattribute:: uge.objects.cluster_queue_v1_0.ClusterQueue.NAME_KEY
    .. autoattribute:: uge.objects.cluster_queue_v1_0.ClusterQueue.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.cluster_queue_v1_0.ClusterQueue.REQUIRED_DATA_DEFAULTS

ComplexConfigurationBase
------------------------

.. autoclass:: uge.objects.complex_configuration_base.ComplexConfigurationBase()
    :members: __init__
    :show-inheritance:

ComplexConfiguration v1.0
-------------------------

.. autoclass:: uge.objects.complex_configuration_v1_0.ComplexConfiguration()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.complex_configuration_v1_0.ComplexConfiguration.VERSION 
    .. autoattribute:: uge.objects.complex_configuration_v1_0.ComplexConfiguration.NAME_KEY
    .. autoattribute:: uge.objects.complex_configuration_v1_0.ComplexConfiguration.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.complex_configuration_v1_0.ComplexConfiguration.REQUIRED_DATA_DEFAULTS

ComplexConfiguration v2.0
-------------------------

.. autoclass:: uge.objects.complex_configuration_v2_0.ComplexConfiguration()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.complex_configuration_v2_0.ComplexConfiguration.VERSION 
    .. autoattribute:: uge.objects.complex_configuration_v2_0.ComplexConfiguration.NAME_KEY
    .. autoattribute:: uge.objects.complex_configuration_v2_0.ComplexConfiguration.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.complex_configuration_v2_0.ComplexConfiguration.REQUIRED_DATA_DEFAULTS

ExecutionHost v1.0
------------------

.. autoclass:: uge.objects.execution_host_v1_0.ExecutionHost()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.execution_host_v1_0.ExecutionHost.VERSION 
    .. autoattribute:: uge.objects.execution_host_v1_0.ExecutionHost.NAME_KEY
    .. autoattribute:: uge.objects.execution_host_v1_0.ExecutionHost.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.execution_host_v1_0.ExecutionHost.REQUIRED_DATA_DEFAULTS

HostGroup v1.0
--------------

.. autoclass:: uge.objects.host_group_v1_0.HostGroup()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.host_group_v1_0.HostGroup.VERSION
    .. autoattribute:: uge.objects.host_group_v1_0.HostGroup.NAME_KEY
    .. autoattribute:: uge.objects.host_group_v1_0.HostGroup.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.host_group_v1_0.HostGroup.REQUIRED_DATA_DEFAULTS

JobClass v1.0
-------------

.. autoclass:: uge.objects.job_class_v1_0.JobClass()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.job_class_v1_0.JobClass.VERSION
    .. autoattribute:: uge.objects.job_class_v1_0.JobClass.NAME_KEY
    .. autoattribute:: uge.objects.job_class_v1_0.JobClass.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.job_class_v1_0.JobClass.REQUIRED_DATA_DEFAULTS

JobClass v2.0
-------------

.. autoclass:: uge.objects.job_class_v2_0.JobClass()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.job_class_v2_0.JobClass.VERSION
    .. autoattribute:: uge.objects.job_class_v2_0.JobClass.NAME_KEY
    .. autoattribute:: uge.objects.job_class_v2_0.JobClass.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.job_class_v2_0.JobClass.REQUIRED_DATA_DEFAULTS

JobClass v3.0
-------------

.. autoclass:: uge.objects.job_class_v3_0.JobClass()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.job_class_v3_0.JobClass.VERSION
    .. autoattribute:: uge.objects.job_class_v3_0.JobClass.NAME_KEY
    .. autoattribute:: uge.objects.job_class_v3_0.JobClass.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.job_class_v3_0.JobClass.REQUIRED_DATA_DEFAULTS

ParallelEnvironment v1.0
------------------------

.. autoclass:: uge.objects.parallel_environment_v1_0.ParallelEnvironment()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.parallel_environment_v1_0.ParallelEnvironment.VERSION
    .. autoattribute:: uge.objects.parallel_environment_v1_0.ParallelEnvironment.NAME_KEY
    .. autoattribute:: uge.objects.parallel_environment_v1_0.ParallelEnvironment.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.parallel_environment_v1_0.ParallelEnvironment.REQUIRED_DATA_DEFAULTS

ParallelEnvironment v2.0
------------------------

.. autoclass:: uge.objects.parallel_environment_v2_0.ParallelEnvironment()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.parallel_environment_v2_0.ParallelEnvironment.VERSION
    .. autoattribute:: uge.objects.parallel_environment_v2_0.ParallelEnvironment.NAME_KEY
    .. autoattribute:: uge.objects.parallel_environment_v2_0.ParallelEnvironment.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.parallel_environment_v2_0.ParallelEnvironment.REQUIRED_DATA_DEFAULTS

Project v1.0
------------

.. autoclass:: uge.objects.project_v1_0.Project()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.project_v1_0.Project.VERSION 
    .. autoattribute:: uge.objects.project_v1_0.Project.NAME_KEY
    .. autoattribute:: uge.objects.project_v1_0.Project.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.project_v1_0.Project.REQUIRED_DATA_DEFAULTS

ResourceQuotaSet v1.0
---------------------

.. autoclass:: uge.objects.resource_quota_set_v1_0.ResourceQuotaSet()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.resource_quota_set_v1_0.ResourceQuotaSet.VERSION 
    .. autoattribute:: uge.objects.resource_quota_set_v1_0.ResourceQuotaSet.NAME_KEY
    .. autoattribute:: uge.objects.resource_quota_set_v1_0.ResourceQuotaSet.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.resource_quota_set_v1_0.ResourceQuotaSet.REQUIRED_DATA_DEFAULTS

SchedulerConfiguration v1.0
---------------------------

.. autoclass:: uge.objects.scheduler_configuration_v1_0.SchedulerConfiguration()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.scheduler_configuration_v1_0.SchedulerConfiguration.VERSION 
    .. autoattribute:: uge.objects.scheduler_configuration_v1_0.SchedulerConfiguration.NAME_KEY
    .. autoattribute:: uge.objects.scheduler_configuration_v1_0.SchedulerConfiguration.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.scheduler_configuration_v1_0.SchedulerConfiguration.REQUIRED_DATA_DEFAULTS

SchedulerConfiguration v2.0
---------------------------

.. autoclass:: uge.objects.scheduler_configuration_v2_0.SchedulerConfiguration()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.scheduler_configuration_v2_0.SchedulerConfiguration.VERSION 
    .. autoattribute:: uge.objects.scheduler_configuration_v2_0.SchedulerConfiguration.NAME_KEY
    .. autoattribute:: uge.objects.scheduler_configuration_v2_0.SchedulerConfiguration.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.scheduler_configuration_v2_0.SchedulerConfiguration.REQUIRED_DATA_DEFAULTS

ShareTree v1.0
--------------

.. autoclass:: uge.objects.share_tree_v1_0.ShareTree()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.share_tree_v1_0.ShareTree.VERSION 
    .. autoattribute:: uge.objects.share_tree_v1_0.ShareTree.FIRST_KEY
    .. autoattribute:: uge.objects.share_tree_v1_0.ShareTree.NAME_KEY
    .. autoattribute:: uge.objects.share_tree_v1_0.ShareTree.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.share_tree_v1_0.ShareTree.REQUIRED_DATA_DEFAULTS

User v1.0
---------

.. autoclass:: uge.objects.user_v1_0.User()
    :members: __init__
    :show-inheritance:

    .. autoattribute:: uge.objects.user_v1_0.User.VERSION 
    .. autoattribute:: uge.objects.user_v1_0.User.NAME_KEY
    .. autoattribute:: uge.objects.user_v1_0.User.USER_PROVIDED_KEYS
    .. autoattribute:: uge.objects.user_v1_0.User.REQUIRED_DATA_DEFAULTS

