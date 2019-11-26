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

import hashlib

from sawtooth_sdk.processor.exceptions import InternalError


IoT_NAMESPACE = hashlib.sha512('IoT'.encode("utf-8")).hexdigest()[0:6]


def _make_iot_address(name):
    return IoT_NAMESPACE + \
        hashlib.sha512(name.encode('utf-8')).hexdigest()[:64]

'''
class Data:
    def __init__(self, name, temperature, humidity):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity
        self.temperatureL = []
        self.humidityL = []
'''

class Data:
    def __init__(self, name, temperature, humidity):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity


class IoT_State:

    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context
        self._address_cache = {}
    
    def set_data(self, data_name, data):
        """Store the data in the validator state.
        Args:
            data_name (str): The name in data.
            data (Data): The information specifying the current data.
        """

        print('2. Ready to enter _load_dataSet function.')

        dataSet = self._load_dataSet(data_name=data_name)

        dataSet[data_name] = data

        self._store_data(data_name, dataSet=dataSet)

        print('4. State set_data np problem')

    def get_data(self, data_name):
        """Get the data associated with data_name.
        Args:
            data_name (str): The name.
        Returns:
            (Data): All the information specifying a data.
        """

        return self._load_dataSet(data_name=data_name).get(data_name)

    # Use the name in data to search the dataSet
    def _load_dataSet(self, data_name):
        address = _make_iot_address(data_name)

        if address in self._address_cache:
            if self._address_cache[address]:
                serialized_dataSet = self._address_cache[address]
                dataSet = self._deserialize(serialized_dataSet)
            else:
                dataSet = {}
        else:
            state_entries = self._context.get_state(
                [address],
                timeout=self.TIMEOUT)
            if state_entries:
                self._address_cache[address] = state_entries[0].data
                dataSet = self._deserialize(serialized_dataSet=state_entries[0].data)
            else:
                self._address_cache[address] = None
                dataSet = {}

        print('3. State _load_dataSet no problem.')
        return dataSet
    
    def _store_data(self, data_name, dataSet):
        address = _make_iot_address(data_name)

        state_data = self._serialize(dataSet)

        self._address_cache[address] = state_data

        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _deserialize(self, serialized_dataSet):
        """Take bytes stored in state and deserialize them into Python
        Game objects.
        Args:
            serialized_dataSet (bytes): The UTF-8 encoded string stored in state.
        Returns:
            (dict): the name in data (str) keys, Data values.
        """

        dataSet = {}
        try:
            for data in serialized_dataSet.decode().split('|'):
                name, temperature, humidity = data.split(',')

                dataSet[name] = Data(name, temperature, humidity)
        except ValueError:
            raise InternalError('Failed to deserialize IoT data')
        
        return dataSet

    def _serialize(self, dataSet):
        """Takes a dict of game objects and serializes them into bytes.
        Args:
            dataSet (dict): the name in data (str) keys, Data values.
        Returns:
            (bytes): The UTF-8 encoded string stored in state.
        """

        data_strs = []
        dataInfo_list = []
        for name, g in dataSet.items():
            data_str = ','.join(
                [name, str(g.temperature), str(g.humidity)])
            data_strs.append(data_str)

        return '|'.join(sorted(data_strs)).encode()
