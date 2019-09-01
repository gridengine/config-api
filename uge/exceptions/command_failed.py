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

from uge.exceptions.qconf_exception import QconfException
from uge.constants import uge_status


class CommandFailed(QconfException):
    """ 
    Command failed error class.

    Error code: uge_status.UGE_COMMAND_FAILED
    """

    def __init__(self, error='', command_stdout=None, command_stderr=None, command_exit_status=None, **kwargs):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str

        :param command_stdout: Command standard output.
        :type command_stdout: str

        :param command_stderr: Command standard error.
        :type command_stderr: str

        :param command_exit_status: Command exit status.
        :type command_exit_status: int

        :param kwargs: Keyword arguments, may contain 'args=error_message', 'exception=exception_object', or 'error_details=details'.
        """
        QconfException.__init__(
            self, error, uge_status.UGE_COMMAND_FAILED,
            **kwargs)
        self.command_stdout = command_stdout
        self.command_stderr = command_stderr
        self.command_exit_status = command_exit_status

    def get_command_stdout(self):
        """
        :returns: Command standard output.
        """
        return self.command_stdout

    def get_command_stderr(self):
        """
        :returns: Command standard error.
        """
        return self.command_stderr

    def get_command_exit_status(self):
        """
        :returns: Command exit status.
        """
        return self.command_exit_status
