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
try:
    import UserList
except ImportError:
    import collections as UserList
from uge.exceptions.invalid_argument import InvalidArgument
from .qconf_object import QconfObject


class QconfNameList(QconfObject, UserList.UserList):
    """ 
    This class represents list of names returned by various qconf commands. It supports
    all standard python list interfaces.
    """

    def __init__(self, name=None, data=None, metadata=None, json_string=None):
        """
        Class constructor. 

        :param name: List name. 
        :type name: str

        :param data: Name list data. If provided, it will override corresponding data from object's JSON string representation.
        :type data: list

        :param metadata: Name list metadata. If provided, it will override corresponding metadata from object's JSON string representation.
        :type metadata: dict

        :param json_string: Name list JSON string representation.
        :type json_string: str

        :raises: **InvalidArgument** - in case metadata is not a dictionary, JSON string is not valid, or it does not contain dictionary representing a QconfNameList object.
        """
        UserList.UserList.__init__(self)
        QconfObject.__init__(self, name=name, data=data, metadata=metadata, json_string=json_string)

    def check_input_data(self, data):
        if type(data) != list:
            raise InvalidArgument('Provided data is not a list: %s.' % str(data))

    def convert_data_to_uge_keywords(self, data):
        pass


#############################################################################
# Testing.
if __name__ == '__main__':
    name_list = QconfNameList(data=['xyz', 'abc'])
    print(name_list.__class__.__name__)
    name_list.append('admin1')
    name_list.append('admin2')
    print(name_list)
    for n in name_list:
        print('NAME: ', n)
