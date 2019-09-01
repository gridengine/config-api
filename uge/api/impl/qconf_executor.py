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
from uge.exceptions.qconf_exception import QconfException
from uge.exceptions.command_failed import CommandFailed
from uge.exceptions.qmaster_unreachable import QmasterUnreachable
from uge.exceptions.authorization_error import AuthorizationError
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists


class QconfExecutor(object):
    QCONF_ERROR_REGEX_LIST = [
        (re.compile('.*unable to send message to qmaster.*'), QmasterUnreachable),
        (re.compile('.*must be manager.*'), AuthorizationError),
        (re.compile('denied.*'), AuthorizationError),
        (re.compile('.*does not exist.*'), ObjectNotFound),
        (re.compile('.*no.*defined.*'), ObjectNotFound),
        (re.compile('.*'), QconfException)
    ]
    QCONF_SUCCESS_REGEX_LIST = []  # for successful outcome incorrectly classified as failure
    QCONF_FAILURE_REGEX_LIST = []  # for failure incorrectly classified as successful outcome

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
            p = self.execute_qconf('-help')
            lines = p.get_stdout().split('\n')
            if not len(lines):
                raise QconfException('Cannot determine UGE version from output: %s' % p.get_stdout())
            self.uge_version = lines[0].split()[-1].split("_")[0]
        return self.uge_version

    def execute_qconf(self, cmd, error_regex_list=[], error_details=None, combine_error_lines=False,
                      success_regex_list=[], failure_regex_list=[]):
        try:
            command = '. %s/%s/common/settings.sh; qconf %s' % (
            self.env_dict['SGE_ROOT'], self.env_dict['SGE_CELL'], cmd)
            p = UgeSubprocess(command, env=self.env_dict)
            p.run()

            # In some cases successful outcome is actually a failure
            error = p.get_stderr()
            if error:
                for (pattern, qconfExClass) in failure_regex_list + QconfExecutor.QCONF_FAILURE_REGEX_LIST:
                    if pattern.match(error):
                        raise qconfExClass(error, error_details=error_details)
            return p
        except CommandFailed as ex:
            error = str(ex)
            if combine_error_lines:
                error = error.replace('\n', '; ')
            for (pattern, result) in success_regex_list + QconfExecutor.QCONF_SUCCESS_REGEX_LIST:
                if pattern.match(error):
                    self.logger.debug(
                        'Ignoring command failed for success pattern, replacing stdout with result: "%s"' % result)
                    p.stdout_ = result
                    return p
            for (pattern, qconfExClass) in error_regex_list + QconfExecutor.QCONF_ERROR_REGEX_LIST:
                if pattern.match(error):
                    raise qconfExClass(error, error_details=error_details)
            raise

    def execute_qconf_with_object(self, cmd, qconf_object, error_regex_list=[]):
        try:
            # fd, tmp_file_path = tempfile.mkstemp(text=True)
            # tmp_file = os.fdopen(fd, 'w')
            tmp_file_path = None
            tmp_dir_path = None
            tmp_file, tmp_file_path, tmp_dir_path = qconf_object.get_tmp_file()
            tmp_file_content = qconf_object.to_uge()
            tmp_file.write(tmp_file_content)
            tmp_file.flush()
            tmp_file.close()
            full_cmd = '%s %s' % (cmd, tmp_file_path)
            error_details = 'Object configuration file content:\n%s' % tmp_file_content
            self.execute_qconf(full_cmd, error_regex_list=error_regex_list, error_details=error_details)
        finally:
            if tmp_file_path is not None:
                os.remove(tmp_file_path)
            if tmp_dir_path is not None:
                os.rmdir(tmp_dir_path)

    def execute_qconf_with_dir(self, cmd, dir, error_regex_list=[]):
        if not os.path.isdir(dir):
            raise QconfException('%s is not a directory' % dir)
        full_cmd = '%s %s' % (cmd, dir)
        self.execute_qconf(full_cmd, error_regex_list=error_regex_list)


#############################################################################
# Testing.
if __name__ == '__main__':
    from uge.exceptions.command_failed import CommandFailed

    sge_root = os.environ.get('SGE_ROOT')
    if not sge_root:
        raise ConfigurationError('SGE_ROOT is not defined.')
    sge_cell = os.environ.get('SGE_CELL', 'default')
    if not sge_cell:
        raise ConfigurationError('SGE_CELL is not defined.')
    sge_qmaster_port = os.environ.get('SGE_QMASTER_PORT')
    if not sge_qmaster_port:
        raise ConfigurationError('SGE_QMASTER_PORT is not defined.')
    sge_execd_port = os.environ.get('SGE_EXECD_PORT')
    if not sge_execd_port:
        raise ConfigurationError('SGE_EXECD_PORT is not defined.')

    print('Configuration: SGE_ROOT=%s, SGE_CELL=%s, SGE_QMASTER_PORT=%s, SGE_EXECD_PORT=%s' % (
    sge_root, sge_cell, sge_qmaster_port, sge_execd_port))
    executor = QconfExecutor(sge_root=sge_root, sge_cell=sge_cell,
                             sge_qmaster_port=sge_qmaster_port,
                             sge_execd_port=sge_qmaster_port)
    try:
        print('Version: ', executor.get_uge_version())

        p = executor.execute_qconf('-sq all.q')
        print(p.get_stdout())
        print(p.get_exit_status())
    except CommandFailed as ex:
        print('Exit Status: ', ex.get_command_exit_status())
        print('Std Error  : ', ex.get_command_stderr())
