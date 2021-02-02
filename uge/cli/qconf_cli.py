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
from __future__ import print_function
import abc
import logging
import os
import sys
from optparse import OptionGroup
from optparse import OptionParser

from uge.config.config_manager import ConfigManager
from uge.exceptions.invalid_argument import InvalidArgument
from uge.exceptions.qconf_exception import QconfException
from uge.log.log_manager import LogManager
# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

class QconfCli(ABC):
    """ Base qconf command line interface class. """

    def __init__(self, valid_arg_count=0):
        """ 
        Class constructor.

        :param valid_arg_count: Number of allowed positional arguments (default: 0).
        :type valid_arg_count: int
        """
        self.logger = LogManager.get_instance().get_logger(self.__class__.__name__)
        self.parser = OptionParser(add_help_option=False)
        self.options = {}
        self.args = []
        self.valid_arg_count = valid_arg_count
        self.option_group_dict = {}

        common_group = 'Common Options'
        self.add_option_group(common_group, None)

        self.add_option_to_group(common_group, '-h', '--help', action='help', help='Show this help message and exit.')
        self.add_option_to_group(common_group, '-?', '', action='help', help='Show this help message and exit.')

        self.add_option_to_group(common_group, '-v', '', action='store_true', dest='cmd_version', default=False,
                                 help='Print version and exit.')

        self.add_option_to_group(common_group, '-d', '--debug', dest='console_log_level',
                                 help='Set debug level; valid values are: critical, error, warning, info, debug')

    def add_option(self, *args, **kwargs):
        """ 
        Add CLI option. 
        """
        self.parser.add_option(*args, **kwargs)

    def add_option_to_group(self, group_name, *args, **kwargs):
        """
        Add option to the given group.
        Group should be created using add_option_group().

        :param group_name: Group name.
        :type group_name: str
        """
        group = self.option_group_dict.get(group_name)
        group.add_option(*args, **kwargs)

    def add_option_group(self, group_name, desc):
        """ 
        Add option group. 

        :param group_name: Group name.
        :type group_name: str
        """
        group = OptionGroup(self.parser, group_name, desc)
        self.parser.add_option_group(group)
        self.option_group_dict[group_name] = group

    def parse_args(self, usage=None):
        """ 
        Parse command arguments. 

        :param usage: Command usage.
        :type usage: str
        """
        if usage:
            self.parser.usage = usage

        try:
            (self.options, self.args) = self.parser.parse_args()
        except SystemExit as rc:
            sys.stdout.flush()
            sys.stderr.flush()
            os._exit(int(str(rc)))

        if self.valid_arg_count < len(self.args):
            # Postitional args are not enabled and we have some
            msg = "Invalid Argument(s):"
            for arg in self.args[self.valid_arg_count:]:
                msg += " " + arg
            raise InvalidArgument(msg)

        opt_dict = self.options.__dict__
        if opt_dict.get('cmd_version'):
            print('%s version: %s' % (os.path.basename(sys.argv[0]), ConfigManager.get_instance().get_version()))
            os._exit(0)

        # Log level.
        console_log_level = opt_dict.get('console_log_level', None)
        if console_log_level:
            LogManager.get_instance().set_console_log_level(console_log_level)

        # Check input arguments.
        self.check_input_args()
        return (self.options, self.args)

    def usage(self, s=None):
        """ Print the help provided by optparse. """

        if s: print('Error:', s, '\n', file=sys.stderr)
        self.parser.print_help()
        os._exit(1)

    def get_options(self):
        """ Returns the command line options. """
        return self.options

    def get_n_args(self):
        """ Returns the number of command line arguments. """
        return len(self.args)

    def get_args(self):
        """ Returns the command line argument list. """
        return self.args

    def get_arg(self, i):
        """ Returns the i-th command line argument. """
        return self.args[i]

    @abc.abstractmethod
    def run_command(self):
        """ This method must be implemented by the derived class. """
        pass

    def check_input_args(self):
        """ 
        This method should verify required arguments in the derived class.
        """
        pass

    def run(self):
        """
        Run command. This method simply invokes run_command() and handles
        any exceptions.
        """
        try:
            self.run_command()
        except QconfException as ex:
            if self.logger.level < logging.INFO:
                self.logger.exception('%s' % ex)
            print('%s' % ex.get_error_message())
            raise SystemExit(ex.get_error_code())
        except SystemExit as ex:
            raise
        except Exception as ex:
            self.logger.exception('%s' % ex)
            print('%s' % ex)
            raise SystemExit(-1)


#############################################################################
# Testing.
if __name__ == '__main__':
    cli = QconfCli()
    cli.add_option("-f", "--file", dest="filename",
                   help="write report to FILE", metavar="FILE")
    cli.add_option("-q", "--quiet",
                   action="store_false", dest="verbose", default=True,
                   help="don't print status messages to stdout")
    (options, args) = cli.parse_args()
    print('OPTIONS: ', options)
    print('ARGS: ', args)

    print('OPTIONS: ', cli.get_options())
    print('ARGS: ', cli.get_args())
    print('options.filename', options.filename)
    print('cli.getOptions().filename', cli.get_options().filename)
    o = cli.get_options()
    print('o.filename', o.filename)

    print('cli.get_args()', cli.get_args())
    print('len(cli.get_args())', len(cli.get_args()))

    for a in cli.get_args():
        print('arg', a)

    first_arg = cli.get_arg(0)
    print('first_arg', first_arg)

    second_arg = cli.get_arg(1)
    print('second_arg', second_arg)

    try:
        third_arg = cli.get_arg(2)
        print('third_arg', third_arg)
    except:
        print('no third arg')
