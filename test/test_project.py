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
import types
import tempfile
from .utils import needs_uge
from .utils import generate_random_string
from .utils import create_config_file
from .utils import load_values

from uge.api.qconf_api import QconfApi
from uge.config.config_manager import ConfigManager
from uge.log.log_manager import LogManager
from uge.exceptions.object_not_found import ObjectNotFound
from uge.exceptions.object_already_exists import ObjectAlreadyExists

create_config_file()
API = QconfApi()
PROJECT_NAME = '%s' % generate_random_string(6)
CONFIG_MANAGER = ConfigManager.get_instance()
LOG_MANAGER = LogManager.get_instance()
VALUES_DICT = load_values('test_values.json')
print(VALUES_DICT)


@needs_uge
def test_object_not_found():
    try:
        project = API.get_prj('__non_existent_project__')
        assert (False)
    except ObjectNotFound as ex:
        # ok
        pass


def test_generate_prj():
    project = API.generate_prj(PROJECT_NAME)
    assert (project.data['name'] == PROJECT_NAME)


def test_add_prj():
    try:
        project_list = API.list_prjs()
    except ObjectNotFound as ex:
        # no projects defined
        project_list = []
    project = API.add_prj(name=PROJECT_NAME)
    assert (project.data['name'] == PROJECT_NAME)
    project_list2 = API.list_prjs()
    assert (len(project_list2) == len(project_list) + 1)
    assert (project_list2.count(PROJECT_NAME) == 1)


def test_list_prjs():
    project_list = API.list_prjs()
    assert (project_list is not None)


def test_object_already_exists():
    try:
        project = API.add_prj(name=PROJECT_NAME)
        assert (False)
    except ObjectAlreadyExists as ex:
        # ok
        pass


def test_get_prj():
    project = API.get_prj(PROJECT_NAME)
    assert (project.data['name'] == PROJECT_NAME)


def test_generate_prj_from_json():
    prj = API.get_prj(PROJECT_NAME)
    json = prj.to_json()
    prj2 = API.generate_object(json)
    assert (prj2.__class__.__name__ == prj.__class__.__name__)
    for key in list(prj.data.keys()):
        v = prj.data[key]
        v2 = prj2.data[key]
        if type(v) == list:
            assert (len(v) == len(v2))
            for s in v:
                assert (v2.count(s) == 1)
        elif type(v) == dict:
            for key in list(v.keys()):
                assert (str(v[key]) == str(v2[key]))
        else:
            assert (str(v) == str(v2))


def test_modify_prj():
    project = API.get_prj(PROJECT_NAME)
    oticket = project.data['oticket']
    project = API.modify_prj(name=PROJECT_NAME, data={'oticket': oticket + 1})
    oticket2 = project.data['oticket']
    assert (oticket2 == oticket + 1)


def test_delete_prj():
    project_list = API.list_prjs()
    API.delete_prj(PROJECT_NAME)
    try:
        project_list2 = API.list_prjs()
    except ObjectNotFound as ex:
        # no projects defined
        project_list2 = []
    assert (len(project_list2) == len(project_list) - 1)
    assert (project_list2.count(PROJECT_NAME) == 0)


def test_get_prjs():
    prjl = API.list_prjs()
    print("Project Names: " + prjl)
    prjs = API.get_prjs()
    print("Projects: " + str(prjs))
    for prj in prjs:
        print("#############################################")
        print(prj.to_uge())
        assert (prj.data['name'] in prjl)


def test_write_prjs():
    try:
        tdir = tempfile.mkdtemp()
        print("*************************** " + tdir)
        prjs = API.get_prjs()
        for prj in prjs:
            print("Before #############################################")
            print(prj.to_uge())

        new_prjs = []
        prj_names = VALUES_DICT['prj_names']
        for name in prj_names:
            nprj = API.generate_prj(name=name)
            new_prjs.append(nprj)
        API.mk_prjs_dir(tdir)
        API.write_prjs(new_prjs, tdir)
        API.add_prjs_from_dir(tdir)
        API.modify_prjs_from_dir(tdir)
        prjs = API.get_prjs()
        for prj in prjs:
            print("After #############################################")
            print(prj.to_uge())

        prjs = API.list_prjs()
        for name in prj_names:
            assert (name in prjs)
            print("project found: " + name)

    finally:
        API.delete_prjs(prj_names)
        API.rm_prjs_dir(tdir)


def test_add_prjs():
    try:
        new_prjs = []
        prj_names = VALUES_DICT['prj_names']
        for name in prj_names:
            nprj = API.generate_prj(name=name)
            new_prjs.append(nprj)

        # print all projects currently in the cluster
        prjs = API.get_prjs()
        for prj in prjs:
            print("Before #############################################")
            print(prj.to_uge())

        # add projects
        API.add_prjs(new_prjs)
        API.modify_prjs(new_prjs)

        # print all projects currently in the cluster
        prjs = API.get_prjs()
        for prj in prjs:
            print("After #############################################")
            print(prj.to_uge())

        # check that projects have been added
        prjs = API.list_prjs()
        for name in prj_names:
            assert (name in prjs)
            print("project found: " + name)

    finally:
        API.delete_prjs(prj_names)


def test_modify_prjs():
    try:
        add_projects = []
        prj_names = VALUES_DICT['prj_names']
        # prj_names = ['tp1', 'tp2']
        for name in prj_names:
            nprj = API.generate_prj(name=name)
            add_projects.append(nprj)

        # print all projects currently in the cluster
        print("Before #############################################")
        prjs = API.get_prjs()
        for prj in prjs:
            print(prj.to_uge())

        # add projects
        API.add_prjs(add_projects)

        # modify added projects
        print("Before modify #############################################")
        prjs = API.get_prjs()
        for prj in prjs:
            if prj.data['name'] in prj_names:
                prj.data['oticket'] += 1
            else:
                print("project not found: " + prj.data['name'])
            print(prj.to_uge())
        API.modify_prjs(prjs)

        # check that projects have been changed
        print("After #############################################")
        prjs = API.get_prjs()
        for p in prjs:
            print(p.to_uge())
            if p.data['name'] in prj_names:
                print("project found: " + p.data['name'] + " with oticket=" + str(p.data['oticket']))
                # assert(p.data['oticket'] == 1)

    finally:
        API.delete_prjs(prj_names)
