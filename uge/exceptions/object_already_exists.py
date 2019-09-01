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


class ObjectAlreadyExists(QconfException):
    """ 
    Object not found error class.

    Error code: uge_status.UGE_OBJECT_ALREADY_EXISTS
    """

    def __init__(self, error='', **kwargs):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str

        :param kwargs: Keyword arguments, may contain 'args=error_message', 'exception=exception_object', or 'error_details=details'.
        """
        QconfException.__init__(
            self, error, uge_status.UGE_OBJECT_ALREADY_EXISTS,
            **kwargs)
