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

# the reactive framework unfortunately does not grok `import as` in conjunction
# with decorators on class instance methods, so we have to revert to `from ...`
# imports
from charms.reactive import (
    Endpoint,
    clear_flag,
    set_flag,
    when_all,
    when_not,
)


class DashboardPluginRequires(Endpoint):
    @when_all('endpoint.{endpoint_name}.joined',
              'endpoint.{endpoint_name}.changed.release',
              'endpoint.{endpoint_name}.changed.bin_path',
              'endpoint.{endpoint_name}.changed.openstack_dir')
    def joined(self):
        clear_flag(
            self.expand_name(
                'endpoint.{endpoint_name}.changed.release'))
        clear_flag(
            self.expand_name(
                'endpoint.{endpoint_name}.changed.bin_path'))
        clear_flag(
            self.expand_name(
                'endpoint.{endpoint_name}.changed.openstack_dir'))
        set_flag(self.expand_name('{endpoint_name}.connected'))
        set_flag(self.expand_name('{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.expand_name('{endpoint_name}.available'))
        clear_flag(self.expand_name('{endpoint_name}.connected'))

    @property
    def release(self):
        """Retrieve the OpenStack release from principal

        :returns release: OpenStack release of principal
        :rtype release: str
        """
        return self.all_joined_units.received.get('release')

    @property
    def bin_path(self):
        """Retrieve bin_path property from principal charm

        :returns bin_path: bin_path property from principal charm
        :rtype bin_path: str
        """
        return self.all_joined_units.received.get('bin_path')

    @property
    def openstack_dir(self):
        """Retrieve openstack_dir property from principal charm

        :returns openstack_dir: openstack_dir property from principal charm
        :rtype openstack_dir: str
        """
        return self.all_joined_units.received.get('openstack_dir')

    def publish_plugin_info(self, local_settings, priority,
                            conflicting_packages=None,
                            install_packages=None):
        """Publish information about our plugin to principal charm.

        The conflicting_packages and install_packages allow the principal charm
        to wholly control what is installed and what isn't.

        :parm local_settings: String is pasted verbatim into the
                              local_settings.py of the principal.
        :type local_settings: str
        :param priority: Value used by principal to order the configuration
                         blobs when multiple plugin subordinates are present.
        :type priority: str
        :param conflicting_packages: List of packages that conflict with this
            dashboard plugin.
        :type conflicting_packages: List[str]
        :param install_packages: List of packages that need to be installed
            for this dashboard plugin to work.
        :type install_packages: List[str]
        """
        for relation in self.relations:
            relation.to_publish['local-settings'] = local_settings
            relation.to_publish['priority'] = priority
            # NOTE(ajkavanagh) to_publish automatically converts to JSON
            relation.to_publish['conflicting-packages'] = conflicting_packages
            relation.to_publish['install-packages'] = install_packages
