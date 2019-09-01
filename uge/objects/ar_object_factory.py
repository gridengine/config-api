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
import imp
import json

from uge.exceptions.ar_exception import AdvanceReservationException
from uge.exceptions.invalid_request import InvalidRequest
from .uge_release_object_map import UGE_RELEASE_OBJECT_MAP


class AdvanceReservationObjectFactory(object):

    @classmethod
    def __get_object_base_module_name(cls, class_name):
        # This method relies on convention: 
        #     ResourceQuotaSet=>resource_quota_set
        base_module_name = class_name[0].lower()
        for letter in class_name[1:]:
            if letter.isupper():
                base_module_name += '_%s' % letter.lower()
            else:
                base_module_name += letter
        return base_module_name

    @classmethod
    def __get_object_class_from_uge_version(cls, uge_version, class_name, base_module_name=None):
        if not uge_version:
            raise InvalidRequest('Cannot generate %s object: UGE version must be specified.' % class_name)
        if uge_version not in UGE_RELEASE_OBJECT_MAP:
            raise AdvanceReservationException('Unsupported UGE version: %s.' % uge_version)
        release_map = UGE_RELEASE_OBJECT_MAP.get(uge_version)
        object_version = release_map.get(class_name)
        return cls.__get_object_class_from_object_version(object_version, class_name, base_module_name)

    @classmethod
    def __get_object_class_from_object_version(cls, object_version, class_name, base_module_name=None):
        if not object_version:
            raise InvalidRequest('Object version not supplied for class %s.' % (class_name))

        if base_module_name is None:
            base_module_name = cls.__get_object_base_module_name(class_name)

        module_name = ('%s_v%s' % (base_module_name, object_version)).replace('.', '_')
        module_file = '%s/%s.py' % ('/'.join(__file__.split('/')[:-1]), module_name)
        module = imp.load_source('uge.objects.%s' % module_name, module_file)
        object_class = getattr(module, class_name)
        return object_class

    @classmethod
    def __generate_object(cls, object_class, name, data, metadata, json_string, add_required_data):
        generated_object = object_class(name=name, data=data, metadata=metadata, json_string=json_string)
        if add_required_data:
            generated_object.update_with_required_data_defaults()
        return generated_object

    @classmethod
    def generate_object(cls, json_string, target_uge_version=None):
        object_dict = json.loads(json_string)
        class_name = object_dict['object_class']
        object_version = object_dict['object_version']
        object_class = cls.__get_object_class_from_object_version(object_version, class_name)
        generated_object = object_class(json_string=json_string)
        generated_object.update_with_required_data_defaults()
        if target_uge_version:
            object_class = cls.__get_object_class_from_uge_version(target_uge_version, class_name)
            generated_object = object_class(json_string=generated_object.to_json())
            generated_object.update_with_required_data_defaults()
        return generated_object

    @classmethod
    def generate_advance_reservation(cls, uge_version, name=None, data=None, metadata=None, json_string=None,
                                     add_required_data=True):
        advance_reservation_class = cls.__get_object_class_from_uge_version(uge_version, 'AdvanceReservation')
        advance_reservation = advance_reservation_class(name=name, data=data, metadata=metadata,
                                                        json_string=json_string)
        if add_required_data:
            advance_reservation.update_with_required_data_defaults()
        return advance_reservation


#############################################################################
# Testing.
if __name__ == '__main__':
    print(__file__)
    module_file = '%s/%s.py' % ('/'.join(__file__.split('/')[:-1]), 'advance_reservation_v1_0')
    print(module_file)
    module = imp.load_source('uge.objects.advance_reservation_v1_0', module_file)
    print(module)
    print(getattr(module, 'AdvanceReservation'))
    ar = AdvanceReservationObjectFactory.generate_advance_reservation('8.6.0')
    print(ar)
    print(ar.VERSION)
