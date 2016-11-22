.. automodule:: uge.exceptions

.. currentmodule:: uge.exceptions

QconfException
--------------

.. autoexception:: uge.exceptions.QconfException()
    :members: __init__, to_json, to_dict, get_error_code, get_error_message, get_args, get_error_details
    :show-inheritance:


AuthorizationError
------------------

.. autoexception:: uge.exceptions.AuthorizationError()
    :members: __init__
    :show-inheritance:

CommandFailed
-------------

.. autoexception:: uge.exceptions.CommandFailed()
    :members: __init__, get_command_stdout, get_command_stderr, get_command_exit_status
    :show-inheritance:

ConfigurationError
------------------

.. autoexception:: uge.exceptions.ConfigurationError()
    :members: __init__
    :show-inheritance:

InvalidArgument
---------------

.. autoexception:: uge.exceptions.InvalidArgument()
    :members: __init__
    :show-inheritance:

InvalidRequest
--------------

.. autoexception:: uge.exceptions.InvalidRequest()
    :members: __init__
    :show-inheritance:

ObjectAlreadyExists
-------------------

.. autoexception:: uge.exceptions.ObjectAlreadyExists()
    :members: __init__
    :show-inheritance:

ObjectNotFound
--------------

.. autoexception:: uge.exceptions.ObjectNotFound()
    :members: __init__
    :show-inheritance:

QmasterUnreachable
------------------

.. autoexception:: uge.exceptions.QmasterUnreachable()
    :members: __init__
    :show-inheritance:

