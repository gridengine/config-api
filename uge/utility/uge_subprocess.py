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
import os
import subprocess

from uge.log.log_manager import LogManager
from uge.exceptions.command_failed import CommandFailed


class UgeSubprocess(subprocess.Popen):

    def __init__(self, args, bufsize=0, executable=None, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                 preexec_fn=None, close_fds=False, shell=True, cwd=None, env=None, universal_newlines=False,
                 startupinfo=None, creationflags=0, use_exceptions=True):
        """
        Overrides Popen constructor with defaults more appropriate for
        Uge usage.
        """
        subprocess.Popen.__init__(self, args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell,
                                  cwd, env, universal_newlines, startupinfo, creationflags)
        self.logger = LogManager.get_instance().get_logger(self.__class__.__name__)
        self.stdout_ = None
        self.stderr_ = None
        self.args_ = args
        self.use_exceptions = use_exceptions

    def __command_log(self):
        # Not very useful to show the name of this file.
        # Walk up the stack to find the caller.
        import traceback
        stack = traceback.extract_stack()
        for i in range(2, len(stack)):
            if stack[-i][0] != stack[-1][0]:
                fileName, lineNumber, functionName, text = stack[-i]
                break
        else:
            fileName = lineNumber = functionName = text = '?'

        self.logger.debug('from [%s:%s] Invoking: [%s]' %
                          (os.path.basename(fileName), lineNumber, self.args_))

    def run(self, input=None):
        self.__command_log()
        (self.stdout_, self.stderr_) = subprocess.Popen.communicate(self, input)
        self.logger.debug('Exit status: %s' % self.returncode)
        if self.returncode != 0 and self.use_exceptions:
            self.logger.debug('StdOut: %s' % self.stdout_.decode())
            self.logger.debug('StdErr: %s' % self.stderr_.decode())
            raise CommandFailed(self.stderr_.decode(), self.stdout_.decode(), self.stderr_.decode(), self.returncode)
        return self.stdout_.decode(), self.stderr_.decode()

    def get_logger(self):
        return self.logger

    def get_args(self):
        return self.args_

    def get_stdout(self):
        return self.stdout_.decode()

    def get_stderr(self):
        return self.stderr_.decode()

    def get_exit_status(self):
        return self.returncode

    @classmethod
    def execute(cls, command):
        """ Create subprocess and run it, return subprocess object. """
        p = UgeSubprocess(command)
        p.run()
        return p

    @classmethod
    def execute_and_ignore_failure(cls, command):
        """ 
        Create subprocess, run it, ignore failures, return subprocess object. 
        """
        p = UgeSubprocess(command)
        try:
            p.run()
        except CommandFailed as ex:
            p.get_logger().debug('Command failed, stdout: %s, stderr: %s' % (p.get_stdout(), p.get_stderr()))
        return p

    @classmethod
    def execute_and_log_to_stdout(cls, command):
        """
        Executes command, displays output to stdout and maintains log file.
        Returns subprocess object
        """
        p = UgeSubprocess(command)
        while True:
            outp = p.stdout.readline()
            if not outp:
                break
            # print(outp, end=' ')
            print(outp)
        retval = p.wait()

        p.logger.debug('Exit status: %s' % retval)

        if retval != 0:
            emsg = ''
            while True:
                err = p.stderr.readline()
                if not err:
                    break
                emsg += err
            raise CommandFailed(emsg)

        return p


#############################################################################
# Testing.
if __name__ == '__main__':
    p = UgeSubprocess('ls -l', use_exceptions=False)
    # print(p.run())
    p.run()
    print(p.get_stdout())
    print(p.get_stderr())
    print(p.get_exit_status())
