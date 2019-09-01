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
import re
import os
import tempfile
from uge.utility.uge_subprocess import UgeSubprocess
from uge.log.log_manager import LogManager
from uge.exceptions.ar_exception import AdvanceReservationException
from uge.exceptions.command_failed import CommandFailed
from uge.exceptions.qmaster_unreachable import QmasterUnreachable
from uge.exceptions.authorization_error import AuthorizationError
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists


class QrsubExecutor(object):
    QRSUB_ERROR_REGEX_LIST = [
        (re.compile('.*unable to send message to qmaster.*'), QmasterUnreachable),
        (re.compile('.*must be manager.*'), AuthorizationError),
        (re.compile('denied.*'), AuthorizationError),
        (re.compile('.*does not exist.*'), ObjectNotFound),
        (re.compile('.*no.*defined.*'), ObjectNotFound),
        (re.compile('.*'), AdvanceReservationException)
    ]
    QRSUB_SUCCESS_REGEX_LIST = []  # for successful outcome incorrectly classified as failure
    QRSUB_FAILURE_REGEX_LIST = []  # for failure incorrectly classified as successful outcome

    def __init__(self, sge_root, sge_cell, sge_qmaster_port, sge_execd_port):
        self.logger = LogManager.get_instance().get_logger(self.__class__.__name__)
        self.env_dict = {
            'SGE_ROOT': sge_root,
            'SGE_CELL': sge_cell,
            'SGE_QMASTER_PORT': str(sge_qmaster_port),
            'SGE_EXECD_PORT': str(sge_execd_port),
            'SGE_SINGLE_LINE': '1',
        }
        self.uge_version = None
        self.__configure()

    def __configure(self):
        self.logger.trace('Retrieving UGE version')
        uge_version = self.get_uge_version()
        self.logger.debug('UGE version: %s' % uge_version)

    def get_uge_version(self):
        if not self.uge_version:
            p = self.execute_qrsub('-help')
            lines = p.get_stdout().split('\n')
            if not len(lines):
                raise AdvanceReservationException('Cannot determine UGE version from output: %s' % p.get_stdout())
            self.uge_version = lines[0].split()[-1].split("_")[0]
        return self.uge_version

    def execute_qrsub(self, cmd, error_regex_list=[], error_details=None, combine_error_lines=False,
                      success_regex_list=[], failure_regex_list=[]):
        try:
            command = '. %s/%s/common/settings.sh; qrsub %s' % (
            self.env_dict['SGE_ROOT'], self.env_dict['SGE_CELL'], cmd)
            p = UgeSubprocess(command, env=self.env_dict)
            p.run()

            # In some cases successful outcome is actually a failure
            error = p.get_stderr()
            if error:
                for (pattern, qrsubExClass) in failure_regex_list + QrsubExecutor.QRSUB_FAILURE_REGEX_LIST:
                    if pattern.match(error):
                        raise qrsubExClass(error, error_details=error_details)
            return p
        except CommandFailed as ex:
            error = str(ex)
            if combine_error_lines:
                error = error.replace('\n', '; ')
            for (pattern, result) in success_regex_list + QrsubExecutor.QRSUB_SUCCESS_REGEX_LIST:
                if pattern.match(error):
                    self.logger.debug(
                        'Ignoring command failed for success pattern, replacing stdout with result: "%s"' % result)
                    p.stdout_ = result
                    return p
            for (pattern, qrsubExClass) in error_regex_list + QrsubExecutor.QRSUB_ERROR_REGEX_LIST:
                if pattern.match(error):
                    raise qrsubExClass(error, error_details=error_details)
            raise

    def request_ar(self, args):
        p = self.execute_qrsub(args);
        lines = p.get_stdout()
        print(lines)
        result = re.findall(r'\d+', lines)
        print(result[0])
        return result[0]


#############################################################################
# Testing.
if __name__ == '__main__':
    from uge.exceptions.command_failed import CommandFailed

    executor = QrsubExecutor()
    try:
        print('Version: ', executor.get_uge_version())

        p = executor.execute_qrsub('-help')
        print(p.get_stdout())
        print(p.get_exit_status())
    except CommandFailed as ex:
        print('Exit Status: ', ex.get_command_exit_status())
        print('Std Error  : ', ex.get_command_stderr())
