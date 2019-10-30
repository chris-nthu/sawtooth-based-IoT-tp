# Copyright 2018 Intel Corporation
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
# -----------------------------------------------------------------------------

from sawtooth_sdk.processor.exceptions import InvalidTransaction


class IoT_Payload:

    # Check the command sent by client has error or not,
    # if no error, then parse the command.
    def __init__(self, payload):
        try:
            # The payload is csv utf-8 encoded string
            name, action, temperature, humidity = payload.decode.split(",")

        except ValueError:
            raise InvalidTransaction('Invalid payload serialization')
            
        if not name:
            raise InvalidTransaction('Name is required')
            
        if '|' in name:
            raise InvalidTransaction('Name cannot contain "|"')
            
        if not action:
            raise InvalidTransaction('Action is required')
            
        if action not in ('create', 'upload', 'delete'):
            raise InvalidTransaction('Invalid action: {}'.format(action))
            
        if action == 'upload':
            temperature = float(temperature)
            humidity = float(humidity)
            
        self._name = name
        self._action = action
        self._temperature = temperature
        self._humidity = humidity

    @staticmethod
    def from_bytes(payload):
        return IoT_Payload(payload=payload)
