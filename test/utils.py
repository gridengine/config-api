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
import string
import random
import os
import os.path
import json
from tempfile import NamedTemporaryFile

from nose import SkipTest
from nose.tools import make_decorator

CONFIG_FILE = '/tmp/uge.test.conf'
LOG_FILE = '/tmp/uge.test.log'

CONFIG_FILE_TEMPLATE = """
[LoggerLevels]
root=error
expressions: ^.*$=trace

[ConsoleLogging]
handler=stream_log_handler.StreamLogHandler(sys.stdout,)
level=debug
format=%(asctime)s %(levelname)s %(process)d %(filename)s:%(lineno)d %(message)s
datefmt=%Y-%m-%d %H:%M:%S

[FileLogging]
handler=timed_rotating_file_log_handler.TimedRotatingFileLogHandler('LOG_FILE')
level=trace
format=%(asctime)s %(levelname)s %(process)d %(message)s
datefmt=%Y-%m-%d %H:%M:%S
"""


def create_config_file(use_temporary_file=False):
    config_file_name = CONFIG_FILE
    if use_temporary_file:
        config_file = NamedTemporaryFile(delete=False)
        config_file_name = config_file.name
    else:
        if os.path.exists(config_file_name):
            create_config_manager()
            return
        config_file = open(config_file_name, 'w')
    config_string = CONFIG_FILE_TEMPLATE.replace(
        'LOG_FILE', LOG_FILE)
    config_file.write(config_string)
    config_file.close()
    create_config_manager()
    return config_file_name


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def remove_test_log_file():
    remove_file(LOG_FILE)


def remove_test_config_file():
    remove_file(CONFIG_FILE)


def remove_test_files():
    remove_file(LOG_FILE)
    remove_file(CONFIG_FILE)


def read_last_line(file_path):
    f = open(file_path, 'r')
    last_line = None
    while True:
        line = f.readline()
        if not line:
            break
        last_line = line
    f.close()
    return last_line


def read_last_log_line():
    return read_last_line(LOG_FILE)


def create_config_manager():
    from uge.config.config_manager import ConfigManager
    cm = ConfigManager.get_instance()
    cm.set_config_file(CONFIG_FILE)
    cm.set_log_file(LOG_FILE)
    cm.set_file_log_level('trace')


def generate_random_string(size, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_random_string_list(n_strings, string_length, delimiter=',', string_prefix=''):
    string_list = ''
    string_delimiter = ''
    for i in range(0, n_strings):
        string_list = '%s%s%s%s' % (string_list, string_delimiter,
                                    string_prefix,
                                    generate_random_string(string_length))
        string_delimiter = delimiter
    return string_list


def load_values(value_file):
    tpd = {}
    if os.path.exists(value_file):
        tpd = json.load(open(value_file))
    return tpd


# Common decorators
def needs_setup(func):
    def inner(*args, **kwargs):
        create_config_file()
        return func(*args, **kwargs)

    return make_decorator(func)(inner)


def needs_cleanup(func):
    def inner(*args, **kwargs):
        remove_test_files()
        return func(*args, **kwargs)

    return make_decorator(func)(inner)


def needs_config(func):
    def inner(*args, **kwargs):
        try:
            create_config_manager()
        except Exception as ex:
            print(ex)
            raise SkipTest("Config manager instance could not be created.")
        return func(*args, **kwargs)

    return make_decorator(func)(inner)


def needs_uge(func):
    def inner(*args, **kwargs):
        from uge.exceptions.configuration_error import ConfigurationError
        if 'SGE_ROOT' not in os.environ:
            raise ConfigurationError('SGE_ROOT is not defined.')
        return func(*args, **kwargs)

    return make_decorator(func)(inner)


#############################################################################
# Testing
if __name__ == '__main__':
    # print 'Last line: ', read_last_line('/tmp/uge.log')
    create_config_file()
    d = load_values('test_values.json')
    print(d)
