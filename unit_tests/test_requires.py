# Copyright 2018 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest import mock

import requires

import charms_openstack.test_utils as test_utils


_hook_args = {}


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        defaults = []
        hook_set = {
            'when_all': {
                'joined': (
                    'endpoint.{endpoint_name}.joined',
                    'endpoint.{endpoint_name}.changed.release',
                    'endpoint.{endpoint_name}.changed.bin_path',
                    'endpoint.{endpoint_name}.changed.openstack_dir',),
            },
            'when_not': {
                'broken': ('endpoint.{endpoint_name}.joined',),
            },
        }
        # test that the hooks were registered via the
        # reactive.barbican_handlers
        self.registered_hooks_test_helper(requires, hook_set, defaults)


class TestDashboardPluginRequires(test_utils.PatchHelper):

    def setUp(self):
        super().setUp()
        self.dashboard_req = requires.DashboardPluginRequires(
            'some-relation', [])
        self._patches = {}
        self._patches_start = {}

    def tearDown(self):
        self.dashboard_req = None
        for k, v in self._patches.items():
            v.stop()
            setattr(self, k, None)
        self._patches = None
        self._patches_start = None

    def patch_dashboard(self, attr, return_value=None):
        mocked = mock.patch.object(self.dashboard_req, attr)
        self._patches[attr] = mocked
        started = mocked.start()
        started.return_value = return_value
        self._patches_start[attr] = started
        setattr(self, attr, started)

    def patch_topublish(self):
        self.patch_dashboard('_relations')
        relation = mock.MagicMock()
        to_publish = mock.PropertyMock()
        type(relation).to_publish = to_publish
        self._relations.__iter__.return_value = [relation]
        return relation.to_publish

    def test_joined(self):
        self.patch_object(requires, 'clear_flag')
        self.patch_object(requires, 'set_flag')
        self.dashboard_req.joined()
        self.clear_flag.assert_has_calls([
            mock.call('endpoint.some-relation.changed.release'),
            mock.call('endpoint.some-relation.changed.bin_path'),
            mock.call('endpoint.some-relation.changed.openstack_dir'),
        ])
        self.set_flag.assert_has_calls([
            mock.call('some-relation.connected'),
            mock.call('some-relation.available'),
        ])

    def test_broken(self):
        self.patch_object(requires, 'clear_flag')
        self.dashboard_req.broken()
        self.clear_flag.assert_has_calls([
            mock.call('some-relation.available'),
            mock.call('some-relation.connected'),
        ])

    def test_publish_plugin_info(self):
        to_publish = self.patch_topublish()
        local_settings = 'key = value'
        priority = 'priority'
        self.dashboard_req.publish_plugin_info(local_settings, priority)
        to_publish.__setitem__.assert_has_calls([
            mock.call('local-settings', local_settings),
            mock.call('priority', priority),
        ])
