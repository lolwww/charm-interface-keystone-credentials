#!/usr/bin/python
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

from charmhelpers.core import hookenv
from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class KeystoneProvides(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:keystone-credentials}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')
        self.update_state()
        self.set_state('{relation_name}.available.updated')
        hookenv.atexit(self._clear_updated)

    def update_state(self):
        """Update the states of the relations based on the data that the
        relation has.
        If the :meth:`base_data_complete` is False then all of the states
        are removed.  Otherwise, the individual states are set according to
        their own data methods.
        """
        # base_complete = self.base_data_complete()
        states = {
            '{relation_name}.available': True,
            '{relation_name}.available.ssl': False,
            '{relation_name}.available.auth': True
        }
        for k, v in states.items():
            if v:
                self.set_state(k)
            else:
                self.remove_state(k)

    @hook('{provides:keystone-credentials}-relation-changed')
    def changed(self):
        self.update_state()
        self.set_state('{relation_name}.available.updated')
        hookenv.atexit(self._clear_updated)

    @hook('{provides:keystone-credentials}-relation-{broken,departed}')
    def departed(self):
        self.remove_state('{relation_name}.connected')
        self.clean_state()

    def clean_state(self):
        empty_creds = {}
        self.push_into_relation(empty_creds)

    def push_into_relation(self, credentials):
        self.set_local(**credentials)
        self.set_remote(**credentials)

    def _clear_updated(self):
        self.remove_state('{relation_name}.available.updated')