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
from uge.cli.qconf_cli import QconfCli
from uge.api.qconf_api import QconfApi
from uge.exceptions.invalid_request import InvalidRequest


class QconfConvert(QconfCli):
    """ Qconf upgrade command. """

    def __init__(self):
        QconfCli.__init__(self)
        self.api = QconfApi()
        self.add_option('', '--input-file', dest='input_file',
                        help='Input file containing object\'s JSON representation.')
        self.add_option('', '--to-uge', dest='target_uge_version', default=self.api.get_uge_version(),
                        help='Target UGE version (default: %s).' % self.api.get_uge_version())
        self.add_option('', '--output-format', dest='output_format', default='json',
                        help='Output format, either json or uge (default: json).')

    def check_input_args(self):
        if not self.options.input_file:
            raise InvalidRequest('Missing input file.')
        if self.options.output_format not in ['json', 'uge']:
            raise InvalidRequest('Output format may be either json or uge.')

    def run_command(self):
        self.parse_args("""
    qconf-convert --input-file=INPUT_FILE
        [--to-uge=TARGET_UGE_VERSION]
        [--output-format=OUTPUT_FORMAT]

Description:
    Converts Qconf object with a given JSON representation to equivalent object corresponding to the specified target UGE version. 
""")
        input_file = self.options.input_file
        target_uge_version = self.options.target_uge_version
        json_string = open(input_file).read()
        qconf_object = self.api.generate_object(json_string, target_uge_version)
        if self.options.output_format == 'json':
            print(qconf_object.to_json())
        else:
            print(qconf_object.to_uge())


#############################################################################
# Run command.
def run():
    cli = QconfConvert()
    cli.run()


if __name__ == '__main__':
    run()
