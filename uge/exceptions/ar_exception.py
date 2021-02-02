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
try:
    import exceptions
except ImportError:
    import builtins as exceptions
import json

from uge.constants import uge_status


class AdvanceReservationException(exceptions.Exception):
    """
    Base Qrdel exception class. 

    Error code: uge_status.UGE_ERROR

    Usage examples:
    
    >>> raise AdvanceReservationException(error_message, error_code)
  
    >>> raise AdvanceReservationException(args=error_message)

    >>> raise AdvanceReservationException(exception=exception_object)
    """

    def __init__(self, error='', error_code=uge_status.UGE_ERROR, **kwargs):
        """ 
        Class constructor. 

        :param error: Error message.
        :type error: str

        :param error_code: Error code.
        :type error_code: int

        :param kwargs: Keyword arguments, may contain 'args=error_message', 'exception=exception_object', or 'error_details=details'.
        """
        args = error
        if args == '':
            args = kwargs.get('args', '')
        ex = kwargs.get('exception', None)
        if ex is not None and isinstance(ex, exceptions.Exception):
            ex_args = "%s" % (ex)
            if args == '':
                args = ex_args
            else:
                args = "%s (%s)" % (args, ex_args)
        exceptions.Exception.__init__(self, args)
        self.error_code = error_code
        self.error_details = kwargs.get('error_details', None)

    def get_args(self):
        """ 
        :returns: Exception arguments. 
        """
        return self.args

    def get_error_code(self):
        """ 
        :returns: Exception error code. 
        """
        return self.error_code

    def get_error_message(self):
        """ 
        :returns: Exception error message. 
        """
        return "%s" % (self.args)

    def get_error_details(self):
        """ 
        :returns: Exception error details. 
        """
        return "%s" % (self.error_details)

    def to_dict(self):
        """ 
        :returns: Exception data dictionary.
        """
        return {'error_message': '%s' % self.args,
                'error_code': self.error_code,
                'error_details': self.error_details,
                'class_name': self.__class__.__name__}

    def to_json(self):
        """ 
        :returns: JSON string with exception data.
        """
        return json.dumps(self.to_dict())
