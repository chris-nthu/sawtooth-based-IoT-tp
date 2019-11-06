# Copyright 2016-2018 Intel Corporation
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
# ------------------------------------------------------------------------------

import logging


from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError

from tpLib.IoT_payload import *
from tpLib.IoT_state import *


LOGGER = logging.getLogger(__name__)


class IoT_TransactionHandler(TransactionHandler):
    # Disable invalid-overridden-method. The sawtooth-sdk expects these to be
    # properties.
    # pylint: disable=invalid-overridden-method
    @property
    def family_name(self):
        return 'IoT'

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [IoT_NAMESPACE]
    
    def apply(self, transaction, context):
        
        header = transaction.header
        signer = header.signer_public_key

        #print('Receive transaction from client: ' transaction)

        iot_payload = IoT_Payload.from_bytes(transaction.payload)
        iot_state = IoT_State(context)

        if iot_payload.action == 'create':

            # Create a "data" structure and put "name" in it
            data = Data(name=iot_payload.name,
                        temperature='',
                        humidity='')
            
            # Store data in sawtooth blockchain
            iot_state.set_data(iot_payload.name, data)

            print('1. Handler create no problem.')
        
        elif iot_payload.action == 'upload':
            
            # Use name to retrive the data
            data = iot_state.get_data(iot_payload.name)

            # Put the IoT information in "data" structure
            data.temperature = iot_payload.temperature
            data.humidity = iot_payload.humidity

            # Store data in sawtooth blockchain
            iot_state.set_data(iot_payload.name, data)

        else:
            raise InvalidTransaction(
                'Unhandled action: {}'.format(iot_payload.action))

